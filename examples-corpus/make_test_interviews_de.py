#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_test_interviews_de.py
==========================

Generate a synthetic GERMAN-language Covid interview corpus for MTA
classroom testing. Parallel structure to the English version: same
profile distribution, same theme weights, same seed produces the
same set of profiles → results between EN and DE versions are
sociologically comparable.

USAGE
-----
    python make_test_interviews_de.py [--seed SEED] [--output DIR]

DESIGN
------
- Same five theme blocks as the English corpus:
    * Income-driven    (financial_struggle / financial_comfort / middle_finances)
    * Age-driven       (young_precarity / middle_parenting / older_career_stress / elder_isolation)
    * Gender-leaning   (domestic_load / remote_work_technical)
    * Universal Covid  (masks_distancing / vaccination / health_worry / digital_tools / social_relations / policy_views / looking_back)
- Same profile distribution: 28 F / 22 M, 12/18/12/8 per age band, 18/19/13 per income.
- Same theme weights as the English version (so groups DIFFER on the
  same dimensions in both languages).
- German vocabulary uses authentic terms: Kurzarbeit, Tafel, Lockdown,
  Maskenpflicht, Impfquote, Homeoffice, Tagesmutter, Impfnachweis,
  Pflegeheim, etc.

This is a SYNTHETIC corpus for teaching the MTA pipeline only.
Do NOT draw real sociological conclusions from these interviews.
"""

import argparse
import csv
import random
import os
from pathlib import Path

# =============================================================================
# QUESTION POOL — interviewer's voice in German
# =============================================================================
QUESTIONS = [
    "Wie haben Sie die Lockdown-Phasen erlebt?",
    "Was hat sich in Ihrem Alltag während der Pandemie am meisten verändert?",
    "Wie sind Sie mit Arbeit und Einkommen in dieser Zeit umgegangen?",
    "Haben Sie sich Sorgen um Ihre Gesundheit oder die Ihrer Angehörigen gemacht?",
    "Wie haben sich Ihre sozialen Beziehungen während der Pandemie entwickelt?",
    "Welche Rolle spielten digitale Werkzeuge in Ihrem Alltag?",
    "Wie blicken Sie auf die Impfkampagne zurück?",
    "Welche Lehren ziehen Sie aus dieser Zeit?",
    "Fanden Sie die Einschränkungen gerechtfertigt oder übertrieben?",
    "Wie haben Sie sich zu den Masken- und Abstandsregeln gefühlt?",
]

# =============================================================================
# SENTENCE POOL — German equivalents of the English themes
# =============================================================================
SENTENCES = {
    # ---- Income-driven themes ----
    "financial_struggle": [
        "Das Geld war in diesen Monaten sehr knapp, ich musste überall sparen.",
        "Ich habe meinen Job in der ersten Welle verloren und es hat ewig gedauert, etwas Neues zu finden.",
        "Ich bin zum ersten Mal in meinem Leben zur Tafel gegangen, das war erniedrigend.",
        "Die Miete zu zahlen wurde jeden Monat zu einer echten Belastung und Quelle von Angst.",
        "Ich musste meine Familie um Hilfe für die Rechnungen bitten, was ich nie zuvor getan hatte.",
        "Das Kurzarbeitergeld kam spät und reichte nicht zum Leben.",
        "Ich habe Zahnarztbesuche und anderes verschoben, weil das Geld einfach fehlte.",
        "Wir haben bei Essen und Kleidung gespart, um das Nötigste bezahlen zu können.",
        "Mein Partner und ich haben gleichzeitig Einkommen verloren, das war wirklich hart.",
        "Der Kündigungsschutz hat uns wahrscheinlich vor der Obdachlosigkeit bewahrt.",
    ],
    "financial_comfort": [
        "Finanziell hatten wir Glück, mein Job ging im Homeoffice ohne Probleme weiter.",
        "Wir haben während des Lockdowns sogar gespart, weil wir nicht reisen oder essen gehen konnten.",
        "Ich habe das Ersparte genutzt, um unser Haus zu renovieren und das Homeoffice zu verbessern.",
        "Unsere Investitionen sind erst eingebrochen, haben sich aber dann wieder schön erholt.",
        "Wir haben ein Zweitwohnsitz auf dem Land gekauft, für die Wochenenden.",
        "Die Reisebeschränkungen haben uns finanziell nichts gekostet, wir haben die Reisen einfach verschoben.",
        "Ich habe mehrere Monate aus unserem Ferienhaus gearbeitet, es war eigentlich sehr angenehm.",
        "Wir haben in bessere Technik investiert, um die Heimarbeit komfortabler zu gestalten.",
        "Die Pandemie hat unser Familienbudget kaum berührt, wir hatten wirklich Glück.",
        "Wir haben lokale Geschäfte unterstützt, weil wir uns das leisten konnten.",
    ],
    "middle_finances": [
        "Wir sind finanziell zurechtgekommen, mussten aber bewusster mit Ausgaben umgehen.",
        "Ich habe einen Teil unserer Ersparnisse aufgebraucht, um durch die unsicheren Monate zu kommen.",
        "Mein Gehalt wurde eine Zeit lang gekürzt, aber mein Arbeitsplatz war nie wirklich in Gefahr.",
        "Wir haben den Kauf eines neuen Autos und ein paar andere Ausgaben verschoben.",
        "Die Hypothek war eine Sorge, aber wir konnten die Raten weiter zahlen.",
    ],

    # ---- Age-driven themes ----
    "young_precarity": [
        "Ich war damals Studentin und mein Nebenjob ist von einem Tag auf den anderen weggefallen.",
        "Praktika wurden abgesagt, das hat den Berufseinstieg wirklich verzögert.",
        "Online-Vorlesungen waren erschöpfend und nicht das, wofür ich mich eingeschrieben hatte.",
        "Ich bin wieder zu meinen Eltern gezogen, weil ich die Miete allein nicht stemmen konnte.",
        "Bewerbungsgespräche per Video fühlten sich seltsam an, es war schwer, einen Bezug aufzubauen.",
        "Viele meiner Freunde saßen im selben Boot, all unsere Pläne wurden verschoben.",
        "Ich hatte das Gefühl, dass meine ersten Berufsjahre durch die Pandemie gestohlen wurden.",
        "Examensfeiern, Partys, alle Meilensteine waren einfach weg.",
    ],
    "middle_parenting": [
        "Mit den Kindern im Homeoffice zu arbeiten war jeden Tag eine enorme Herausforderung.",
        "Die Schulschließungen haben uns gezwungen, Hausunterricht zu machen und gleichzeitig zu arbeiten.",
        "Die Kinder haben ihre Freunde schrecklich vermisst, das hat mir das Herz gebrochen.",
        "Geschlossene Kitas bedeuteten, dass wir Meetings und Kleinkinder den ganzen Tag jonglierten.",
        "Mein Partner und ich mussten den Tag in Schichten aufteilen, um die Kinder zu betreuen.",
        "Bei Hausaufgaben zu helfen und nebenbei zu arbeiten war völlig erschöpfend.",
        "Wir haben für jedes Kind ein Tablet gekauft, damit sie am Online-Unterricht teilnehmen konnten.",
        "Die mentale Last der Haushaltsorganisation ist während des Lockdowns explodiert.",
    ],
    "older_career_stress": [
        "In meinem Alter war die Aussicht, den Job zu verlieren und einen neuen zu suchen, beängstigend.",
        "Ich hatte Sorge, dass Altersdiskriminierung eine Jobsuche unmöglich machen würde.",
        "Meine Eltern waren alt und ich lebte in der Angst, ihnen das Virus mitzubringen.",
        "Die Umstellung auf Heimarbeit war in meinem Alter schwierig, die Technik war neu.",
        "Umstrukturierungen in meiner Firma setzten ältere Beschäftigte besonders unter Druck.",
        "Ich musste viele neue digitale Werkzeuge schneller lernen, als mir lieb war.",
    ],
    "elder_isolation": [
        "Mir wurde aufgrund meines Alters und meiner Gesundheit empfohlen, monatelang zu Hause zu bleiben.",
        "Ich habe wochenlang niemanden persönlich gesehen, nur Stimmen am Telefon.",
        "Meine Enkelkinder haben mich durchs Fenster oder per Videoanruf besucht.",
        "Der Tag des Impftermins war eine echte Erleichterung, fast eine Feier.",
        "Ich habe einen Freund an das Virus verloren und konnte nicht richtig zur Beerdigung gehen.",
        "Die Isolation war schwerer als die Angst vor der Krankheit selbst.",
        "Familien-Videoanrufe wurden zum Höhepunkt meiner Woche.",
        "Ich fühlte mich in diesen langen ruhigen Monaten von der Welt vergessen.",
    ],

    # ---- Gender-leaning themes ----
    "domestic_load": [
        "Der Großteil der Hausarbeit blieb an mir hängen, obwohl wir beide zu Hause waren.",
        "Ich habe ständig gekocht, die Familie hat monatelang jede Mahlzeit zu Hause gegessen.",
        "Mir ist aufgefallen, dass ich die Vorräte, Medikamente und Termine im Kopf hatte.",
        "Die emotionale Unterstützung für die ganze Familie wurde zu meiner unausgesprochenen Aufgabe.",
        "Kinderbetreuung und Haushaltsaufgaben zusammen ließen mir keine Zeit für mich selbst.",
    ],
    "remote_work_technical": [
        "Das Heimbüro einzurichten, das VPN, die zwei Bildschirme, das war einiges an Arbeit.",
        "Ich musste lernen, Meetings per Video zu leiten, das hat meinen Führungsstil verändert.",
        "Die Produktivität hat sich tatsächlich verbessert ohne Pendeln und Büroablenkungen.",
        "Die Koordination von Projekten über verteilte Teams hinweg war eine echte Umstellung.",
        "Ich habe meinen Arbeitsablauf um asynchrone Kommunikationstools herum neu gestaltet.",
    ],

    # ---- Universal Covid themes ----
    "masks_distancing": [
        "Eine Maske zu tragen wurde nach ein paar Wochen zur zweiten Natur.",
        "Den körperlichen Abstand von Menschen einzuhalten fühlte sich anfangs seltsam und unnatürlich an.",
        "Ich trage in vollen Räumen manchmal noch eine Maske, aus Gewohnheit.",
        "Die Maskendebatten in den Medien waren erschöpfend zu verfolgen.",
        "Ich hatte gemischte Gefühle, was die Maskenpflicht für Kinder in den Schulen anging.",
    ],
    "vaccination": [
        "Ich habe mich impfen lassen, sobald ich konnte, das gab mir echte Sicherheit.",
        "Ich habe ein paar Wochen gewartet, um zu sehen, wie die Impfstoffe wirken, bevor ich meine bekam.",
        "Der Impfprozess war bei uns gut organisiert, sehr effizient.",
        "Ich hatte einen wunden Arm und Müdigkeit für einen Tag, aber nichts Schlimmeres.",
        "Boosterimpfungen wurden Teil der Routine, fast wie eine jährliche Gewohnheit.",
        "Einige in meinem Umfeld waren skeptisch, wir hatten viele lange Gespräche.",
    ],
    "health_worry": [
        "Ich hatte ständig Angst, das Virus zu bekommen und schwer zu erkranken.",
        "Jedes Mal, wenn jemand in der Familie hustete, kam die Angst zurück.",
        "Ich habe begonnen, viel mehr auf meine allgemeine Gesundheit und Immunabwehr zu achten.",
        "Jemanden auf der Intensivstation zu kennen hat die Bedrohung wirklich greifbar gemacht.",
        "Die täglichen Fallzahlen zu lesen wurde eine Weile zu einer ungesunden Obsession.",
    ],
    "digital_tools": [
        "Videoanrufe haben monatelang fast jede persönliche Interaktion ersetzt.",
        "Online-Einkäufe wurden zu einer Gewohnheit, die ich seitdem beibehalten habe.",
        "Ich habe an virtuellen sozialen Veranstaltungen teilgenommen, das fühlte sich seltsam an, war aber besser als nichts.",
        "Streamingdienste haben uns durch die langen Abende drinnen unterhalten.",
        "Ich habe E-Mails und Telefonate wiederentdeckt, nach Jahren, in denen ich nur Nachrichten geschrieben habe.",
    ],
    "social_relations": [
        "Ich habe gelernt, wer meine echten Freunde sind, als wir uns nicht persönlich treffen konnten.",
        "Manche Beziehungen sind vertieft worden, andere sind in den langen Monaten still verblasst.",
        "Spaziergänge im Freien mit einer Person nach der anderen wurden zu kostbaren Momenten.",
        "Ich habe gemerkt, dass ich weniger, aber bedeutungsvollere Kontakte in dieser Zeit hatte.",
        "Sich nach den Lockerungen wieder mit Leuten zu verbinden war manchmal merkwürdig.",
    ],
    "policy_views": [
        "Ich empfand die Einschränkungen unter den Umständen im Großen und Ganzen als angemessen.",
        "Manche Regeln wirkten unstimmig, und das hat das öffentliche Vertrauen untergraben.",
        "Ich denke, die Regierungen haben viel gelernt, aber am Anfang schlecht kommuniziert.",
        "Im Nachhinein hätte die Reaktion schneller und besser koordiniert sein können.",
        "Ich habe den Gesundheitsbehörden vertraut, auch wenn sich ihre Empfehlungen änderten.",
    ],
    "looking_back": [
        "Ich glaube, die Pandemie hat uns gezwungen, neu zu überdenken, was im Leben wirklich zählt.",
        "Manche Dinge haben sich dauerhaft verändert, wie wir Arbeit sehen und wo wir leben.",
        "Ich schätze kleine alltägliche Freiheiten viel mehr als früher.",
        "Die Gesellschaft erwies sich als fragiler, als ich dachte, aber auch als widerstandsfähiger.",
        "Die psychischen Folgen sind, glaube ich, auch heute noch bei uns.",
    ],
}


# =============================================================================
# PROFILE → THEME WEIGHTS  (identical to the English version, on purpose)
# =============================================================================

GENDER_WEIGHTS = {
    "F": {
        "domestic_load":         2.5,
        "remote_work_technical": 0.5,
        "health_worry":          1.3,
        "social_relations":      1.2,
    },
    "M": {
        "domestic_load":         0.4,
        "remote_work_technical": 2.2,
        "policy_views":          1.3,
    },
}

AGE_WEIGHTS = {
    "18-29": {
        "young_precarity":    3.0,
        "middle_parenting":   0.1,
        "older_career_stress": 0.1,
        "elder_isolation":    0.1,
        "digital_tools":      1.5,
        "social_relations":   1.4,
    },
    "30-44": {
        "young_precarity":    0.2,
        "middle_parenting":   2.8,
        "older_career_stress": 0.5,
        "elder_isolation":    0.1,
        "remote_work_technical": 1.4,
    },
    "45-59": {
        "young_precarity":    0.1,
        "middle_parenting":   0.7,
        "older_career_stress": 2.5,
        "elder_isolation":    0.4,
    },
    "60+": {
        "young_precarity":    0.1,
        "middle_parenting":   0.1,
        "older_career_stress": 0.5,
        "elder_isolation":    3.0,
        "vaccination":        1.6,
        "health_worry":       1.5,
    },
}

INCOME_WEIGHTS = {
    "low": {
        "financial_struggle":  3.5,
        "financial_comfort":   0.05,
        "middle_finances":     0.3,
    },
    "mid": {
        "financial_struggle":  0.4,
        "financial_comfort":   0.3,
        "middle_finances":     2.5,
    },
    "high": {
        "financial_struggle":  0.05,
        "financial_comfort":   3.5,
        "middle_finances":     0.3,
    },
}


# =============================================================================
# COMPOSITION
# =============================================================================

def compute_theme_weights(gender: str, age: str, income: str) -> dict:
    weights = {theme: 1.0 for theme in SENTENCES.keys()}
    for src in (GENDER_WEIGHTS[gender], AGE_WEIGHTS[age], INCOME_WEIGHTS[income]):
        for theme, w in src.items():
            weights[theme] *= w
    return weights


def pick_sentence(rng: random.Random, theme_weights: dict) -> str:
    themes = list(theme_weights.keys())
    weights = [theme_weights[t] for t in themes]
    theme = rng.choices(themes, weights=weights, k=1)[0]
    return rng.choice(SENTENCES[theme])


def make_interview(gender: str, age: str, income: str,
                   rng: random.Random,
                   n_questions: int = 7) -> str:
    weights = compute_theme_weights(gender, age, income)
    questions = rng.sample(QUESTIONS, n_questions)
    lines = []
    for q in questions:
        lines.append(f"F: {q}")  # 'F' = Frage (Q in German)
        n_sent = rng.randint(2, 4)
        answer_parts = [pick_sentence(rng, weights) for _ in range(n_sent)]
        lines.append("A: " + " ".join(answer_parts))  # 'A' = Antwort
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def make_profile_distribution(rng: random.Random) -> list:
    """Same target distribution as the English corpus, for parallelism."""
    profiles = []
    gender_pool = ["F"] * 28 + ["M"] * 22
    age_pool = ["18-29"] * 12 + ["30-44"] * 18 + ["45-59"] * 12 + ["60+"] * 8
    income_pool = ["low"] * 18 + ["mid"] * 19 + ["high"] * 13

    rng.shuffle(gender_pool)
    rng.shuffle(age_pool)
    rng.shuffle(income_pool)

    for g, a, i in zip(gender_pool, age_pool, income_pool):
        profiles.append((g, a, i))
    return profiles


def main():
    parser = argparse.ArgumentParser(
        description="Generate a synthetic German Covid interview corpus.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str,
                        default="test_interviews_covid_de")
    parser.add_argument("--n-interviews", type=int, default=50)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles = make_profile_distribution(rng)[:args.n_interviews]

    csv_rows = []
    for idx, (gender, age, income) in enumerate(profiles, start=1):
        fname = f"interview_{gender}_{age}_{income}_{idx:03d}.txt"
        text = make_interview(gender, age, income, rng)
        (out_dir / fname).write_text(text, encoding="utf-8")
        csv_rows.append({
            "filename": fname,
            "gender":   gender,
            "age":      age,
            "income":   income,
        })

    csv_path = out_dir / "interviews_metadata.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "gender",
                                                "age", "income"])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"✓ Generated {len(csv_rows)} German interviews in "
          f"{out_dir.resolve()}")
    print(f"  Seed used: {args.seed}")
    from collections import Counter
    print(f"  Gender: {dict(Counter(p[0] for p in profiles))}")
    print(f"  Age:    {dict(Counter(p[1] for p in profiles))}")
    print(f"  Income: {dict(Counter(p[2] for p in profiles))}")


if __name__ == "__main__":
    main()
