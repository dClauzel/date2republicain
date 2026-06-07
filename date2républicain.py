#!/usr/bin/env python3
# /usr/local/bin/date2républicain.py
"""Convertir une date grégorienne en date du calendrier républicain français.

Le script accepte une date au format ISO 8601 (YYYY-MM-DD) ou, à défaut,
utilise la date courante.

Formats de sortie :
- texte simple ;
- JSON ;
- XML de données seul ;
- XSD seul ;
- document XML unique contenant à la fois un bloc <xs:schema> et un bloc <data> ;
- document XML unique avec DTD interne.

Exemples :
    ./date2républicain.py
    ./date2républicain.py 2026-06-07 --date --fête --officiel
    ./date2républicain.py 2026-06-07 --json
    ./date2républicain.py 2026-06-07 --xml
    ./date2républicain.py --xsd
    ./date2républicain.py 2026-06-07 --xml-inline-schema
    ./date2républicain.py 2026-06-07 --dtd
"""

import sys
import json
import argparse
from datetime import date
from typing import Any
from xml.sax.saxutils import escape as xml_escape


MOIS = [
    "Vendémiaire",
    "Brumaire",
    "Frimaire",
    "Nivôse",
    "Pluviôse",
    "Ventôse",
    "Germinal",
    "Floréal",
    "Prairial",
    "Messidor",
    "Thermidor",
    "Fructidor",
]

JOURS_DECADE = [
    "Primidi",
    "Duodi",
    "Tridi",
    "Quartidi",
    "Quintidi",
    "Sextidi",
    "Septidi",
    "Octidi",
    "Nonidi",
    "Décadi",
]

SANS_CULOTTIDES = [
    "la Vertu",
    "le Génie",
    "le Travail",
    "l'Opinion",
    "les Récompenses",
    "la Révolution",
]

