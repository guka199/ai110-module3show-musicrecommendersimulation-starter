import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


# Default scoring weights used by every profile unless overridden
DEFAULT_WEIGHTS: Dict[str, float] = {
    "genre":   2.0,   # flat bonus for categorical match
    "mood":    1.0,   # flat bonus for categorical match
    "energy":  2.0,   # proximity multiplier (0–2.0 pts)
    "valence": 1.5,   # proximity multiplier (0–1.5 pts)
    "tempo":   1.0,   # proximity multiplier after bpm normalization (0–1.0 pts)
}


@dataclass
class Song:
    """Immutable value object holding a single song's audio attributes from the CSV."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Stores a user's taste preferences used as the reference point for scoring."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.5
    target_tempo_bpm: float = 100.0


class Recommender:
    """OOP wrapper around the scoring logic; holds the song catalog in memory."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Return a weighted similarity score for one song against the user profile."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += DEFAULT_WEIGHTS["genre"]
        if song.mood == user.favorite_mood:
            score += DEFAULT_WEIGHTS["mood"]
        score += (1 - abs(song.energy - user.target_energy)) * DEFAULT_WEIGHTS["energy"]
        score += (1 - abs(song.valence - user.target_valence)) * DEFAULT_WEIGHTS["valence"]
        acoustic_target = 1.0 if user.likes_acoustic else 0.0
        score += (1 - abs(song.acousticness - acoustic_target)) * 0.5
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by descending similarity score."""
        # sorted() returns a NEW list; self.songs is left unchanged.
        # .sort() would mutate the list in place — avoided so the catalog stays
        # intact across multiple calls with different profiles.
        return sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable sentence describing why this song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre matches your preference for {song.genre}")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood matches your preference for {song.mood}")
        if abs(song.energy - user.target_energy) < 0.2:
            reasons.append(f"energy {song.energy:.2f} is close to your target {user.target_energy:.2f}")
        if not reasons:
            reasons.append("overall audio profile similarity")
        return "; ".join(reasons)


# ---------------------------------------------------------------------------
# Functional API (used by main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    songs = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(
    user_prefs: Dict,
    song: Dict,
    weights: Optional[Dict[str, float]] = None,
) -> Tuple[float, List[str]]:
    """
    Score one song against user preferences; return (total_score, reason_list).

    Algorithm recipe (default weights)
    -----------------------------------
    +2.0  genre match          (exact string, categorical)
    +1.0  mood match           (exact string, categorical)
    +2.0  energy proximity     (1 - |Δenergy|) × 2.0
    +1.5  valence proximity    (1 - |Δvalence|) × 1.5   — only if user supplies "valence"
    +1.0  tempo proximity      normalized over 200 bpm   — only if user supplies "tempo_bpm"

    Pass a custom `weights` dict to override any of the five multipliers for experiments.
    """
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    score = 0.0
    reasons = []

    if song.get("genre") == user_prefs.get("genre"):
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")

    if song.get("mood") == user_prefs.get("mood"):
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    target_energy = user_prefs.get("energy", 0.5)
    energy_pts = (1 - abs(song.get("energy", 0.5) - target_energy)) * w["energy"]
    score += energy_pts
    reasons.append(f"energy proximity (+{energy_pts:.2f})")

    if "valence" in user_prefs:
        valence_pts = (1 - abs(song.get("valence", 0.5) - user_prefs["valence"])) * w["valence"]
        score += valence_pts
        reasons.append(f"valence proximity (+{valence_pts:.2f})")

    if "tempo_bpm" in user_prefs:
        # Normalize over a 200 bpm ceiling so tempo is comparable to 0-1 features
        norm_song = song.get("tempo_bpm", 100) / 200.0
        norm_user = user_prefs["tempo_bpm"] / 200.0
        tempo_pts = (1 - abs(norm_song - norm_user)) * w["tempo"]
        score += tempo_pts
        reasons.append(f"tempo proximity (+{tempo_pts:.2f})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Optional[Dict[str, float]] = None,
) -> List[Tuple[Dict, float, str]]:
    """Score every song with score_song, sort descending, and return the top-k results."""
    # sorted() is used (not .sort()) so the original songs list is never mutated —
    # this matters when recommend_songs is called repeatedly with different profiles.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
