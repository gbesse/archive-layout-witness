import unittest,io,zipfile,tarfile
from archive_layout_witness import run
class Tests(unittest.TestCase):
 def zip(self,entries):
  buf=io.BytesIO()
  with zipfile.ZipFile(buf,'w')as z:
   for name,value in entries:z.writestr(name,value)
  return {'format':'zip','archive_hex':buf.getvalue().hex()}
 def test_traversal_and_case_unicode_collision_witnesses(self):
  r=run(self.zip([('../x','x'),('A.txt','a'),('a.txt','b'),('é','a'),('e\u0301','b')]));self.assertEqual(r['members'][0]['issues'],['unsafe_member_path']);self.assertEqual(len(r['portable_collisions']),2)
 def test_tar_link_escaping_and_safe_relative_link(self):
  buf=io.BytesIO()
  with tarfile.open(fileobj=buf,mode='w')as t:
   for name,target in [('dir/bad','../../outside'),('dir/good','../inside')]:
    item=tarfile.TarInfo(name);item.type=tarfile.SYMTYPE;item.linkname=target;t.addfile(item)
  r=run({'format':'tar','archive_hex':buf.getvalue().hex()});self.assertIn('escaping_link_target',r['members'][0]['issues']);self.assertEqual(r['members'][1]['issues'],[])
 def test_budget_checked_without_extraction(self):
  with self.assertRaises(ValueError):run({**self.zip([('x','abcd')]),'maximum_uncompressed_bytes':3})
 def test_windows_absolute_and_backslash_traversal(self):
  r=run(self.zip([('C:/outside','a'),('..\\outside','b')]));self.assertTrue(all('unsafe_member_path'in x['issues']for x in r['members']))
