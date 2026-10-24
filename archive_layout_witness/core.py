import io,zipfile,tarfile,stat,unicodedata,re,posixpath
from .common import integer

def normalized(raw):
 s=raw.replace('\\','/');s=unicodedata.normalize('NFC',s)
 return posixpath.normpath(s)
def unsafe(raw):
 p=normalized(raw)
 return p.startswith('/')or p=='..'or p.startswith('../')or bool(re.match('^[A-Za-z]:',p))or'\x00'in p
def run(data):
 raw=bytes.fromhex(data['archive_hex']);kind=data['format'];limit=integer(data.get('maximum_uncompressed_bytes',20_000_000),1,20_000_000)
 if len(raw)>8_000_000:raise ValueError('archive_size')
 rows=[];total=0
 def add(name,size,type,target=None):
  nonlocal total
  total+=size
  if len(rows)>=1000 or total>limit:raise ValueError('archive_budget')
  issues=[]
  if unsafe(name):issues.append('unsafe_member_path')
  if target is not None:
   joined=posixpath.join(posixpath.dirname(normalized(name))if type=='symlink'else'',target.replace('\\','/'))
   if unsafe(target)and(target.startswith(('/','\\'))or re.match('^[A-Za-z]:',target))or unsafe(joined):issues.append('escaping_link_target')
  rows.append({'name':name,'portable_path':normalized(name).casefold(),'size':size,'kind':type,'link_target':target,'issues':issues})
 try:
  if kind=='zip':
   with zipfile.ZipFile(io.BytesIO(raw))as archive:
    infos=archive.infolist()
    if len(infos)>1000:raise ValueError('members')
    for item in infos:
     mode=item.external_attr>>16;symlink=stat.S_ISLNK(mode)
     if symlink and item.file_size>4096:raise ValueError('link_size')
     target=archive.read(item).decode('utf-8')if symlink else None
     add(item.filename,item.file_size,'symlink'if symlink else'directory'if item.is_dir()else'file',target)
  elif kind=='tar':
   with tarfile.open(fileobj=io.BytesIO(raw),mode='r:*')as archive:
    for item in archive:
     add(item.name,item.size,'symlink'if item.issym()else'hardlink'if item.islnk()else'directory'if item.isdir()else'file'if item.isfile()else'special',item.linkname if item.issym()or item.islnk()else None)
     if not(item.issym()or item.islnk()or item.isdir()or item.isfile()):rows[-1]['issues'].append('special_member')
  else:raise ValueError('format')
 except(zipfile.BadZipFile,tarfile.TarError,UnicodeError):raise ValueError('archive')from None
 links={normalized(row['name'])for row in rows if row['kind']in('symlink','hardlink')}
 for row in rows:
  components=normalized(row['name']).split('/')
  if any('/'.join(components[:i])in links for i in range(1,len(components))):row['issues'].append('member_below_link')
 groups={}
 for row in rows:groups.setdefault(row['portable_path'],[]).append(row['name'])
 collisions=[{'portable_path':k,'members':v}for k,v in sorted(groups.items())if len(v)>1]
 return {'members':rows,'portable_collisions':collisions,'declared_uncompressed_bytes':total,'model':'read_only_zip_tar_metadata_layout_nfc_casefold_portability_policy_no_extraction_or_crc_claim'}
