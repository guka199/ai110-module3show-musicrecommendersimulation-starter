# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0** — a content-based music recommender simulation.

---

## 2. Intended Use

VibeFinder suggests up to five songs from a small hand-curated catalog based on a user's
stated genre, mood, energy level, valence (positiveness), and tempo preference. It is built
for classroom exploration of how recommender systems work — not for production use or real
listeners.

It assumes the user can describe their taste with explicit preferences (e.g., "I want chill
lofi at energy 0.38"). Real-world systems infer these from listening history; this simulation
skips that step on purpose to keep the logic transparent.

---

## 3. How the Model Works

Imagine each song wears a name tag with five numbers: how energetic it is, how positive it
sounds, how fast the beat is, plus labels for its genre and mood. The user also wears a name
tag with their ideal values.

VibeFinder compares the two name tags song by song. For genre and mood it asks "do they
match exactly?" — a match adds bonus points. For energy, positiveness, and tempo it asks
"how close are the numbers?" — the closer, the more points. The song with the most total
points rises to the top.

That is literally the whole algorithm: five comparisons, five scores, one sum, sort by sum.

---

## 4. Data

The catalog contains **18 songs** across 11 genres: pop, lofi, rock, ambient, jazz,
synthwave, indie pop, hip-hop, classical, country, metal, reggae, r&b, edm, and blues.
Moods covered: happy, chill, intense, relaxed, moody, focused, confident, peaceful,
nostalgic, aggressive, romantic, euphoric, and melancholy.

The 10 starter songs were provided by the course. I added 8 songs to fill clear gaps
(classical, metal, reggae, blues, r&b, edm, hip-hop, country). Despite this expansion,
pop and lofi still have the most songs (3 each), which gives them a structural advantage.

---

## 5. Strengths

- **Clear profiles get clear results.** The "Chill Lofi Studier" profile ranked the two
  most textbook-lofi tracks (#1 Library Rain, #2 Midnight Coding) exactly where intuition
  says they belong.
- **Transparent explanations.** Every recommendation includes a per-feature breakdown so
  the user can see exactly why a song ranked where it did.
- **Genre separation works.** The system correctly keeps metal and EDM out of the lofi
  results even when energy values overlap, because the genre bonus creates a clear gap.

---

## 6. Limitations and Bias

**Genre count skew.** Pop and lofi each have 3 catalog entries; classical, metal, r&b, and
blues each have only 1. A pop user has 3 chances to earn the +2.0 genre bonus; a blues user
has exactly 1. This makes the system structurally worse at serving niche tastes.

**Mood vocabulary is coarse.** Two songs tagged "chill" can feel completely different in
practice — one ambient drone, one jazzy guitar. The system treats them identically, which
can produce recommendations that match the label but not the actual listening experience.

**The genre bonus can overpower everything else.** With a +2.0 flat genre bonus, a mediocre
genre match always outscores a nearly-perfect energy/valence/tempo match in a different
genre. The "Conflicted Raver" experiment showed this: Ultraviolet Drop ranked first purely
on genre+energy, even though the user's mood preference ("melancholy") matched Crossroads
Lament far better.

**No personalization over time.** The system has no memory. It cannot learn that a user
who said "lofi" actually skips every track under 70 bpm. Every run starts from zero.

**Cold-start assumption.** The system requires the user to self-describe their taste
accurately. New or casual users who cannot name a genre or target energy level cannot be
served.

---

## 7. Evaluation

I tested five user profiles:

| Profile | Top Result | Intuition Match? |
|---|---|---|
| High-Energy Pop Fan | Sunrise City (pop/happy) | ✅ Perfect |
| Chill Lofi Studier | Library Rain (lofi/chill) | ✅ Perfect |
| Deep Intense Rock | Storm Runner (rock/intense) | ✅ Perfect |
| Conflicted Raver (EDM + melancholy) | Ultraviolet Drop (EDM/euphoric) | ⚠️ Genre won over mood |
| Classical Explorer | Moonlight Reverie (classical/peaceful) | ✅ Perfect |

**Surprise:** The "Conflicted Raver" edge case revealed that when a user has contradictory
categorical preferences (high-energy genre + sad mood), the system picks the genre winner and
ignores the mood signal almost entirely. Crossroads Lament — the one song with a melancholy
tag — ranked 4th, not 1st, because its energy was too low.

**Experiment — weight shift (genre ×0.5, energy ×2):**
Halving the genre bonus and doubling the energy multiplier caused Storm Runner (rock, high
energy) to enter the top 5 for the High-Energy Pop Fan profile, displacing Riddim Season.
Rooftop Lights also rose from rank 3 to 3 but with a much higher score. The experiment
confirmed that the system is sensitive to weight choices and that energy is a stronger
differentiator than genre when the weights allow it.

---

## 8. Future Work

- **Weighted categorical match.** Instead of a binary genre bonus, score genre similarity
  on a scale (pop ≈ indie pop > jazz > metal) so close-but-not-exact genres still earn
  partial credit.
- **Multi-mood preferences.** Let users specify a ranked list of moods so the system can
  reward songs that hit any of them, not just an exact string match.
- **Catalog diversity enforcement.** Cap results at one song per genre to prevent the pop
  catalog depth advantage from flooding the top 5.
- **Implicit profile learning.** Track which recommendations the user skips vs. replays,
  and nudge the target values accordingly between sessions.

---

## 9. Personal Reflection

Building VibeFinder made the invisible visible: real recommenders run the same basic loop
(score every item, sort, slice) but at the scale of 100 million songs with dozens of
features instead of 18 songs and five. The math is not magic — it is multiplication and
subtraction.

The most surprising moment was the "Conflicted Raver" profile. I expected the sad mood
preference to pull blues or synthwave to the top, but the system picked EDM because it saw
genre+energy and declared victory. That result is technically correct by the rules I wrote,
but it feels wrong — and that gap between "correct by the formula" and "right for the human"
is exactly where real recommender teams spend most of their time tuning.
