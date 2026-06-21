# date2républicain

Convertit une date grégorienne en date du calendrier républicain français.

## Description

`date2républicain.py` accepte une date au format ISO 8601 (`YYYY-MM-DD`) ou, à défaut, utilise la date du jour. Il calcule la date républicaine correspondante, le nom de la décade, la fête du jour selon le calendrier de Fabre d'Églantine, et indique si la date se situe dans la période d'usage historique officiel (22 septembre 1792 – 31 décembre 1805).

Le script est autonome : aucune dépendance externe, bibliothèque standard Python uniquement.

## Prérequis

- Python 3.10+

## Installation

```sh
cp date2républicain.py /usr/local/bin/date2républicain.py
chmod +x /usr/local/bin/date2républicain.py
```

## Utilisation

```sh
date2républicain.py [YYYY-MM-DD] [OPTIONS]
```

Sans argument, la date du jour est utilisée.

### Options de sélection des champs (texte)

| Option        | Description                                       |
| ------------- | ------------------------------------------------- |
| `--date`      | Date républicaine complète                        |
| `--court`     | Forme courte (`jour mois an`)                     |
| `--décade`    | Nom du jour dans la décade (Primidi, Duodi…)      |
| `--numdécade` | Numéro de décade (1 à 3)                          |
| `--jour`      | Numéro du jour dans le mois                       |
| `--mois`      | Nom du mois                                       |
| `--an`        | Année en chiffres romains                         |
| `--fête`      | Fête du jour (calendrier de Fabre d'Églantine)    |
| `--officiel`  | Indique si la date est dans la période officielle |

### Options de format de sortie (exclusifs)

| Option                | Description                                              |
| --------------------- | -------------------------------------------------------- |
| `--json`              | Sortie JSON                                              |
| `--xml`               | Sortie XML des données seules                            |
| `--xsd`               | Schéma XSD du bloc `<calendrier_republicain>`            |
| `--xml-inline-schema` | Document XML unique avec `<xsd:schema>` et données       |
| `--dtd`               | Document XML unique avec DTD interne                     |
| `--format PATTERN`    | Format personnalisé avec champs nommés (voir ci-dessous) |

### Format personnalisé

```sh
date2républicain.py --format "{decade} {jour} {mois} an {an} — {fete}"
```

Champs disponibles : `{decade}` `{num_decade}` `{jour}` `{mois}` `{an}` `{fete}` `{date}` `{court}` `{officiel}` `{date_gregorienne}` `{periode_officielle_debut}` `{periode_officielle_fin}`

## Exemples

```sh
# Date du jour, sortie complète par défaut
date2républicain.py

# Date spécifique, date + fête + indicateur officiel
date2républicain.py 2026-06-07 --date --fête --officiel

# Date historique (dans la période officielle)
date2républicain.py 1795-04-09

# Sortie JSON
date2républicain.py 2026-06-07 --json

# Sortie XML
date2républicain.py 2026-06-07 --xml

# Schéma XSD seul
date2républicain.py --xsd

# Document XML avec schéma inline
date2républicain.py 2026-06-07 --xml-inline-schema

# Document XML avec DTD interne
date2républicain.py 2026-06-07 --dtd

# Format personnalisé
date2républicain.py --format "{decade} {jour} {mois} an {an} — {fete}"
```

## Licence

En ce glorieux jour du 2026-06-21, moi Damien Clauzel place ce logiciel sous la [licence « Fais pas chier » (FPC)](https://clauzel.eu/FPC/).
