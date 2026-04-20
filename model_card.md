# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0** — a content-based music recommender simulation.

---

## 2. Intended Use and Non-Intended Use

**Intended use:** VibeFinder is a classroom simulation built to teach how content-based
recommender systems work. It suggests up to five songs from a small hand-curated catalog
based on explicit user preferences (genre, mood, energy level, valence, and tempo). The
goal is transparency — every score is explainable in plain English — not accuracy at scale.

**Non-intended use:** VibeFinder should **not** be used as a production music service, a
tool for making decisions about which artists to promote, or as any kind of content
moderation system. It has a catalog of 18 songs, no knowledge of lyrics or cultural
context, no fairness auditing, and no way to handle user data responsibly. Deploying it
in any real product context would be misleading and potentially harmful to users who expect
the depth of a professional recommendation engine.

It also should not be used to infer anything about a real person's identity, mood, or
mental state from their music preferences — the "mood" labels in this catalog describe
the sound of a song, not the emotional state of the listener.

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

**Biggest learning moment**

The "Conflicted Raver" edge case was the clearest lesson of the whole project. I set up a
profile with high-energy EDM preferences but a "melancholy" mood — two preferences that
pull in opposite directions. I expected the system to compromise and surface something moody
but energetic (maybe synthwave). Instead it picked Ultraviolet Drop (EDM/euphoric) because
genre and energy together outweighed the mood signal. That result is *correct by the rules
I wrote* — but it feels wrong. That gap, between "right by the formula" and "right for the
human," was the moment the whole concept of AI alignment clicked for me in a concrete way.
Weight choices are not neutral engineering decisions; they encode a value judgment about what
matters most to a listener.

**How AI tools helped — and when I had to double-check**

AI tools (Copilot / Claude) were most useful for boilerplate: writing the CSV loader, the
dataclass definitions, the sorted() vs .sort() comparison. These are tasks where the code
is predictable and the risk of a subtle bug is low. Where I had to slow down and verify was
the scoring logic itself. The AI suggested a proximity formula that used `abs(song - user)`
which was correct, but it initially forgot to multiply the result by a weight — so all five
features were treated equally, defeating the whole purpose of the weighted design. The lesson:
AI tools draft, humans decide. Every weight choice and formula needed a sanity-check against
a known song (e.g., "Sunrise City is the best pop/happy match; does it actually score
highest?") before I trusted the output.

**What surprised me about how simple algorithms still "feel" like recommendations**

I expected 18 songs and five math operations to produce obviously mechanical results. What
surprised me was how *plausible* the outputs felt for well-defined profiles. When I ran the
"Chill Lofi Studier" profile, the system returned Library Rain and Midnight Coding at the
top — exactly what a thoughtful human DJ would pick. The reason it *feels* like intelligent
curation is that the features (energy, valence, tempo) genuinely capture the dimensions
listeners use to describe their taste, even if they never use those words. The algorithm
is not thinking; it is just measuring the same things a human measures, more precisely.
That made me realize that a lot of "AI magic" in products is the same arithmetic — the
sophistication is in choosing the right features and the right weights, not in the math itself.

**What I would try next**

If I continued this project, the first change would be replacing the binary genre bonus with
a genre similarity graph — so "indie pop" and "pop" share partial credit, and "ambient" and
"lofi" are neighbors. The second would be adding implicit feedback: a simple skip counter
that adjusts the user's target energy downward each time a high-energy track is skipped.
That single change would turn VibeFinder from a static form into something that actually
learns. The third would be a diversity rule at the ranking step — no two songs from the
same artist in the top five — because right now a catalog dominated by one artist would let
them sweep all five slots, which is a real fairness problem in production recommenders.
