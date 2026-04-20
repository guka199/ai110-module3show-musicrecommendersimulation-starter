"""
Command-line runner for the Music Recommender Simulation.
Run from the project root: python -m src.main
"""

from recommender import load_songs, recommend_songs, DEFAULT_WEIGHTS

BAR = "─" * 60

# ---------------------------------------------------------------------------
# User Profiles
# ---------------------------------------------------------------------------

PROFILES = {
    "High-Energy Pop Fan": {
        "genre":     "pop",
        "mood":      "happy",
        "energy":    0.90,
        "valence":   0.85,
        "tempo_bpm": 128,
    },
    "Chill Lofi Studier": {
        "genre":     "lofi",
        "mood":      "chill",
        "energy":    0.38,
        "valence":   0.60,
        "tempo_bpm": 78,
    },
    "Deep Intense Rock": {
        "genre":     "rock",
        "mood":      "intense",
        "energy":    0.95,
        "valence":   0.40,
        "tempo_bpm": 155,
    },
    # Edge case: conflicting preferences (high energy + melancholy mood)
    # Tests whether numerical features can override categorical mismatch
    "Conflicted Raver (edge case)": {
        "genre":     "edm",
        "mood":      "melancholy",
        "energy":    0.95,
        "valence":   0.25,
        "tempo_bpm": 140,
    },
    # Edge case: niche genre with only one match in the catalog
    "Classical Explorer (edge case)": {
        "genre":     "classical",
        "mood":      "peaceful",
        "energy":    0.20,
        "valence":   0.75,
        "tempo_bpm": 65,
    },
}

# ---------------------------------------------------------------------------
# Experiment: double energy weight, halve genre weight
# This tests whether energy can drive recommendations more than genre loyalty.
# ---------------------------------------------------------------------------
EXPERIMENTAL_WEIGHTS = {
    **DEFAULT_WEIGHTS,
    "genre":  1.0,   # halved from 2.0
    "energy": 4.0,   # doubled from 2.0
}


def print_recommendations(label: str, prefs: dict, songs: list, weights=None) -> None:
    """Print a formatted recommendation block for one user profile."""
    print(f"\n{BAR}")
    print(f"  PROFILE: {label}")
    print(f"  genre={prefs.get('genre')}  mood={prefs.get('mood')}  "
          f"energy={prefs.get('energy')}  valence={prefs.get('valence', '—')}")
    if weights:
        print(f"  [EXPERIMENTAL weights: genre={weights['genre']}, energy={weights['energy']}]")
    print(BAR)

    results = recommend_songs(prefs, songs, k=5, weights=weights)
    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"  {rank}. {song['title']}  —  {song['artist']}")
        print(f"     Genre: {song['genre']:<14} Mood: {song['mood']:<14} Score: {score:.2f}")
        print(f"     Why: {explanation}")
    print()


def main() -> None:
    """Load songs and run recommendations for every defined profile plus one experiment."""
    songs = load_songs("data/songs.csv")
    print(f"\nLoaded {len(songs)} songs from catalog.\n")

    # --- Standard profiles ---
    for label, prefs in PROFILES.items():
        print_recommendations(label, prefs, songs)

    # --- Experiment: weight shift on High-Energy Pop Fan ---
    print(f"\n{'═' * 60}")
    print("  EXPERIMENT: doubled energy weight, halved genre weight")
    print(f"  (applied to 'High-Energy Pop Fan' profile)")
    print(f"{'═' * 60}")
    print_recommendations(
        "High-Energy Pop Fan [EXPERIMENTAL]",
        PROFILES["High-Energy Pop Fan"],
        songs,
        weights=EXPERIMENTAL_WEIGHTS,
    )


if __name__ == "__main__":
    main()