NOMS_JOURS = [
    "le raisin",
    "le safran",
    "la châtaigne",
    "le colchique",
    "le cheval",
    "la balsamine",
    "la carotte",
    "l'amaranthe",
    "le panais",
    "la cuve",
    "la pomme de terre",
    "l'immortelle",
    "le potiron",
    "le réséda",
    "l'âne",
    "la belle de nuit",
    "la citrouille",
    "le sarrasin",
    "le tournesol",
    "le pressoir",
    "le chanvre",
    "la pêche",
    "le navet",
    "l'amaryllis",
    "le bœuf",
    "l'aubergine",
    "le piment",
    "la tomate",
    "l'orge",
    "le tonneau",
    "la pomme",
    "le céleri",
    "la poire",
    "la betterave",
    "l'oie",
    "l'héliotrope",
    "la figue",
    "la scorsonère",
    "l'alisier",
    "la charrue",
    "le salsifis",
    "la macre",
    "le topinambour",
    "l'endive",
    "le dindon",
    "le chervis",
    "le cresson",
    "la dentelaire",
    "la grenade",
    "la herse",
    "la bacchante",
    "l'azerole",
    "la garance",
    "l'orange",
    "le faisan",
    "la pistache",
    "le macjonc",
    "le coing",
    "le cormier",
    "le rouleau",
    "la raiponce",
    "le turneps",
    "la chicorée",
    "la nèfle",
    "le cochon",
    "la mâche",
    "le chou-fleur",
    "le miel",
    "le genièvre",
    "la pioche",
    "la cire",
    "le raifort",
    "le cèdre",
    "le sapin",
    "le chevreuil",
    "l'ajonc",
    "le cyprès",
    "le lierre",
    "la sabine",
    "le hoyau",
    "l'érable sucré",
    "la bruyère",
    "le roseau",
    "l'oseille",
    "le grillon",
    "le pignon",
    "le liège",
    "la truffe",
    "l'olive",
    "la pelle",
    "la tourbe",
    "la houille",
    "le bitume",
    "le soufre",
    "le chien",
    "la lave",
    "la terre végétale",
    "le fumier",
    "le salpêtre",
    "le fléau",
    "le granit",
    "l'argile",
    "l'ardoise",
    "le grès",
    "le lapin",
    "le silex",
    "la marne",
    "la pierre à chaux",
    "le marbre",
    "le van",
    "la pierre à plâtre",
    "le sel",
    "le fer",
    "le cuivre",
    "le chat",
    "l'étain",
    "le plomb",
    "le zinc",
    "le mercure",
    "le crible",
    "la lauréole",
    "la mousse",
    "le fragon",
    "le perce-neige",
    "le taureau",
    "le laurier-thym",
    "l'amadouvier",
    "le mézéréon",
    "le peuplier",
    "la coignée",
    "l'ellébore",
    "le brocoli",
    "le laurier",
    "l'avelinier",
    "la vache",
    "le buis",
    "le lichen",
    "l'if",
    "la pulmonaire",
    "la serpette",
    "le thlaspi",
    "la thimèle",
    "le chiendent",
    "la traînasse",
    "le lièvre",
    "la guède",
    "le noisetier",
    "le cyclamen",
    "la chélidoine",
    "le traîneau",
    "le tussilage",
    "le cornouiller",
    "le violier",
    "le troène",
    "le bouc",
    "l'asaret",
    "l'alaterne",
    "la violette",
    "le marceau",
    "la bêche",
    "le narcisse",
    "l'orme",
    "la fumeterre",
    "le vélar",
    "la chèvre",
    "l'épinard",
    "le doronic",
    "le mouron",
    "le cerfeuil",
    "le cordeau",
    "la mandragore",
    "le persil",
    "la cochléaria",
    "la pâquerette",
    "le thon",
    "le pissenlit",
    "la sylve",
    "le capillaire",
    "le frêne",
    "le plantoir",
    "la primevère",
    "le platane",
    "l'asperge",
    "la tulipe",
    "la poule",
    "la bette",
    "le bouleau",
    "la jonquille",
    "l'aulne",
    "le couvoir",
    "la pervenche",
    "le charme",
    "la morille",
    "le hêtre",
    "l'abeille",
    "la laitue",
    "le mélèze",
    "la cigüe",
    "le radis",
    "la ruche",
    "le gainier",
    "la romaine",
    "le marronnier",
    "la roquette",
    "le pigeon",
    "le lilas",
    "l'anémone",
    "la pensée",
    "la myrtille",
    "le greffoir",
    "la rose",
    "le chêne",
    "la fougère",
    "l'aubépine",
    "le rossignol",
    "l'ancolie",
    "le muguet",
    "le champignon",
    "la jacinthe",
    "le râteau",
    "la rhubarbe",
    "le sainfoin",
    "le bâton d'or",
    "le chamerops",
    "le ver à soie",
    "la consoude",
    "la pimprenelle",
    "la corbeille d'or",
    "l'arroche",
    "le sarcloir",
    "le statice",
    "la fritillaire",
    "la bourrache",
    "la valériane",
    "la carpe",
    "le fusain",
    "la civette",
    "la buglosse",
    "le sénevé",
    "la houlette",
    "la luzerne",
    "l'hémérocalle",
    "le trèfle",
    "l'angélique",
    "le canard",
    "la mélisse",
    "le fromental",
    "le martagon",
    "le serpolet",
    "la faux",
    "la fraise",
    "la bétoine",
    "le pois",
    "l'acacia",
    "la caille",
    "l'œillet",
    "le sureau",
    "le pavot",
    "le tilleul",
    "la fourche",
    "le barbeau",
    "la camomille",
    "le chèvrefeuille",
    "le caille-lait",
    "la tanche",
    "le jasmin",
    "la verveine",
    "le thym",
    "la pivoine",
    "le chariot",
    "le seigle",
    "l'avoine",
    "l'oignon",
    "la véronique",
    "le mulet",
    "le romarin",
    "le concombre",
    "l'échalote",
    "l'absinthe",
    "la faucille",
    "la coriandre",
    "l'artichaut",
    "le girofle",
    "la lavande",
    "le chamois",
    "le tabac",
    "la groseille",
    "la gesse",
    "la cerise",
    "le parc",
    "la menthe",
    "le cumin",
    "le haricot",
    "l'orcanète",
    "la pintade",
    "la sauge",
    "l'ail",
    "la vesce",
    "le blé",
    "la chalémie",
    "l'épeautre",
    "le bouillon-blanc",
    "le melon",
    "l'ivraie",
    "le bélier",
    "la prêle",
    "l'armoise",
    "le carthame",
    "la mûre",
    "l'arrosoir",
    "le panis",
    "la salicorne",
    "l'abricot",
    "le basilic",
    "la brebis",
    "la guimauve",
    "le lin",
    "l'amande",
    "la gentiane",
    "l'écluse",
    "la carline",
    "le câprier",
    "la lentille",
    "l'aunée",
    "la loutre",
    "le myrte",
    "le colza",
    "le lupin",
    "le coton",
    "le moulin",
    "la prune",
    "le millet",
    "le lycoperdon",
    "l'escourgeon",
    "le saumon",
    "la tubéreuse",
    "le sucrion",
    "l'apocyn",
    "la réglisse",
    "l'échelle",
    "la pastèque",
    "le fenouil",
    "l'épine-vinette",
    "la noix",
    "la truite",
    "le citron",
    "la cardère",
    "le nerprun",
    "la tagette",
    "la hotte",
    "l'églantier",
    "la noisette",
    "le houblon",
    "le sorgho",
    "l'écrevisse",
    "la bigarade",
    "la verge d'or",
    "le maïs",
    "le marron",
    "le panier",
]

