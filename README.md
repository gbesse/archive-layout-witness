# archive-layout-witness

## Français

Auditer les chemins et collisions d’une archive sans l’extraire.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m archive_layout_witness examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Inspecte de vrais ZIP/TAR sans extraction : traversée de chemin, liens sortants et collisions selon une politique portable NFC + casse repliée. Rend chaque membre problématique et les groupes de collision.

### Limites

Politique portable explicite, pas émulation de chaque système de fichiers ni certificat de sécurité. Métadonnées et cibles de liens seulement ; CRC et contenu des fichiers ordinaires non validés.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Audit archive paths and collisions without extracting it.

Synthetic data; no network access or secret required.

```sh
python -m archive_layout_witness examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Inspects actual ZIP/TAR without extraction: path traversal, escaping links and collisions under a portable NFC + casefold policy. Reports problematic members and collision groups.

### Limits

Explicit portability policy, not every-filesystem emulation or security certificate. Metadata and link targets only; ordinary-file contents and CRC are not validated.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Auditar rutas y colisiones de un archivo sin extraerlo.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m archive_layout_witness examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Inspecciona ZIP/TAR reales sin extraer: rutas ascendentes, enlaces salientes y colisiones bajo política portátil NFC + casefold. Informa miembros problemáticos y grupos de colisión.

### Límites

Política portátil explícita, no emulación de cada sistema de archivos o certificado de seguridad. Solo metadatos y destinos; no valida contenido ordinario ni CRC.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://docs.python.org/3/library/tarfile.html#extraction-filters
- https://docs.python.org/3/library/zipfile.html
