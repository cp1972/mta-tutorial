#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_test_articles_de.py
========================

Generate a synthetic GERMAN corpus contrasting JOURNALISTIC vs.
SCIENTIFIC articles across four domains (medicine, sociology, climate,
economy). 50 articles, continuous prose.

USAGE
-----
    python make_test_articles_de.py [--seed SEED] [--output DIR]

DESIGN
------
Each article = an opening sentence + several body sentences + a
closing sentence, drawn from STYLE pools (journalistic vs scientific)
and DOMAIN pools (medicine, sociology, climate, economy).

The style pool determines:
- Sentence length and rhythm
- Vocabulary register (everyday vs technical)
- Discourse markers ("gestern" vs "die Studie zeigt")
- Structure (anecdote / citation / question vs hypothesis / method / result)

The domain pool adds topic-specific vocabulary.

Distinguishing journalistic from scientific writing should be very
EASY for MTA (the style markers differ strongly). Distinguishing
domains within a style should be more SUBTLE.
"""

import argparse
import csv
import random
from pathlib import Path

# =============================================================================
# STYLE: JOURNALISTIC — short sentences, anecdotal, present tense, citations
# =============================================================================

JOURNALISTIC_OPENERS = [
    "Gestern wurde bekannt, dass {topic_phrase}.",
    "Eine neue Welle der Diskussion erfasst {domain_field}.",
    "Was viele nicht wissen: {topic_phrase}.",
    "Diese Woche steht {domain_field} im Mittelpunkt der Debatte.",
    "Ein überraschender Befund sorgt für Aufsehen in {domain_field}.",
    "Es war ein normaler Tag, bis die Nachricht eintraf: {topic_phrase}.",
    "Wer hätte das gedacht? {topic_phrase}.",
    "Eine Begegnung am Rande einer Konferenz brachte es ans Licht: {topic_phrase}.",
]

JOURNALISTIC_BODY = [
    "Die Reaktionen sind heftig, von Befürwortern wie Kritikern.",
    "Eine Mutter aus Halle erzählt von ihrer eigenen Erfahrung mit der Sache.",
    "Im Gespräch mit unserer Redaktion betont die Expertin: «Das ist ein klares Signal.»",
    "Hinter den Kulissen brodelt es seit Monaten.",
    "Manche sprechen schon von einer Zeitenwende.",
    "Die Zahlen sind alarmierend, sagen die einen, übertrieben, die anderen.",
    "Auf der Straße hört man unterschiedliche Stimmen zum Thema.",
    "Der Politik bleibt jetzt nicht mehr viel Zeit zum Handeln.",
    "Was bedeutet das für uns alle im Alltag?",
    "Ein Blick in die Nachbarländer zeigt: dort läuft es anders.",
    "Die Frage ist nicht ob, sondern wann sich etwas ändert.",
    "Eltern, Kinder, Senioren — alle sind betroffen.",
    "Es geht um Vertrauen, um Verantwortung, um Mut.",
    "Die Bilder gingen um die Welt und lösten eine Welle der Solidarität aus.",
    "Manche Stimmen warnen vor übereilten Schlussfolgerungen.",
]

JOURNALISTIC_CLOSERS = [
    "Eines ist klar: Die Geschichte ist noch lange nicht zu Ende.",
    "Wir bleiben dran und werden weiter berichten.",
    "Was meinen Sie dazu? Schreiben Sie uns.",
    "Die nächsten Wochen werden entscheidend sein.",
    "Vielleicht ist es Zeit, neu nachzudenken.",
    "Und wer trägt am Ende die Konsequenzen?",
]

# =============================================================================
# STYLE: SCIENTIFIC — long sentences, technical, hypothesis-driven, neutral
# =============================================================================

SCIENTIFIC_OPENERS = [
    "Die vorliegende Untersuchung befasst sich mit der Frage, inwiefern {topic_phrase}.",
    "Im Rahmen der hier vorgestellten Studie wurde überprüft, ob {topic_phrase}.",
    "Ausgangspunkt der folgenden Analyse ist die Beobachtung, dass {topic_phrase}.",
    "Ziel des vorliegenden Beitrags ist es, theoretisch und empirisch zu klären, ob {topic_phrase}.",
    "Die methodische Herangehensweise dieser Arbeit gründet auf der Annahme, dass {topic_phrase}.",
    "In der Fachliteratur wird zunehmend diskutiert, ob {topic_phrase}.",
    "Vor dem Hintergrund aktueller theoretischer Debatten lässt sich festhalten, dass {topic_phrase}.",
    "Die folgende Argumentation knüpft an bestehende Forschungsergebnisse an, wonach {topic_phrase}.",
]

SCIENTIFIC_BODY = [
    "Die statistische Auswertung der erhobenen Daten zeigt einen signifikanten Zusammenhang zwischen den untersuchten Variablen.",
    "Im Folgenden werden die theoretischen Grundlagen kurz dargelegt und anschließend operationalisiert.",
    "Die empirische Datenbasis besteht aus einer Stichprobe von 1247 Fällen, die mittels geschichteter Zufallsauswahl gewonnen wurden.",
    "Aus methodologischer Perspektive ist anzumerken, dass die Reliabilität der eingesetzten Skalen zufriedenstellend ist.",
    "Die Ergebnisse der multivariaten Regression deuten auf eine substanzielle Effektstärke hin.",
    "Es lässt sich theoretisch ableiten, dass die beobachteten Muster nicht zufällig sind.",
    "Eine kritische Reflexion der Befunde im Lichte der Literatur erscheint angebracht.",
    "Die hier vorgestellte Hypothese steht im Einklang mit den Ergebnissen früherer Untersuchungen.",
    "Methodologische Limitationen, insbesondere hinsichtlich der Generalisierbarkeit, sind zu berücksichtigen.",
    "Im interdisziplinären Diskurs wird diese Position vor allem von Forschenden aus dem strukturalistischen Lager vertreten.",
    "Die Operationalisierung der zentralen Konzepte erfolgte über validierte Messinstrumente.",
    "Eine differenzierte Betrachtung der intervenierenden Variablen ist für die Interpretation unerlässlich.",
    "Konfundierende Faktoren wurden durch geeignete statistische Kontrollen berücksichtigt.",
    "Die theoretische Einordnung der Befunde verweist auf einen Paradigmenwechsel in der jüngeren Forschung.",
    "Aus diesen Befunden ergeben sich weiterführende Forschungsfragen, die in einer Folgestudie zu adressieren wären.",
]

SCIENTIFIC_CLOSERS = [
    "Die vorliegende Analyse leistet einen Beitrag zur weiterführenden theoretischen Diskussion.",
    "Weiterführende empirische Untersuchungen erscheinen geboten.",
    "Die Generalisierbarkeit der Ergebnisse auf andere Populationen bedarf zusätzlicher Forschung.",
    "Insgesamt bestätigen die Befunde die eingangs formulierte Hypothese.",
    "Diese Ergebnisse erweitern den bestehenden Forschungsstand in mehrfacher Hinsicht.",
    "Eine Replikationsstudie in einem anderen kulturellen Kontext wäre wünschenswert.",
]

# =============================================================================
# DOMAIN POOLS — domain-specific topic phrases and vocabulary
# =============================================================================

DOMAIN_TOPIC_PHRASES = {
    "medicine": [
        "neue Therapieansätze die Behandlung von Diabetes grundlegend verändern könnten",
        "die Zahl der Krankenhausaufenthalte aufgrund von Atemwegserkrankungen steigt",
        "ein neuer Impfstoff vielversprechende Resultate in klinischen Studien zeigt",
        "die Versorgungslage in ländlichen Regionen sich weiter verschlechtert",
        "die Lebenserwartung in bestimmten Bevölkerungsgruppen stagniert",
    ],
    "sociology": [
        "soziale Ungleichheit sich entlang neuer Bruchlinien verschärft",
        "Bildungschancen weiterhin stark vom Elternhaus abhängen",
        "die soziale Mobilität in Deutschland zurückgeht",
        "städtische und ländliche Lebenswelten zunehmend auseinanderdriften",
        "die Pluralisierung von Lebensformen die Familiensoziologie herausfordert",
    ],
    "climate": [
        "die Treibhausgasemissionen erneut neue Höchststände erreichen",
        "der Meeresspiegel schneller ansteigt als bisher angenommen",
        "die Häufigkeit extremer Wetterereignisse in Mitteleuropa zunimmt",
        "die Energiewende neue ökonomische Verteilungsfragen aufwirft",
        "die Biodiversität in Agrarlandschaften dramatisch abnimmt",
    ],
    "economy": [
        "die Inflation weiterhin die Kaufkraft der Mittelschicht belastet",
        "die Lieferketten globaler Märkte fragiler geworden sind",
        "die Digitalisierung bestimmte Branchen tiefgreifend transformiert",
        "die Vermögenskonzentration in Deutschland weiter zunimmt",
        "der Arbeitsmarkt sich in Richtung prekärer Beschäftigung verschiebt",
    ],
}

DOMAIN_FIELDS = {
    "medicine":  "die medizinische Forschung",
    "sociology": "die soziologische Debatte",
    "climate":   "die Klimaforschung",
    "economy":   "die wirtschaftspolitische Diskussion",
}

DOMAIN_VOCAB_SENTENCES = {
    "medicine": [
        "Klinische Studien an mehreren Universitätskliniken belegen die Wirksamkeit.",
        "Die Patientensicherheit steht im Zentrum der ärztlichen Bewertung.",
        "Pharmazeutische Wirkstoffe werden zunehmend personalisiert eingesetzt.",
        "Die Symptome treten in der Regel innerhalb weniger Tage auf.",
        "Niedergelassene Ärzte berichten von einem deutlichen Anstieg der Fallzahlen.",
    ],
    "sociology": [
        "Gesellschaftliche Klassenlagen prägen Lebensentwürfe nachhaltig.",
        "Die Habitusforschung im Anschluss an Bourdieu liefert Erklärungsansätze.",
        "Soziale Ungleichheit reproduziert sich über Generationen hinweg.",
        "Milieuspezifische Praktiken strukturieren den Alltag.",
        "Die kulturelle Kapitalausstattung beeinflusst Bildungswege.",
    ],
    "climate": [
        "Modelle des IPCC prognostizieren weitere Temperaturanstiege.",
        "Der Kohlenstoffhaushalt der Atmosphäre verschiebt sich weiter.",
        "Erneuerbare Energien verzeichnen einen rasanten Ausbau.",
        "Permafrostböden tauen mit besorgniserregender Geschwindigkeit.",
        "Klimaadaptionsstrategien werden auf kommunaler Ebene erprobt.",
    ],
    "economy": [
        "Die EZB hält an ihrer aktuellen Zinspolitik vorerst fest.",
        "Konjunkturindikatoren signalisieren eine vorsichtige Erholung.",
        "Unternehmensinvestitionen bleiben hinter den Erwartungen zurück.",
        "Der Konsum der privaten Haushalte stagniert auf niedrigem Niveau.",
        "Steuerpolitische Maßnahmen sollen Anreize für Investitionen schaffen.",
    ],
}

# =============================================================================
# COMPOSITION
# =============================================================================

def make_article(style: str, domain: str, rng: random.Random) -> str:
    """Compose one article from style + domain pools."""
    topic = rng.choice(DOMAIN_TOPIC_PHRASES[domain])
    field = DOMAIN_FIELDS[domain]

    if style == "journalistic":
        opener = rng.choice(JOURNALISTIC_OPENERS).format(
            topic_phrase=topic, domain_field=field
        )
        # Mix: more style-body, plus some domain vocab
        n_body = rng.randint(5, 7)
        body_pool = JOURNALISTIC_BODY * 2 + DOMAIN_VOCAB_SENTENCES[domain]
        body = rng.sample(body_pool, n_body)
        closer = rng.choice(JOURNALISTIC_CLOSERS)
    else:  # scientific
        opener = rng.choice(SCIENTIFIC_OPENERS).format(
            topic_phrase=topic, domain_field=field
        )
        n_body = rng.randint(5, 7)
        body_pool = SCIENTIFIC_BODY * 2 + DOMAIN_VOCAB_SENTENCES[domain]
        body = rng.sample(body_pool, n_body)
        closer = rng.choice(SCIENTIFIC_CLOSERS)

    paragraph = " ".join([opener] + body + [closer])
    return paragraph + "\n"


def make_profile_distribution(rng: random.Random) -> list:
    """25 journalistic + 25 scientific, ~12-13 per domain."""
    profiles = []
    # 50 total: 25 journalistic / 25 scientific
    # 4 domains: 13/12/13/12 across (medicine/sociology/climate/economy)
    domains = (
        ["medicine"] * 13 + ["sociology"] * 12
        + ["climate"] * 13 + ["economy"] * 12
    )
    styles = ["journalistic"] * 25 + ["scientific"] * 25

    rng.shuffle(domains)
    rng.shuffle(styles)
    for s, d in zip(styles, domains):
        profiles.append((s, d))
    return profiles


def main():
    parser = argparse.ArgumentParser(
        description="Generate a German journalistic vs scientific articles corpus.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str,
                        default="test_articles_journ_sci_de")
    parser.add_argument("--n-articles", type=int, default=50)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles = make_profile_distribution(rng)[:args.n_articles]

    csv_rows = []
    for idx, (style, domain) in enumerate(profiles, start=1):
        # Use shorter codes in the filename: journ/sci, med/soc/cli/eco
        style_short = "journ" if style == "journalistic" else "sci"
        domain_short = {"medicine": "med", "sociology": "soc",
                        "climate": "cli", "economy": "eco"}[domain]
        fname = f"article_{style_short}_{domain_short}_{idx:03d}.txt"
        text = make_article(style, domain, rng)
        (out_dir / fname).write_text(text, encoding="utf-8")
        csv_rows.append({
            "filename": fname,
            "style":    style,
            "domain":   domain,
        })

    csv_path = out_dir / "articles_metadata.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "style", "domain"])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"✓ Generated {len(csv_rows)} German articles in "
          f"{out_dir.resolve()}")
    print(f"  Seed used: {args.seed}")
    from collections import Counter
    print(f"  Style:  {dict(Counter(p[0] for p in profiles))}")
    print(f"  Domain: {dict(Counter(p[1] for p in profiles))}")


if __name__ == "__main__":
    main()