DATE_DEBUT_OFFICIELLE = date(1792, 9, 22)
DATE_FIN_OFFICIELLE = date(1805, 12, 31)
EPOCH_JD = 2375840


def to_roman(n: int) -> str:
    """Convertir un entier positif en chiffres romains."""
    valeurs = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    resultat = ""
    for valeur, symbole in valeurs:
        while n >= valeur:
            resultat += symbole
            n -= valeur
    return resultat


def gregorian_to_jd(year: int, month: int, day: int) -> int:
    """Convertir une date grégorienne en numéro de jour julien."""
    if month <= 2:
        year -= 1
        month += 12
    a = year // 100
    b = 2 - a + a // 4
    return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524


def is_sextile(an: int) -> bool:
    """Indiquer si une année républicaine est sextile."""
    return (an % 4 == 0) and (an % 100 != 0 or an % 400 == 0) and (an % 4000 != 0)


def annee_debut_jd(an: int) -> int:
    """Calculer le jour julien du début d'une année républicaine."""
    jd = EPOCH_JD
    for y in range(1, an):
        jd += 366 if is_sextile(y) else 365
    return jd


def jd_to_republican(jd: int) -> tuple[int, int, int]:
    """Convertir un jour julien en date républicaine."""
    jd_rel = jd - EPOCH_JD
    if jd_rel < 0:
        raise ValueError(
            "Date antérieure au calendrier républicain (avant le 22/09/1792)."
        )

    an = jd_rel // 365 + 1
    while True:
        debut_suivant = annee_debut_jd(an + 1) - EPOCH_JD
        if jd_rel < debut_suivant:
            break
        an += 1

    debut_an = annee_debut_jd(an) - EPOCH_JD
    jour_dans_annee = jd_rel - debut_an

    if jour_dans_annee < 360:
        mois_idx = jour_dans_annee // 30
        jour = (jour_dans_annee % 30) + 1
    else:
        mois_idx = 12
        jour = jour_dans_annee - 360

    return an, mois_idx, jour


