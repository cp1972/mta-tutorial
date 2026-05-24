#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_test_health_de.py
=======================

Generate 80 synthetic German testimonies about HEALTH representations,
crossed across four dimensions: location × gender × age × education.

USAGE
-----
    python make_test_health_de.py [--seed SEED] [--output DIR]

DESIGN
------
Each text is a short personal testimony on how the speaker thinks about
their health, their access to care, prevention habits, illness experience.

Profile dimensions encoded via CSV (file names too long otherwise):
- location:  urban / rural
- gender:    F / M
- age:       young (25-44) / mid (45-64) / old (65+)
- education: low / mid / high

48 theoretical cells for 80 texts → ~1.7 per cell on average; some cells
empty. Sociological tests are run per DIMENSION (one at a time via CSV),
not on the full cross-classification.

Expected differentiation:
- NET on education      (medical vocabulary differs strongly by educational level)
- MODERATE on location  (urban access, rural shortages)
- MODERATE on age       (different concerns by life stage)
- SUBTLE on gender      (some differences in body talk, prevention)
"""

import argparse
import csv
import random
from pathlib import Path

# ===== EDUCATION-DRIVEN POOLS (the strongest signal) =====
EDUCATION_POOLS = {
    "low": [
        "Ich gehe halt zum Arzt, wenn was weh tut, das war's eigentlich.",
        "So genau will ich das gar nicht wissen, was die Ärzte da sagen.",
        "Tabletten nehmen, abwarten, weitermachen, anders geht's nicht.",
        "Vorsorge, das ist nichts für unsereins, das ist was für die anderen.",
        "Mein Hausarzt kennt mich, dem vertrau ich, der weiß schon, was er macht.",
        "Krankheit gehört zum Leben, da kann man nichts machen.",
        "Ich versteh die ganzen Fremdwörter nicht, die die Ärzte benutzen.",
        "Wenn ich krank bin, dann arbeite ich halt trotzdem, irgendwie geht das schon.",
    ],
    "mid": [
        "Ich versuche, regelmäßig zur Vorsorge zu gehen, auch wenn ich keine Beschwerden habe.",
        "Eine ausgewogene Ernährung und Bewegung sind mir wichtig im Alltag.",
        "Manchmal hole ich eine Zweitmeinung ein, gerade bei größeren Entscheidungen.",
        "Ich informiere mich im Internet, aber mit Vorsicht, da steht ja viel Unsinn.",
        "Mein Hausarzt überweist mich an einen Facharzt, wenn das nötig ist.",
        "Ich nehme an den empfohlenen Früherkennungsuntersuchungen teil.",
        "Gesundheit ist ein Gut, das man pflegen muss, das habe ich gelernt.",
        "Eine gute Krankenversicherung gibt mir Sicherheit für den Notfall.",
    ],
    "high": [
        "Ich verfolge die epidemiologischen Studien zur Prävention von Herz-Kreislauf-Erkrankungen.",
        "Die evidenzbasierte Medizin sollte die Grundlage jeder therapeutischen Entscheidung sein.",
        "Soziale Determinanten von Gesundheit beeinflussen meine Sichtweise erheblich.",
        "Ich konsultiere wissenschaftliche Reviews, bevor ich Behandlungsoptionen abwäge.",
        "Die Ungleichverteilung von Gesundheitschancen ist sozialpolitisch ein Skandal.",
        "Prävention ist langfristig kosteneffizienter als Reaktion auf bereits manifeste Krankheit.",
        "Ich diskutiere meine Befunde mit dem Arzt auf Augenhöhe und stelle gezielte Rückfragen.",
        "Lebensstil, Genetik und Umwelt interagieren komplex bei der Krankheitsentstehung.",
    ],
}

# ===== LOCATION-DRIVEN POOLS =====
LOCATION_POOLS = {
    "urban": [
        "In der Stadt habe ich mehrere Fachärzte im Umkreis von zwei Kilometern.",
        "Wenn ich einen Termin brauche, kann ich zwischen mehreren Praxen wählen.",
        "Die Universitätsklinik ist nur eine Tramfahrt entfernt.",
        "Auch abends finde ich eine Notdienstapotheke in Laufweite.",
        "Die Vielfalt an Therapeuten hier in der Stadt ist erfreulich.",
    ],
    "rural": [
        "In unserem Dorf gibt es nur noch einen Hausarzt, und der geht bald in Rente.",
        "Für einen Facharzttermin muss ich vierzig Kilometer in die Kreisstadt fahren.",
        "Die nächste Notaufnahme ist fünfundzwanzig Autominuten entfernt.",
        "Die Versorgung auf dem Land wird immer schlechter, das spüren wir hier deutlich.",
        "Ohne Auto wäre der Zugang zu medizinischer Versorgung bei uns kaum möglich.",
    ],
}

# ===== AGE-DRIVEN POOLS =====
AGE_POOLS = {
    "young": [
        "In meinem Alter denkt man eigentlich noch nicht so viel über Krankheit nach.",
        "Sport, gesunde Ernährung, ausreichend Schlaf — das ist meine Strategie.",
        "Stress im Beruf ist für mich aktuell das größte Gesundheitsthema.",
        "Mental Health ist in meiner Generation viel präsenter als bei den Eltern.",
    ],
    "mid": [
        "Mit Mitte fünfzig merke ich, dass der Körper anders reagiert als früher.",
        "Erste chronische Themen tauchen auf, der Rücken, der Blutdruck.",
        "Ich achte jetzt bewusster auf die Werte beim Hausarzt als früher.",
        "Die Wechseljahre haben mein Verhältnis zum Körper verändert.",
    ],
    "old": [
        "Mit über siebzig gehört der Arztbesuch zum Rhythmus des Alltags.",
        "Ich nehme inzwischen mehrere Medikamente, das ist nicht zu vermeiden.",
        "Die Erinnerung an früher Verstorbene begleitet mich beim Nachdenken über Gesundheit.",
        "Selbstständig bleiben zu können ist für mich das wichtigste Gesundheitsziel.",
    ],
}

# ===== GENDER-LEANING POOLS (subtle) =====
GENDER_POOLS = {
    "F": [
        "Frauenheilkundliche Themen begleiten mich seit der Pubertät.",
        "Ich übernehme oft auch die Verantwortung für die Gesundheit meiner Angehörigen.",
        "Bei Symptomen werde ich von Ärzten manchmal weniger ernst genommen, finde ich.",
    ],
    "M": [
        "Männer gehen zu spät zum Arzt, das gilt leider auch für mich.",
        "Über Gesundheit sprechen Männer untereinander selten offen.",
        "Vorsorgeuntersuchungen für Männer kenne ich nur vage.",
    ],
}

# ===== UNIVERSAL HEALTH SENTENCES =====
UNIVERSAL = [
    "Gesundheit ist nicht alles, aber ohne Gesundheit ist alles nichts.",
    "Die Krankenkasse zahlt nicht alles, was ich für nötig halten würde.",
    "Manche Behandlungen müssen privat finanziert werden, das ist ein Thema.",
    "Die Pandemie hat mein Verhältnis zur Gesundheit verändert.",
]


def make_testimony(location, gender, age, education,
                   rng: random.Random) -> str:
    """Compose a health testimony, weighted toward the four profile pools."""
    parts = []
    # Education-driven: 3 sentences (strongest signal)
    parts.extend(rng.sample(EDUCATION_POOLS[education], 3))
    # Location: 1-2
    parts.extend(rng.sample(LOCATION_POOLS[location], rng.randint(1, 2)))
    # Age: 1-2
    parts.extend(rng.sample(AGE_POOLS[age], rng.randint(1, 2)))
    # Gender: 1
    parts.append(rng.choice(GENDER_POOLS[gender]))
    # Universal: 1
    parts.append(rng.choice(UNIVERSAL))
    rng.shuffle(parts)
    return " ".join(parts) + "\n"


def make_profile_distribution(rng: random.Random, n: int = 80) -> list:
    """Sample 80 profiles across the 4-dim space, slightly uneven."""
    profiles = []
    for _ in range(n):
        # Slightly biased sampling for realism
        location = rng.choices(["urban", "rural"], weights=[0.6, 0.4])[0]
        gender = rng.choices(["F", "M"], weights=[0.55, 0.45])[0]
        age = rng.choices(["young", "mid", "old"],
                          weights=[0.35, 0.40, 0.25])[0]
        education = rng.choices(["low", "mid", "high"],
                                weights=[0.30, 0.40, 0.30])[0]
        profiles.append((location, gender, age, education))
    return profiles


def main():
    parser = argparse.ArgumentParser(
        description="Generate German health testimony corpus.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str,
                        default="test_health_de")
    parser.add_argument("--n-texts", type=int, default=80)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles = make_profile_distribution(rng, n=args.n_texts)
    csv_rows = []
    # Filenames include all 4 dimensions for consistency with other corpora
    # Pattern: health_<location>_<gender>_<age>_<education>_<id>.txt
    for idx, (loc, gen, age, edu) in enumerate(profiles, start=1):
        fname = f"health_{loc}_{gen}_{age}_{edu}_{idx:03d}.txt"
        text = make_testimony(loc, gen, age, edu, rng)
        (out_dir / fname).write_text(text, encoding="utf-8")
        csv_rows.append({
            "filename":  fname,
            "location":  loc,
            "gender":    gen,
            "age":       age,
            "education": edu,
        })

    csv_path = out_dir / "health_metadata.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "location",
                                                "gender", "age", "education"])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"✓ Generated {len(csv_rows)} German health testimonies in "
          f"{out_dir.resolve()}")
    print(f"  Seed used: {args.seed}")
    from collections import Counter
    print(f"  Location:  {dict(Counter(p[0] for p in profiles))}")
    print(f"  Gender:    {dict(Counter(p[1] for p in profiles))}")
    print(f"  Age:       {dict(Counter(p[2] for p in profiles))}")
    print(f"  Education: {dict(Counter(p[3] for p in profiles))}")


if __name__ == "__main__":
    main()
