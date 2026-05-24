#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_test_biographies_de.py
============================

Generate 50 synthetic German biographical narratives, first-person,
contrasting by gender × profession (3 professions).

USAGE
-----
    python make_test_biographies_de.py [--seed SEED] [--output DIR]

DESIGN
------
Each narrative follows a loose biographical arc:
    childhood → education → career → family → today.
Sentences are drawn from:
- A profession pool (vocabulary, career milestones)
- A gender pool (subtle: domestic/career emphasis, interruptions)
- A common life-events pool (everyone has)

Distribution: 26 F / 24 M; ~17 per profession (Lehrer / Arbeiter / Pflegekraft).
- Pflegekraft = nursing/care worker (often associated with women historically,
  but we mix freely for realism).

Expected differentiation:
- NET on profession (different vocabulary, career arcs)
- SUBTLE on gender (career interruption, mention of domestic life)
"""

import argparse
import csv
import random
from pathlib import Path

# =============================================================================
# CHILDHOOD — universal first paragraph
# =============================================================================
CHILDHOOD = [
    "Ich bin in den siebziger Jahren in einer kleinen Stadt in Sachsen-Anhalt aufgewachsen.",
    "Meine Kindheit habe ich auf dem Land verbracht, in einem Dorf mit kaum tausend Einwohnern.",
    "Ich wurde 1968 geboren und wuchs in einer Arbeiterfamilie in Halle auf.",
    "Mein Geburtsjahrgang ist 1972, und ich bin in Magdeburg zur Welt gekommen.",
    "Als Kind der frühen achtziger Jahre habe ich noch die Wende bewusst miterlebt.",
    "Ich komme aus einer Lehrerfamilie und bin in der DDR groß geworden.",
    "Meine Eltern waren beide in der Landwirtschaft tätig, ich bin auf einem Hof aufgewachsen.",
]

# =============================================================================
# EDUCATION — generic
# =============================================================================
EDUCATION_GENERIC = [
    "Die Schulzeit war für mich eine Zeit der Orientierung, ich wusste lange nicht, was ich werden wollte.",
    "Nach dem Abitur wollte ich zunächst etwas ganz anderes machen als das, was ich später ergriffen habe.",
    "Meine Ausbildung habe ich direkt nach der zehnten Klasse begonnen.",
    "Die Berufswahl war für mich keine bewusste Entscheidung, sondern eher ein Hineinwachsen.",
]

# =============================================================================
# PROFESSION POOLS — career-specific vocabulary and arcs
# =============================================================================
PROFESSION_POOLS = {
    "Lehrer": {
        "education": [
            "Ich habe an der Universität in Leipzig Lehramt für Grundschule studiert.",
            "Das Studium der Pädagogik und der Germanistik dauerte sechs Semester länger als geplant.",
            "Mein Referendariat absolvierte ich an einer Schule in Halle-Neustadt.",
            "Die zweite Staatsprüfung war ein echter Einschnitt in meinem Leben.",
        ],
        "career": [
            "In den ersten Jahren als Lehrer war ich Klassenlehrer einer fünften Klasse.",
            "Ich unterrichtete vor allem Mathematik und Geografie, später kam noch Ethik dazu.",
            "Die Konferenzen, die Korrekturen, die Elterngespräche — der Beruf füllt mehr aus, als man denkt.",
            "Ich habe drei Generationen von Schülern und Schülerinnen begleitet.",
            "Die Schulreformen der letzten Jahrzehnte haben den Alltag im Klassenzimmer stark verändert.",
            "Ich habe an einem Gymnasium in der Innenstadt unterrichtet, bis ich pensioniert wurde.",
            "Pädagogische Beziehungen aufzubauen war für mich das Wichtigste an meinem Beruf.",
            "Die Korrekturarbeit am Wochenende war über Jahrzehnte mein Begleiter.",
        ],
        "today": [
            "Heute gebe ich noch ehrenamtlich Nachhilfe für Kinder aus sozial benachteiligten Familien.",
            "Im Ruhestand engagiere ich mich in der Erwachsenenbildung an der Volkshochschule.",
            "Ich verfolge die Diskussionen über die Schule heute weiterhin mit großem Interesse.",
        ],
    },
    "Arbeiter": {
        "education": [
            "Ich habe eine Lehre als Maschinenbauer in einem volkseigenen Betrieb absolviert.",
            "Meine Ausbildung zum Schlosser dauerte drei Jahre, Berufsschule und Werkstatt im Wechsel.",
            "Nach der zehnten Klasse begann ich eine Facharbeiterausbildung in der Chemieindustrie.",
            "Den Beruf habe ich von der Pike auf gelernt, ohne lange theoretische Umwege.",
        ],
        "career": [
            "Ich habe vierzig Jahre in derselben Fabrik gearbeitet, an verschiedenen Maschinen.",
            "Die Schichtarbeit war hart, aber das Geld stimmte und die Kollegen wurden zur zweiten Familie.",
            "Die Wende war ein tiefer Einschnitt, viele meiner Kollegen verloren plötzlich ihre Stelle.",
            "Nach der Treuhand-Zeit musste ich mich umschulen lassen und in einem anderen Betrieb anfangen.",
            "Körperliche Arbeit hat mich geprägt, der Rücken trägt heute die Spuren davon.",
            "Ich war über Jahre Mitglied im Betriebsrat und habe mich für die Belegschaft eingesetzt.",
            "Die Akkordarbeit war manchmal entwürdigend, aber sie brachte das nötige Einkommen.",
            "In der Frühschicht aufzustehen war eine Disziplin, die mir bis heute geblieben ist.",
        ],
        "today": [
            "Heute lebe ich von einer kleinen Rente und bin froh, dass die Knie noch mitmachen.",
            "Mein Sohn hat einen ganz anderen Beruf ergriffen, das ist auch gut so.",
            "Ich gehe heute noch gerne in die alte Werkshalle, wenn dort Tag der offenen Tür ist.",
        ],
    },
    "Pflegekraft": {
        "education": [
            "Meine Ausbildung zur Krankenschwester habe ich an einer städtischen Klinik absolviert.",
            "Drei Jahre Ausbildung, zwischen Stationsarbeit und theoretischem Unterricht aufgeteilt.",
            "Nach der mittleren Reife begann ich die Ausbildung in der Altenpflege.",
            "Die Pflegeschule war für mich ein Ort, an dem ich viel über mich selbst gelernt habe.",
        ],
        "career": [
            "Auf der Intensivstation habe ich gelernt, was Verantwortung wirklich bedeutet.",
            "Ich habe in verschiedenen Pflegeheimen gearbeitet, immer im Schichtdienst.",
            "Der Personalmangel in der Pflege hat sich in den letzten Jahren dramatisch verschärft.",
            "Die emotionale Belastung des Berufs unterschätzen viele Außenstehende.",
            "Sterbebegleitung war ein Teil meines Alltags, der mich tief geprägt hat.",
            "Die Pflege braucht Hände, aber vor allem braucht sie Zeit, die uns oft fehlt.",
            "Wir Pflegekräfte sind das Rückgrat des Gesundheitssystems, auch wenn es selten anerkannt wird.",
            "Die Dokumentation am Computer hat in den letzten Jahren immer mehr Zeit gefressen.",
        ],
        "today": [
            "Heute arbeite ich nur noch in Teilzeit, mein Rücken lässt mehr nicht zu.",
            "Im Ruhestand mache ich noch ehrenamtliche Besuche im Hospiz.",
            "Ich engagiere mich in der Pflegekammer für bessere Arbeitsbedingungen.",
        ],
    },
}

# =============================================================================
# GENDER POOLS — subtle weighting on family/career emphasis
# =============================================================================
GENDER_FAMILY = {
    "F": [
        "Mit meinem ersten Kind habe ich drei Jahre Erziehungszeit genommen, das war für mich selbstverständlich.",
        "Die Vereinbarkeit von Familie und Beruf war ein ständiger Balanceakt, jeden Tag aufs Neue.",
        "Als alleinerziehende Mutter musste ich beruflich oft Abstriche machen.",
        "Mein Mann unterstützte mich zwar, aber die Hauptverantwortung für die Kinder lag bei mir.",
        "Ich habe meine Karriere für die Familie unterbrochen und das nie bereut.",
        "Die Frage nach Kindern hat mich beruflich oft anders dastehen lassen als meine männlichen Kollegen.",
        "Meine Tochter wuchs zu großen Teilen bei meiner Mutter auf, weil ich arbeiten musste.",
    ],
    "M": [
        "Meine Frau hat sich in den ersten Jahren um die Kinder gekümmert, ich war beruflich stark eingespannt.",
        "Die Geburt meines Sohnes habe ich erlebt, ohne meine Arbeit groß zu unterbrechen.",
        "Meine berufliche Identität war über Jahrzehnte das Zentrum meines Lebens.",
        "Vaterschaft habe ich vor allem als wirtschaftliche Verantwortung verstanden, lange Zeit.",
        "Erst als die Kinder größer waren, habe ich angefangen, mehr im Haushalt mitzumachen.",
        "Meine Karriereschritte konnte ich verfolgen, ohne dabei die Familie ins Zentrum rücken zu müssen.",
    ],
}

# =============================================================================
# UNIVERSAL LIFE EVENTS — sprinkled in across all profiles
# =============================================================================
UNIVERSAL = [
    "Ein Wendepunkt war für mich der Umzug in eine andere Stadt, das hat vieles verändert.",
    "Der Tod meines Vaters war ein Einschnitt, der mich politisch nachdenklicher gemacht hat.",
    "Mit fünfzig habe ich noch einmal angefangen, ein Instrument zu lernen.",
    "Reisen war für mich immer wichtig, auch wenn das Geld nicht für die großen Ziele reichte.",
    "Die Wende habe ich als Befreiung erlebt, aber sie hat auch viel Sicherheit weggenommen.",
    "Mein Glaube hat mich durch schwere Zeiten getragen, auch wenn ich heute weniger in die Kirche gehe.",
    "Die Freundschaften aus der Jugend halten heute noch, wir treffen uns regelmäßig.",
    "Politisch engagiere ich mich seit Jahren in meiner Gemeinde.",
]


# =============================================================================
# COMPOSITION
# =============================================================================

def make_biography(gender: str, profession: str, rng: random.Random) -> str:
    """Compose one biographical narrative."""
    parts = []
    # 1. Childhood (always)
    parts.append(rng.choice(CHILDHOOD))

    # 2. Education (generic + profession-specific)
    parts.append(rng.choice(EDUCATION_GENERIC))
    parts.append(rng.choice(PROFESSION_POOLS[profession]["education"]))

    # 3. Career (3-5 profession sentences + 1-2 universal)
    career_pool = PROFESSION_POOLS[profession]["career"]
    n_career = rng.randint(3, 5)
    parts.extend(rng.sample(career_pool, n_career))
    parts.extend(rng.sample(UNIVERSAL, rng.randint(1, 2)))

    # 4. Family/gender (1-2 sentences)
    n_family = rng.randint(1, 2)
    parts.extend(rng.sample(GENDER_FAMILY[gender], n_family))

    # 5. Today (1 sentence)
    parts.append(rng.choice(PROFESSION_POOLS[profession]["today"]))

    return " ".join(parts) + "\n"


def make_profile_distribution(rng: random.Random) -> list:
    """50 total, 3 professions (~17 each), 26 F / 24 M."""
    profiles = []
    professions = ["Lehrer"] * 17 + ["Arbeiter"] * 17 + ["Pflegekraft"] * 16
    genders = ["F"] * 26 + ["M"] * 24

    rng.shuffle(professions)
    rng.shuffle(genders)
    for g, p in zip(genders, professions):
        profiles.append((g, p))
    return profiles


def main():
    parser = argparse.ArgumentParser(
        description="Generate German biographical narratives corpus.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=str,
                        default="test_biographies_de")
    parser.add_argument("--n-biographies", type=int, default=50)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles = make_profile_distribution(rng)[:args.n_biographies]

    csv_rows = []
    for idx, (gender, profession) in enumerate(profiles, start=1):
        fname = f"bio_{gender}_{profession}_{idx:03d}.txt"
        text = make_biography(gender, profession, rng)
        (out_dir / fname).write_text(text, encoding="utf-8")
        csv_rows.append({
            "filename":   fname,
            "gender":     gender,
            "profession": profession,
        })

    csv_path = out_dir / "biographies_metadata.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "gender",
                                                "profession"])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"✓ Generated {len(csv_rows)} German biographies in "
          f"{out_dir.resolve()}")
    print(f"  Seed used: {args.seed}")
    from collections import Counter
    print(f"  Gender:     {dict(Counter(p[0] for p in profiles))}")
    print(f"  Profession: {dict(Counter(p[1] for p in profiles))}")


if __name__ == "__main__":
    main()