def get_components(
    greg_date: date, an: int, mois_idx: int, jour: int
) -> dict[str, Any]:
    """Construire les composants dérivés d'une date républicaine."""
    an_romain = to_roman(an)
    officiel = DATE_DEBUT_OFFICIELLE <= greg_date <= DATE_FIN_OFFICIELLE

    if mois_idx == 12:
        fete = SANS_CULOTTIDES[jour]
        return {
            "date_gregorienne": greg_date.isoformat(),
            "decade": None,
            "num_decade": None,
            "jour": None,
            "mois": None,
            "an": an_romain,
            "fete": fete,
            "date_complete": f"Jour de {fete} an {an_romain}",
            "date_courte": f"{fete} {an_romain}",
            "officiel": officiel,
            "periode_officielle_debut": DATE_DEBUT_OFFICIELLE.isoformat(),
            "periode_officielle_fin": DATE_FIN_OFFICIELLE.isoformat(),
            "sc_idx": jour,
        }

    num_decade = ((jour - 1) // 10) + 1
    decade = JOURS_DECADE[(jour - 1) % 10]
    mois = MOIS[mois_idx]
    fete = NOMS_JOURS[mois_idx * 30 + (jour - 1)]

    return {
        "date_gregorienne": greg_date.isoformat(),
        "decade": decade,
        "num_decade": num_decade,
        "jour": jour,
        "mois": mois,
        "an": an_romain,
        "fete": fete,
        "date_complete": f"{decade} {jour} {mois} an {an_romain}",
        "date_courte": f"{jour} {mois} {an_romain}",
        "officiel": officiel,
        "periode_officielle_debut": DATE_DEBUT_OFFICIELLE.isoformat(),
        "periode_officielle_fin": DATE_FIN_OFFICIELLE.isoformat(),
        "sc_idx": None,
    }


def format_text(c: dict[str, Any], opts: dict[str, bool]) -> str:
    """Formater la sortie texte selon les options demandées."""
    if c["sc_idx"] is not None:
        any_opt = any(opts.values())
        if not any_opt or opts.get("date"):
            return c["date_complete"] + "."

        parts = []
        if opts.get("an"):
            parts.append(c["an"])
        if opts.get("fete"):
            parts.append(c["fete"])
        if opts.get("officiel"):
            parts.append("officiel" if c["officiel"] else "hors période officielle")
        return " ".join(str(x) for x in parts) if parts else c["date_complete"] + "."

    any_opt = any(opts.values())
    if not any_opt:
        return f"{c['date_complete']}, on célèbre {c['fete']}."

    if opts.get("court"):
        return c["date_courte"]

    if opts.get("date"):
        base = c["date_complete"]
        if opts.get("fete"):
            base += f", on célèbre {c['fete']}"
        if opts.get("officiel"):
            base += ", officiel" if c["officiel"] else ", hors période officielle"
        return base + "."

    parts = []
    if opts.get("decade"):
        parts.append(c["decade"])
    if opts.get("num_decade"):
        parts.append(str(c["num_decade"]))
    if opts.get("jour"):
        parts.append(str(c["jour"]))
    if opts.get("mois"):
        parts.append(c["mois"])
    if opts.get("an"):
        parts.append(c["an"])
    if opts.get("fete"):
        parts.append(c["fete"])
    if opts.get("officiel"):
        parts.append("officiel" if c["officiel"] else "hors période officielle")
    return " ".join(parts)


def format_custom(c: dict[str, Any], pattern: str) -> str:
    """Appliquer un format personnalisé."""
    mapping = {
        "decade": c["decade"] or "",
        "num_decade": c["num_decade"] or "",
        "jour": c["jour"] or "",
        "mois": c["mois"] or "",
        "an": c["an"],
        "fete": c["fete"],
        "date": c["date_complete"],
        "court": c["date_courte"],
        "officiel": "true" if c["officiel"] else "false",
        "date_gregorienne": c["date_gregorienne"],
        "periode_officielle_debut": c["periode_officielle_debut"],
        "periode_officielle_fin": c["periode_officielle_fin"],
    }
    try:
        return pattern.format(**mapping)
    except KeyError as exc:
        raise ValueError(f"Champ inconnu dans --format : {exc.args[0]}") from exc


def format_json(c: dict[str, Any]) -> str:
    """Sérialiser les champs en JSON."""
    out = {
        "date_gregorienne": c["date_gregorienne"],
        "decade": c["decade"],
        "num_decade": c["num_decade"],
        "jour": c["jour"],
        "mois": c["mois"],
        "an": c["an"],
        "fete": c["fete"],
        "date_complete": c["date_complete"],
        "date_courte": c["date_courte"],
        "officiel": c["officiel"],
        "periode_officielle": {
            "debut": c["periode_officielle_debut"],
            "fin": c["periode_officielle_fin"],
        },
    }
    return json.dumps(out, ensure_ascii=False, indent=2)


def format_xml(c: dict[str, Any]) -> str:
    """Produire le document XML de données seul."""
    fields = {
        "date_gregorienne": c["date_gregorienne"],
        "decade": c["decade"],
        "num_decade": c["num_decade"],
        "jour": c["jour"],
        "mois": c["mois"],
        "an": c["an"],
        "fete": c["fete"],
        "date_complete": c["date_complete"],
        "date_courte": c["date_courte"],
        "officiel": str(c["officiel"]).lower(),
        "periode_officielle_debut": c["periode_officielle_debut"],
        "periode_officielle_fin": c["periode_officielle_fin"],
    }

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<calendrier_republicain>"]
    for key, value in fields.items():
        safe_value = "" if value is None else xml_escape(str(value))
        lines.append(f"  <{key}>{safe_value}</{key}>")
    lines.append("</calendrier_republicain>")
    return "\n".join(lines)


def _xsd_elements_block() -> str:
    """Générer les déclarations XSD des champs de calendrier_republicain."""
    nullable = {"decade", "num_decade", "jour", "mois"}
    date_fields = {
        "date_gregorienne",
        "periode_officielle_debut",
        "periode_officielle_fin",
    }

    sequence = [
        "date_gregorienne",
        "decade",
        "num_decade",
        "jour",
        "mois",
        "an",
        "fete",
        "date_complete",
        "date_courte",
        "officiel",
        "periode_officielle_debut",
        "periode_officielle_fin",
    ]

    lines: list[str] = []
    for name in sequence:
        if name in date_fields:
            lines.append(f'              <xs:element name="{name}" type="xs:date"/>')
        elif name == "officiel":
            lines.append(f'              <xs:element name="{name}" type="xs:boolean"/>')
        elif name == "num_decade":
            lines.extend(
                [
                    f'              <xs:element name="{name}">',
                    "                <xs:simpleType>",
                    '                  <xs:union memberTypes="xs:positiveInteger xs:string"/>',
                    "                </xs:simpleType>",
                    "              </xs:element>",
                ]
            )
        elif name in nullable:
            lines.append(
                f'              <xs:element name="{name}" type="xs:string" nillable="true"/>'
            )
        else:
            lines.append(f'              <xs:element name="{name}" type="xs:string"/>')

    return "\n".join(lines)


def format_xsd() -> str:
    """Produire le schéma XSD décrivant le bloc <data>."""
    elements = _xsd_elements_block()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:annotation>
    <xs:documentation>
      Schéma XSD pour la sortie XML de date2républicain.py.
      Validation usuelle : xmllint --schema calendrier_republicain.xsd --noout data.xml
    </xs:documentation>
  </xs:annotation>

  <xs:element name="data">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="calendrier_republicain">
          <xs:complexType>
            <xs:sequence>
{elements}
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>"""


def _xml_data_elements(c: dict[str, Any]) -> str:
    """Produire le bloc XML interne sous <calendrier_republicain>."""
    fields = {
        "date_gregorienne": c["date_gregorienne"],
        "decade": c["decade"],
        "num_decade": c["num_decade"],
        "jour": c["jour"],
        "mois": c["mois"],
        "an": c["an"],
        "fete": c["fete"],
        "date_complete": c["date_complete"],
        "date_courte": c["date_courte"],
        "officiel": str(c["officiel"]).lower(),
        "periode_officielle_debut": c["periode_officielle_debut"],
        "periode_officielle_fin": c["periode_officielle_fin"],
    }

    lines: list[str] = []
    for key, value in fields.items():
        safe = "" if value is None else xml_escape(str(value))
        lines.append(f"      <{key}>{safe}</{key}>")
    return "\n".join(lines)


def format_xml_inline_schema(c: dict[str, Any]) -> str:
    """Produire un document XML unique contenant <xs:schema> et <data>."""
    xsd_content = _xsd_elements_block()
    data_content = _xml_data_elements(c)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<document xmlns:xs="http://www.w3.org/2001/XMLSchema"',
        '          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">',
        "",
        "  <xs:schema>",
        "    <xs:annotation>",
        "      <xs:documentation>",
        "        Schéma XSD pour le bloc data du calendrier républicain.",
        "      </xs:documentation>",
        "    </xs:annotation>",
        "",
        '    <xs:element name="data">',
        "      <xs:complexType>",
        "        <xs:sequence>",
        '          <xs:element name="calendrier_republicain">',
        "            <xs:complexType>",
        "              <xs:sequence>",
        xsd_content,
        "              </xs:sequence>",
        "            </xs:complexType>",
        "          </xs:element>",
        "        </xs:sequence>",
        "      </xs:complexType>",
        "    </xs:element>",
        "  </xs:schema>",
        "",
        "  <data>",
        "    <calendrier_republicain>",
        data_content,
        "    </calendrier_republicain>",
        "  </data>",
        "",
        "</document>",
    ]
    return "\n".join(lines)


def format_xml_with_dtd(c: dict[str, Any]) -> str:
    """Produire un document XML unique avec DTD interne."""
    sequence = [
        "date_gregorienne",
        "decade",
        "num_decade",
        "jour",
        "mois",
        "an",
        "fete",
        "date_complete",
        "date_courte",
        "officiel",
        "periode_officielle_debut",
        "periode_officielle_fin",
    ]
    seq_str = ", ".join(sequence)
    elem_decls = "\n".join(f"  <!ELEMENT {name} (#PCDATA)>" for name in sequence)

    dtd = (
        f"<!DOCTYPE calendrier_republicain [\n"
        f"  <!ELEMENT calendrier_republicain ({seq_str})>\n"
        f"{elem_decls}\n"
        f"]>"
    )

    fields = {
        "date_gregorienne": c["date_gregorienne"],
        "decade": c["decade"],
        "num_decade": c["num_decade"],
        "jour": c["jour"],
        "mois": c["mois"],
        "an": c["an"],
        "fete": c["fete"],
        "date_complete": c["date_complete"],
        "date_courte": c["date_courte"],
        "officiel": str(c["officiel"]).lower(),
        "periode_officielle_debut": c["periode_officielle_debut"],
        "periode_officielle_fin": c["periode_officielle_fin"],
    }

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        dtd,
        "<calendrier_republicain>",
    ]
    for key, value in fields.items():
        safe = "" if value is None else xml_escape(str(value))
        lines.append(f"  <{key}>{safe}</{key}>")
    lines.append("</calendrier_republicain>")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """Construire et analyser les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Convertit une date grégorienne en date républicaine française.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  %(prog)s
  %(prog)s 1795-04-09
  %(prog)s --mois --an
  %(prog)s 2026-06-07 --fête
  %(prog)s --date --fête --officiel
  %(prog)s --court
  %(prog)s --json
  %(prog)s --xml
  %(prog)s --xsd
  %(prog)s --xml-inline-schema
  %(prog)s --dtd
  %(prog)s --format "{decade} {jour} {mois} an {an} — {fete}"

Champs disponibles avec --format :
  {decade} {num_decade} {jour} {mois} {an} {fete}
  {date} {court} {officiel} {date_gregorienne}
  {periode_officielle_debut} {periode_officielle_fin}
        """,
    )
    parser.add_argument(
        "date_iso",
        nargs="?",
        metavar="YYYY-MM-DD",
        help="Date grégorienne (défaut : aujourd'hui)",
    )
    parser.add_argument(
        "--décade",
        "--decade",
        dest="decade",
        action="store_true",
        help="Affiche le nom dans la décade",
    )
    parser.add_argument(
        "--numdécade",
        "--numdecade",
        dest="num_decade",
        action="store_true",
        help="Affiche le numéro de décade (1 à 3)",
    )
    parser.add_argument(
        "--jour", dest="jour", action="store_true", help="Affiche le numéro du jour"
    )
    parser.add_argument(
        "--mois", dest="mois", action="store_true", help="Affiche le mois"
    )
    parser.add_argument(
        "--an",
        dest="an",
        action="store_true",
        help="Affiche l'année en chiffres romains",
    )
    parser.add_argument(
        "--date", dest="date", action="store_true", help="Affiche la date complète"
    )
    parser.add_argument(
        "--fête",
        "--fete",
        dest="fete",
        action="store_true",
        help="Affiche la fête du jour",
    )
    parser.add_argument(
        "--officiel",
        dest="officiel",
        action="store_true",
        help="Indique si la date est dans la période historique officielle",
    )
    parser.add_argument(
        "--court", dest="court", action="store_true", help="Affiche une forme courte"
    )
    parser.add_argument(
        "--format", dest="custom_format", help="Format personnalisé avec champs nommés"
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Affiche une sortie JSON",
    )
    parser.add_argument(
        "--xml",
        dest="xml_output",
        action="store_true",
        help="Affiche une sortie XML des données",
    )
    parser.add_argument(
        "--xsd",
        dest="xsd_output",
        action="store_true",
        help="Affiche le schéma XSD du bloc <data>",
    )
    parser.add_argument(
        "--xml-inline-schema",
        dest="xml_inline_schema",
        action="store_true",
        help="Produit un document XML unique contenant <xs:schema> et <data>",
    )
    parser.add_argument(
        "--dtd",
        dest="dtd_output",
        action="store_true",
        help="Produit un document XML unique avec DTD interne",
    )
    return parser.parse_args()


def resolve_date(date_iso: str | None) -> date:
    """Résoudre la date fournie par l'utilisateur."""
    if date_iso is None:
        return date.today()
    try:
        return date.fromisoformat(date_iso)
    except ValueError as exc:
        raise ValueError(
            f"date invalide : '{date_iso}' ; format attendu YYYY-MM-DD"
        ) from exc


def main() -> int:
    """Point d'entrée principal du programme."""
    args = parse_args()

    try:
        d = resolve_date(args.date_iso)
        jd = gregorian_to_jd(d.year, d.month, d.day)
        an, mois_idx, jour = jd_to_republican(jd)
        components = get_components(d, an, mois_idx, jour)

        exclusive = sum(
            bool(x)
            for x in [
                args.custom_format,
                args.json_output,
                args.xml_output,
                args.xsd_output,
                args.xml_inline_schema,
                args.dtd_output,
            ]
        )
        if exclusive > 1:
            raise ValueError(
                "--format, --json, --xml, --xsd, --xml-inline-schema "
                "et --dtd sont mutuellement exclusifs"
            )

        if args.json_output:
            print(format_json(components))
            return 0

        if args.xml_output:
            print(format_xml(components))
            return 0

        if args.xsd_output:
            print(format_xsd())
            return 0

        if args.xml_inline_schema:
            print(format_xml_inline_schema(components))
            return 0

        if args.dtd_output:
            print(format_xml_with_dtd(components))
            return 0

        if args.custom_format:
            print(format_custom(components, args.custom_format))
            return 0

        opts = {
            "decade": args.decade,
            "num_decade": args.num_decade,
            "jour": args.jour,
            "mois": args.mois,
            "an": args.an,
            "date": args.date,
            "fete": args.fete,
            "officiel": args.officiel,
            "court": args.court,
        }
        print(format_text(components, opts))
        return 0

    except ValueError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
