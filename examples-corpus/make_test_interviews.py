#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_test_interviews.py
=======================

Generate a synthetic English-language Covid interview corpus for MTA
classroom testing. Produces 50 interviews with a Q/R semi-structured
format, plus a CSV metadata file.

USAGE
-----
    python make_test_interviews.py [--seed SEED] [--output DIR]

DESIGN
------
- Each interview is built from a pool of plausible sentences classified
  by sociological theme (work, family, health, finance, isolation, etc.).
- For each interview, the sentence pool is weighted by the speaker's
  profile (gender × age × income), producing subtle but real differences.
- Some sentences are profile-neutral (common Covid experience).
- Group differences are designed to be:
    * NET on income      (well-documented inequalities in Covid)
    * MODERATE on age    (different life stages → different concerns)
    * SUBTLE on gender   (some topics show it, others don't)

This is a SYNTHETIC corpus for teaching the MTA pipeline only.
Do NOT draw real sociological conclusions from these interviews.
"""

import argparse
import csv
import random
import os
from pathlib import Path

# =============================================================================
# QUESTION POOL — the interviewer's voice (constant across interviews)
# =============================================================================
QUESTIONS = [
    "How did you experience the lockdown periods?",
    "What changed the most in your daily life during the pandemic?",
    "How did you handle work or income during this period?",
    "Did you worry about your health or the health of people close to you?",
    "How did your social relationships evolve during the pandemic?",
    "What role did digital tools play in your daily life?",
    "How do you look back on the vaccination campaign?",
    "What lessons do you take from this period?",
    "Did you find the restrictions justified or excessive?",
    "How did you feel about masks and physical distancing rules?",
]

# =============================================================================
# SENTENCE POOL — keyed by theme, used to compose answers
# =============================================================================
# Each theme contains 10-20 plausible answer sentences. Themes are
# weighted differently for each profile to create subtle group signals.

SENTENCES = {
    # ---- Income-driven themes ----
    "financial_struggle": [
        "Money was very tight during those months, I had to cut everything.",
        "I lost my job during the first wave and finding a new one took ages.",
        "I went to the food bank for the first time in my life, it was humbling.",
        "Paying rent became a real source of anxiety, every month was a battle.",
        "I had to ask my family for help with the bills, which I had never done.",
        "Unemployment benefits arrived late and were not enough to live on.",
        "I postponed dental care and other things because money was scarce.",
        "We cut spending on food and clothes to keep the essentials going.",
        "My partner and I both lost income at the same time, it was hard.",
        "The eviction moratorium probably saved us from being homeless.",
    ],
    "financial_comfort": [
        "Financially we were lucky, my job continued from home without issue.",
        "We even saved money during lockdown since we could not travel or eat out.",
        "I used the savings to renovate our house and improve our home office.",
        "Our investments took a hit at first but recovered nicely afterwards.",
        "We bought a second property in the countryside for weekends away.",
        "Travel restrictions cost us nothing financially, we just postponed trips.",
        "I worked from our holiday home for several months, it was actually pleasant.",
        "We invested in better technology to make remote work more comfortable.",
        "The pandemic barely affected our family budget, we were fortunate.",
        "We supported local businesses since we had the means to do so.",
    ],
    "middle_finances": [
        "We managed financially but had to be more careful with spending.",
        "I used some of our savings to get through the uncertain months.",
        "My salary was reduced for a while but my job was never really at risk.",
        "We postponed buying a new car and a few other expenses.",
        "The mortgage was a worry but we kept up with payments.",
    ],

    # ---- Age-driven themes ----
    "young_precarity": [
        "I was a student then and my part-time job disappeared overnight.",
        "Internships were cancelled, it really delayed the start of my career.",
        "Online classes were exhausting and not what I had signed up for.",
        "I moved back in with my parents because I could not afford rent alone.",
        "Job interviews on video felt strange, I struggled to make a connection.",
        "Many of my friends were in the same boat, all our plans got postponed.",
        "I felt my early career years were stolen by the pandemic.",
        "Graduation ceremonies, parties, all the milestones were just gone.",
    ],
    "middle_parenting": [
        "Working from home with the kids was an enormous challenge daily.",
        "School closures forced us to homeschool while keeping our jobs going.",
        "The kids missed their friends terribly and it broke my heart to see.",
        "Daycare closures meant we juggled meetings and toddlers all day.",
        "My partner and I had to split the day in shifts to manage the children.",
        "Helping with homework on top of my own work was completely draining.",
        "We bought tablets for each child so they could attend online classes.",
        "The mental load of organizing the household exploded during lockdown.",
    ],
    "older_career_stress": [
        "At my age, the prospect of losing my job and finding another was scary.",
        "I worried that age discrimination would make a job search impossible.",
        "My parents were elderly and I lived in fear of bringing the virus home.",
        "The shift to remote work was difficult at my age, the technology was new.",
        "Restructuring at my company put older employees under particular pressure.",
        "I had to learn many new digital tools faster than I would have liked.",
    ],
    "elder_isolation": [
        "I was advised to stay home for months because of my age and health.",
        "I went weeks without seeing anyone in person, only voices on the phone.",
        "My grandchildren visited through the window or on a video call.",
        "The vaccine appointment day was a real relief, almost a celebration.",
        "I lost a friend to the virus and could not attend the funeral properly.",
        "The isolation was harder than the fear of the illness itself.",
        "Family video calls became the highlight of my week.",
        "I felt forgotten by the world during those long quiet months.",
    ],

    # ---- Gender-leaning themes (subtle weighting) ----
    "domestic_load": [
        "Most of the housework fell on me even though we were both home.",
        "I was constantly cooking, the family ate every meal at home for months.",
        "I noticed I was the one keeping track of supplies, medicines, schedules.",
        "The emotional support for the whole family became my unspoken job.",
        "Childcare and household tasks combined left no time for myself.",
    ],
    "remote_work_technical": [
        "Setting up the home office, the VPN, the dual monitors took some work.",
        "I had to learn to lead meetings on video, it changed my management style.",
        "Productivity actually improved without commuting and office distractions.",
        "Coordinating projects across distributed teams was a real shift.",
        "I redesigned my workflow around asynchronous communication tools.",
    ],

    # ---- Universal Covid themes (everyone speaks about this) ----
    "masks_distancing": [
        "Wearing a mask became second nature after a few weeks.",
        "Keeping physical distance from people felt strange and unnatural at first.",
        "I sometimes still wear a mask in crowded places out of habit.",
        "The mask debates in the media were exhausting to follow.",
        "I had complicated feelings about masking children in schools.",
    ],
    "vaccination": [
        "I got vaccinated as soon as I was eligible, it gave me real peace of mind.",
        "I waited a few weeks to see how the vaccines worked before taking mine.",
        "The vaccination process was well organized in my area, very efficient.",
        "I had a sore arm and tiredness for a day, but nothing worse than that.",
        "Booster doses became part of the routine, like an annual habit.",
        "Some people in my circle were hesitant, we had many long conversations.",
    ],
    "health_worry": [
        "I was constantly worried about catching the virus and falling severely ill.",
        "Every time someone in the family coughed, the anxiety came back.",
        "I started paying much more attention to my general health and immunity.",
        "Knowing someone in intensive care really brought the threat home.",
        "Reading the daily case numbers became an unhealthy obsession for a while.",
    ],
    "digital_tools": [
        "Video calls replaced almost all face-to-face interaction for months.",
        "Online grocery shopping became a habit I have kept ever since.",
        "I joined virtual social events, which felt strange but better than nothing.",
        "Streaming services kept us entertained through the long evenings indoors.",
        "I rediscovered email and phone calls after years of mostly messaging.",
    ],
    "social_relations": [
        "I learned who my real friends were when we could not meet in person.",
        "Some relationships deepened, others quietly faded during the long months.",
        "Outdoor walks with one friend at a time became precious moments.",
        "I noticed I made fewer but more meaningful contacts during that time.",
        "Reconnecting with people after restrictions lifted was sometimes awkward.",
    ],
    "policy_views": [
        "I felt the restrictions were generally reasonable given the circumstances.",
        "Some rules seemed inconsistent and that undermined public trust.",
        "I think governments learned a lot but communicated badly at the start.",
        "Looking back, the response could have been faster and more coordinated.",
        "I trusted the public health authorities even when their advice changed.",
    ],
    "looking_back": [
        "I think the pandemic forced us to reconsider what really matters in life.",
        "Some things changed permanently, like how we view work and where we live.",
        "I appreciate small everyday freedoms much more than I used to.",
        "Society proved more fragile than I thought but also more resilient.",
        "The mental health consequences are still with us, I think, even now.",
    ],
}


# =============================================================================
# PROFILE → THEME WEIGHTS
# =============================================================================
# For each profile dimension, define how heavily each theme is weighted
# relative to baseline 1.0. Multiple dimensions multiply together.

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
    """Multiply the base weight (1.0) by gender × age × income modifiers."""
    weights = {theme: 1.0 for theme in SENTENCES.keys()}
    for src in (GENDER_WEIGHTS[gender], AGE_WEIGHTS[age], INCOME_WEIGHTS[income]):
        for theme, w in src.items():
            weights[theme] *= w
    return weights


def pick_sentence(rng: random.Random, theme_weights: dict) -> str:
    """Pick a theme according to weights, then a sentence from that theme."""
    themes = list(theme_weights.keys())
    weights = [theme_weights[t] for t in themes]
    theme = rng.choices(themes, weights=weights, k=1)[0]
    return rng.choice(SENTENCES[theme])


def make_interview(gender: str, age: str, income: str,
                   rng: random.Random,
                   n_questions: int = 7) -> str:
    """Compose a single semi-structured interview as a Q/R text."""
    weights = compute_theme_weights(gender, age, income)
    questions = rng.sample(QUESTIONS, n_questions)
    lines = []
    for q in questions:
        lines.append(f"Q: {q}")
        # Each answer has 2-4 sentences
        n_sent = rng.randint(2, 4)
        answer_parts = [pick_sentence(rng, weights) for _ in range(n_sent)]
        lines.append("R: " + " ".join(answer_parts))
        lines.append("")  # blank line between exchanges
    return "\n".join(lines).strip() + "\n"


def make_profile_distribution(rng: random.Random) -> list:
    """
    Return a list of 50 (gender, age, income) tuples, slightly unbalanced
    for realism.
    """
    # Target counts:
    # Gender: 28 F, 22 M
    # Age: 12 in 18-29, 18 in 30-44, 12 in 45-59, 8 in 60+
    # Income: 18 low, 19 mid, 13 high
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
        description="Generate a synthetic Covid interview corpus for MTA.",
    )
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility (default: 42).")
    parser.add_argument("--output", type=str,
                        default="test_interviews_covid_en",
                        help="Output directory (default: "
                             "test_interviews_covid_en).")
    parser.add_argument("--n-interviews", type=int, default=50,
                        help="Number of interviews (default: 50).")
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

    # Write the metadata CSV
    csv_path = out_dir / "interviews_metadata.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "gender",
                                                "age", "income"])
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"✓ Generated {len(csv_rows)} interviews in {out_dir.resolve()}")
    print(f"  Seed used: {args.seed}")
    # Summary of distribution
    from collections import Counter
    print(f"  Gender: {dict(Counter(p[0] for p in profiles))}")
    print(f"  Age:    {dict(Counter(p[1] for p in profiles))}")
    print(f"  Income: {dict(Counter(p[2] for p in profiles))}")


if __name__ == "__main__":
    main()
