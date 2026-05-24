#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_test_human_ai_de.py
=========================

Generate 50 synthetic German short texts contrasting HUMAN-style
writing (with hesitations, anecdotes, asymmetry) vs AI-style writing
(formal, balanced lists, metadiscourse).

USAGE
-----
    python make_test_human_ai_de.py [--seed SEED] [--output DIR]

CRITICAL PEDAGOGICAL CAVEAT
---------------------------
This corpus is DESIGNED to be distinguished. The 'human' texts deliberately
include markers of spontaneity (filler words, contradictions, idiosyncratic
phrasing). The 'AI' texts deliberately include markers commonly associated
with default-mode LLM writing (formal openers, balanced structures,
metadiscourse, concluding summaries).

What MTA detects is therefore NOT 'AI in general' but 'a certain stylistic
default of formal LLM writing'. A human writing formally, or an AI
prompted to mimic oral speech, could pass under the radar in BOTH directions.

This corpus is a teaching tool to show that topic modeling can detect
stylistic register differences — it is NOT an AI detector.
"""

import argparse
import csv
import random
from pathlib import Path

# ============================================================
# HUMAN-STYLE POOLS — spontaneous, asymmetric, anecdotal
# ============================================================

HUMAN_OPENERS = [
    "Also, ich weiß ja nicht, was die anderen denken, aber ich finde",
    "Naja, das ist eine schwierige Frage, ehrlich gesagt",
    "Ach, dazu fällt mir spontan ein, dass",
    "Hm, lass mich mal überlegen",
    "Ja gut, also wenn ich ehrlich bin",
    "Weißt du was, ich hab da letztens drüber nachgedacht",
    "Mensch, das ist ja ein Thema",
    "Ich erinner mich da an eine Geschichte, das war damals",
]

HUMAN_BODY = [
    "Ich mein, das ist halt so eine Sache, die kann man nicht in einem Satz sagen.",
    "Mein Nachbar zum Beispiel, der sagt immer was anderes, aber gut, das ist sein Ding.",
    "Manchmal denk ich mir, ach, lass es einfach, und dann mach ich's doch.",
    "Ich versteh's selber nicht so ganz, ehrlich gesagt.",
    "Das ist so komisch, weil eigentlich müsste es ja anders sein, aber irgendwie.",
    "Und dann ist mir aufgefallen, also so richtig aufgefallen erst hinterher.",
    "Aber wie soll ich sagen, das ändert ja auch nichts dran.",
    "Ich mein, jeder hat ja seine eigene Sicht, ne, das ist nichts Neues.",
    "Sowas erlebt man nicht jeden Tag, ich kann dir sagen.",
    "Da würd ich jetzt nicht zu viel reininterpretieren, ehrlich.",
    "Bin mir nicht sicher, ob das stimmt, was ich da gerade sage.",
    "Vielleicht klingt das jetzt blöd, aber für mich ist das so.",
    "Wie war das nochmal? Ach ja, jetzt fällt's mir wieder ein.",
    "Tja, was soll man da machen, da kannste nichts machen.",
    "Ich kenne jemand, der hat genau das Gegenteil erlebt, find ich krass.",
]

HUMAN_CLOSERS = [
    "Aber ich hör jetzt mal auf, sonst rede ich mich noch um Kopf und Kragen.",
    "Ja, das war's auch schon, mehr fällt mir grad nicht ein.",
    "Egal, ich glaub, du verstehst, was ich meine.",
    "Naja, jeder muss das für sich selber wissen, denk ich.",
    "Ach komm, jetzt hab ich genug geredet.",
]

# ============================================================
# AI-STYLE POOLS — formal, balanced, metadiscourse-heavy
# ============================================================

AI_OPENERS = [
    "Diese Frage berührt mehrere wichtige Aspekte, die es zu betrachten gilt.",
    "Es ist wichtig zu betonen, dass es hierzu verschiedene Perspektiven gibt.",
    "Diese komplexe Thematik lässt sich aus verschiedenen Blickwinkeln betrachten.",
    "Bei der Beantwortung dieser Frage müssen wir verschiedene Faktoren berücksichtigen.",
    "Es gibt mehrere Schlüsselaspekte, die in Bezug auf diese Frage relevant sind.",
    "Lassen Sie uns diese vielschichtige Angelegenheit systematisch betrachten.",
    "Im Folgenden werde ich die wichtigsten Punkte zu diesem Thema darlegen.",
    "Diese Fragestellung erfordert eine differenzierte und ausgewogene Betrachtung.",
]

AI_BODY = [
    "Einerseits ist anzumerken, dass diese Position durchaus ihre Berechtigung hat.",
    "Andererseits sollten wir auch die Gegenargumente sorgfältig prüfen.",
    "Es ist jedoch wichtig zu beachten, dass die Situation kontextabhängig ist.",
    "Erstens muss berücksichtigt werden, dass mehrere Faktoren zusammenwirken.",
    "Zweitens spielt der historische und kulturelle Kontext eine entscheidende Rolle.",
    "Drittens darf die individuelle Perspektive nicht vernachlässigt werden.",
    "Es lässt sich grundsätzlich festhalten, dass eine eindeutige Antwort schwierig ist.",
    "Diese Überlegungen führen uns zu einer ausgewogenen Bewertung der Sachlage.",
    "Es ist sowohl die positive als auch die negative Seite zu berücksichtigen.",
    "Eine sorgfältige Abwägung der verschiedenen Standpunkte ist hier unerlässlich.",
    "Aus dieser Perspektive heraus erscheint eine differenzierte Bewertung geboten.",
    "Hierbei gilt es, sowohl kurzfristige als auch langfristige Aspekte zu beachten.",
    "Wichtig erscheint mir der Hinweis, dass es keine universell gültige Antwort gibt.",
    "Es handelt sich um ein vielschichtiges Thema mit mehreren Dimensionen.",
    "Festzuhalten bleibt, dass eine ganzheitliche Betrachtungsweise erforderlich ist.",
]

AI_CLOSERS = [
    "Zusammenfassend lässt sich sagen, dass eine ausgewogene Perspektive entscheidend ist.",
    "Abschließend möchte ich betonen, dass dies eine sehr persönliche Entscheidung ist.",
    "Es ist hoffentlich deutlich geworden, dass die Antwort vielschichtig ausfällt.",
    "Letztendlich hängt die Bewertung von den individuellen Werten und Prioritäten ab.",
    "Ich hoffe, diese Ausführungen konnten zur Klärung der Frage beitragen.",
]


def make_text(style: str, rng: random.Random) -> str:
    if style == "human":
        opener_pool, body_pool, closer_pool = (
            HUMAN_OPENERS, HUMAN_BODY, HUMAN_CLOSERS
        )
    else:
        opener_pool, body_pool, closer_pool = (
            AI_OPENERS, AI_BODY, AI_CLOSERS
        )
    n_body = rng.randint(4, 6)
    sentences = ([rng.choice(opener_pool)]
                 + rng.sample(body_pool, n_body)
                 + [rng.choice(closer_pool)])
    # Human texts often join with ", " or just space, AI is more formal
    if style == "human":
        # Add some run-on quality
        return " ".join(sentences) + "\n"
    else:
        return " ".join(sentences) + "\n"


def make_profile_distribution(rng: random.Random) -> list:
    """25 human, 25 AI-style."""
    profiles = ["human"] * 25 + ["ai"] * 25
    rng.shuffle(profiles)
    return profiles


def main():
    parser = argparse.ArgumentParser(
        description="Generate German human vs AI text corpus (synthetic).",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str,
                        default="test_human_ai_de")
    parser.add_argument("--n-texts", type=int, default=50)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles = make_profile_distribution(rng)[:args.n_texts]
    csv_rows = []
    for idx, style in enumerate(profiles, start=1):
        fname = f"text_{style}_{idx:03d}.txt"
        text = make_text(style, rng)
        (out_dir / fname).write_text(text, encoding="utf-8")
        csv_rows.append({"filename": fname, "style": style})

    csv_path = out_dir / "texts_metadata.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "style"])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"✓ Generated {len(csv_rows)} German human-vs-AI texts in "
          f"{out_dir.resolve()}")
    print(f"  Seed used: {args.seed}")
    from collections import Counter
    print(f"  Style: {dict(Counter(profiles))}")
    print("")
    print("  ⚠  PEDAGOGICAL CAVEAT: see README_test_dataset.md.")
    print("     This corpus tests stylistic register differences,")
    print("     NOT a generalized 'AI detector'.")


if __name__ == "__main__":
    main()
