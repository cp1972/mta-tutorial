# Testkorpus für Interviews — Covid-Pandemie (synthetisch, Deutsch)

Dieser Ordner enthält ein **synthetisches** Korpus von 50 kurzen Interviews
über die Covid-19-Pandemie, das zum Testen und Lehren der
Gruppenvergleichsfunktion in MTA dient. Jedes Interview ist ein
halbstrukturierter Austausch (F/A-Format) mit 7 Fragen aus einer
zufälligen Auswahl.

Dies ist die **deutsche Parallele** zum englischen Korpus
`test_interviews_covid_en/`: gleicher Zufalls-Seed (42), gleiche
Profilverteilung, gleiche Themen-Gewichtungen. Die statistischen
Muster sollten daher in beiden Sprachen sehr ähnlich sein — was
zeigt, dass MTA die *Wortstruktur des Diskurses* erfasst, nicht
einen Sprachartefakt.

## ⚠ Wichtig: Es handelt sich um fiktive Daten

Diese Interviews wurden durch ein Python-Skript erzeugt. Sie benutzen
plausible Sätze, sind aber **keine echten Aussagen**. Verwenden Sie sie
nur zum:

1. Erlernen der MTA-Funktionsweise
2. Üben der statistischen Interpretation
3. Demonstrieren der Pipeline im Unterricht

## Struktur

- **50 Interview-Dateien** benannt nach dem Schema
  `interview_<gender>_<age>_<income>_<id>.txt`
- **Eine Metadaten-CSV** `interviews_metadata.csv` listet jede Datei
  mit ihren drei Gruppencodes auf — direkt verwendbar mit der
  MTA-Option `--groups-from csv`

## Profilverteilung

| Dimension | Kategorien | Anzahl |
| --- | --- | --- |
| Geschlecht (gender) | F, M | 28 F / 22 M |
| Altersgruppe (age) | 18-29, 30-44, 45-59, 60+ | 12 / 18 / 12 / 8 |
| Einkommen (income) | low, mid, high | 18 / 19 / 13 |

Die Verteilung ist **leicht unausgewogen**, um eine realistische
Felderhebung statt eines kontrollierten Experiments widerzuspiegeln.

## Welche Unterschiede sind zu erwarten?

Der Generator wurde so konzipiert, dass er drei Niveaus der
Gruppendifferenzierung erzeugt, von klar bis subtil. Das zwingt die
Studierenden dazu, **wirklich die p-Werte zu lesen**, statt anzunehmen,
dass jeder Vergleich signifikant ist.

| Gruppierung | Erwartete Differenzierung | Warum |
| --- | --- | --- |
| **Income** | **Klar** | Die Ungleichheiten während Covid sind gut dokumentiert (Jobverlust vs. komfortables Homeoffice). Mehrere Topics sollten sich stark unterscheiden. |
| **Age** | **Mäßig** | Verschiedene Lebensphasen führten zu unterschiedlichen Sorgen (Prekarität bei den Jungen, Elternschaft im mittleren Alter, Isolation bei den Älteren). Einige Topics werden sich unterscheiden, andere nicht. |
| **Gender** | **Subtil** | Unterschiede bei Hausarbeit und Homeoffice-Stil sind vorhanden, aber feiner. Etwa die Hälfte der Topics könnte unterscheiden. |

Nach dem Ausführen von MTA auf diesem Korpus sollten Sie ungefähr
folgendes beobachten:

- Für **income** bei α=0,05: Die meisten paarweisen Vergleiche
  (NMF k=4) kommen sowohl bei Welch als auch bei Mann-Whitney
  signifikant zurück und **überstehen die Benjamini-Hochberg-Korrektur**.
- Für **age** bei α=0,05: Einige Vergleiche sind roh signifikant, aber
  die Korrektur reduziert sie deutlich — ein guter Lehrmoment über
  Mehrfachtests.
- Für **gender** bei α=0,05: Ungefähr die Hälfte der Topics
  unterscheidet die Gruppen, die andere Hälfte nicht.

Die tatsächlichen Zahlen hängen vom Zufalls-Seed und den NMF/LDA-
Modellparametern ab.

## Anwendung mit MTA

### Schnellstart — Streamlit-Webapp

1. Starten Sie MTA über `start_MTA` und wählen Sie Option
   `[1] Streamlit web app`.
2. Auf der Seite "Load corpus" laden Sie alle 50 `.txt`-Dateien plus
   eine Stopword-Datei hoch (die mitgelieferte `stopwords_de.txt`
   funktioniert gut).
