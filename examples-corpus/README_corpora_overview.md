# Synthetische Testkorpora für MTA — Übersicht (Deutsch)

Dieser Ordner enthält **fünf synthetische Korpora** für das Testen und
Unterrichten von MTA, alle auf Deutsch. Sie wurden für verschiedene
soziologische Untersuchungsdesigns konzipiert.

## ⚠ Wichtig: Es handelt sich um fiktive Daten

**Alle Korpora sind synthetisch**, erzeugt durch Python-Skripte mit
sorgfältig konstruierten Satz-Pools. Sie sind didaktische Werkzeuge,
keine empirischen Daten. Ziehen Sie keine soziologischen Schlüsse
aus diesen Texten.

## Übersicht der Korpora

| # | Ordner | Was | Dimensionen | Erwartete Differenzierung |
|---|--------|-----|-------------|---------------------------|
| 1 | `test_interviews_covid_en/` | 50 Covid-Interviews, **Englisch** | gender × age × income | Income: klar / Age: mäßig / Gender: subtil |
| 1' | `test_interviews_covid_de/` | 50 Covid-Interviews, **Deutsch** (Paralleldatei zu #1) | gender × age × income | gleich wie #1 |
| 2 | `test_articles_journ_sci_de/` | 50 Artikel, **Journalismus vs. Wissenschaft** | style × domain | Style: sehr klar / Domain: subtil |
| 3 | `test_biographies_de/` | 50 Lebensgeschichten, 1. Person | gender × profession | Profession: klar / Gender: subtil |
| 4 | `test_health_de/` | 80 Gesundheitsaussagen | location × gender × age × education | Education: klar / Location, Gender: mäßig / Age: subtil |
| 5 | `test_human_ai_de/` | 50 Texte, **Mensch vs. KI-Stil** | style | Style: sehr klar — siehe Warnung unten |

Jeder Ordner enthält:
- Die `.txt`-Dateien des Korpus
- Eine `*_metadata.csv` für die Gruppenextraktion via CSV
- Ein eigenes `README_test_dataset.md` mit Details

## Welches Korpus für welche Lehrsituation?

- **Erstes Beispiel im Unterricht**: Korpus #1' (Covid DE) — bekanntes Thema, drei Dimensionen, drei verschiedene Differenzierungsstärken in einem einzigen Korpus.
- **Sprachvergleich**: #1 ↔ #1' (englisch & deutsch parallel) — zeigt, dass MTA Diskursstruktur erfasst, nicht Sprachartefakte.
- **Stilanalyse**: Korpus #2 (Journ vs Sci) — zeigt, wie klar Topic Modeling stilistische Register trennt.
- **Biographische Methode**: Korpus #3 — Aufbau der Lebensgeschichte sichtbar machen.
- **Multidimensionale Analyse**: Korpus #4 (Gesundheit) — CSV mit 4 Spalten, jede Dimension separat analysierbar.
- **Methodenkritik & KI-Diskurs**: Korpus #5 — siehe Warnung unten.

## Wichtige Warnung zu Korpus #5 (Mensch vs. KI)

**Dieses Korpus testet keinen 'KI-Detektor' im allgemeinen Sinn.**

Was passiert: Die `human`-Texte enthalten Marker des spontanen Sprechens
(Füllwörter, Brüche, Anekdoten). Die `ai`-Texte enthalten Marker
des förmlichen LLM-Schreibens im Standardmodus (formelle Einleitungen,
ausgewogene Listen, Metadiskurs, zusammenfassende Schlüsse). Beide
wurden bewusst KONSTRUIERT. MTA findet, was hineinprogrammiert wurde.

**Was Studierende lernen sollten:**
1. Topic Modeling kann stilistische Register sehr klar trennen — eine
   echte methodologische Erkenntnis.
2. Ein Mensch, der formell schreibt, oder eine KI mit der Anweisung
   "schreibe wie ein hesitierender Mensch" könnte dieselben Tests
   bestehen — die Klassifikation gilt für *einen bestimmten Schreibstil*,
   nicht für die Quelle.
3. Was MTA wirklich detektiert, ist also nicht "KI vs. Mensch", sondern
   "stylistic register A vs. stylistic register B" — und das ist eine
   wichtige epistemologische Differenzierung.

## Schnellstart für jedes Korpus

```bash
# Mit Streamlit-App
.venv/bin/streamlit run code/streamlit_app.py
# → 'Load corpus' Seite: .txt-Dateien des gewählten Korpus + stopwords_de.txt hochladen
# → 'Topic models': NMF mit k=4 (k=3 für Korpus #5)
# → 'Group comparison': CSV des Korpus hochladen für simultane Analyse aller Dimensionen

# Mit CLI (Beispiel: Korpus #4)
.venv/bin/python code/MTA_v2.py \
    --corpus    examples/test_health_de \
    --stopwords examples/stopwords_de.txt \
    --action compare-groups \
    --groups-from csv \
    --groups-csv examples/test_health_de/health_metadata.csv \
    --n-topics 4 --language de
```

## Position der Gruppencodes im Dateinamen

Alle Korpora kodieren die Gruppendimensionen im Dateinamen (getrennt durch `_`),
sodass Sie sie auch ohne CSV mit `--groups-from filenames --group-position N`
analysieren können. Position 1 = erstes Element des Dateinamens.

| Korpus | Position 2 | Position 3 | Position 4 | Position 5 |
|--------|-----------|-----------|-----------|-----------|
| #1, #1' (Covid) | gender (F/M) | age band | income | — |
| #2 (Journ/Sci) | style (journ/sci) | domain (med/soc/cli/eco) | — | — |
| #3 (Biographies) | gender (F/M) | profession | — | — |
| **#4 (Gesundheit)** | **location (urban/rural)** | **gender (F/M)** | **age (young/mid/old)** | **education (low/mid/high)** |
| #5 (Mensch/KI) | style (human/ai) | — | — | — |

## Neu generieren

Jedes Korpus hat seinen eigenen Generator (`make_test_*.py`).
Mit `--seed N` können Sie verschiedene Stichproben desselben
generativen Prozesses erzeugen — nützlich für Robustheitsübungen.