3. Führen Sie NMF und LDA auf der Seite "Topic models" aus (versuchen
   Sie zunächst k=4).
4. Auf der neuen Seite "Group comparison" wählen Sie entweder:
   - Position **2** für den Vergleich nach Geschlecht,
   - Position **3** für das Alter,
   - Position **4** für das Einkommen,
   - Oder laden Sie `interviews_metadata.csv` hoch, um alle drei
     Dimensionen auf einmal zu vergleichen.

### Schnellstart — Kommandozeile

```bash
# Vergleich nach Einkommen
.venv/bin/python code/MTA_v2.py \
    --corpus    examples/test_interviews_covid_de \
    --stopwords examples/stopwords_de.txt \
    --action compare-groups \
    --groups-from filenames --group-position 4 \
    --n-topics 4 --language de

# Alle drei Dimensionen auf einmal via CSV
.venv/bin/python code/MTA_v2.py \
    --corpus    examples/test_interviews_covid_de \
    --stopwords examples/stopwords_de.txt \
    --action compare-groups \
    --groups-from csv \
    --groups-csv examples/test_interviews_covid_de/interviews_metadata.csv \
    --n-topics 4 --language de
```

## Vorgeschlagene Unterrichtsaufgaben

1. **Interpretationsübung.** Identifizieren Sie für jedes signifikante
   Topic in der "income"-Gruppierung die repräsentativsten Wörter
   (Seite 2 in Streamlit, oder `nmf_top_words.csv` im Batch-Modus) und
   schlagen Sie eine soziologische Bezeichnung vor. Diskutieren Sie, ob
   die Bezeichnung angesichts des Einkommensgefälles Sinn ergibt.

2. **Mehrfachtest-Übung.** Wählen Sie die "age"-Gruppierung (k=4
   ergibt 24 paarweise Tests). Zählen Sie, wie viele Tests bei roh
   p<0,05 signifikant sind, dann wie viele die BH-Korrektur überstehen.
   Diskutieren Sie, warum das für ehrliche Berichterstattung wichtig ist.

3. **Effektgröße vs. p-Wert-Übung.** Vergleichen Sie für ein Topic die
   *mittleren* Gewichte zwischen zwei Gruppen (Effektgröße) und den
   *p-Wert* (statistische Signifikanz). Konstruieren Sie Fälle, in denen
   p klein ist, der Unterschied aber soziologisch trivial — oder
   umgekehrt.

4. **Sprachvergleich-Übung.** Führen Sie die gleiche Analyse auf
   diesem deutschen Korpus UND auf seinem englischen Pendant
   (`test_interviews_covid_en/`) aus. Vergleichen Sie die statistischen
   Muster: sind sie ähnlich? Wenn ja, was sagt das über die
   Diskursstruktur aus, die MTA erfasst? Diese Übung gibt es nicht für
   echte Daten, aber sie ist hier möglich, weil die beiden Korpora
   denselben Seed verwenden.

5. **Robustheitsübung.** Erzeugen Sie das Korpus mit einem anderen
   Seed neu (`python make_test_interviews_de.py --seed 123 --output
   ./test_v2_de`) und führen Sie die Analyse erneut aus. Wie stabil
   sind die Schlussfolgerungen über verschiedene Zufallsstichproben
   desselben datenerzeugenden Prozesses hinweg?

## Korpus neu generieren

Das Skript `make_test_interviews_de.py` ermöglicht es, neue Varianten
zu erstellen:

```bash
# Standard: 50 Interviews mit Seed 42
python make_test_interviews_de.py

# Eine andere Stichprobe (gleicher generativer Prozess, andere Ziehungen)
python make_test_interviews_de.py --seed 123

# Ein größeres Korpus für stärkere statistische Power
python make_test_interviews_de.py --seed 42 --n-interviews 200
```

## Hinweis zu den synthetischen Sätzen

Der Satz-Pool wurde so gestaltet, dass er soziologisch plausibel,
aber bewusst vereinfacht ist. Echte Interviews würden Zögern,
Selbstkorrekturen, idiosynkratisches Vokabular, Erzählbögen und
Widersprüche enthalten — nichts davon ist hier präsent. Das Testkorpus
ist ein **vereinfachtes Labormodell** dessen, wie echte Interviewdaten
aus Sicht eines Topic-Modells aussehen, kein Ersatz dafür.
