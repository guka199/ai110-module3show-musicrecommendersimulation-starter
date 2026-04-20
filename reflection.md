# Reflection: Profile Comparison Notes

## High-Energy Pop Fan vs. Chill Lofi Studier

These two profiles live at opposite ends of the energy axis (0.90 vs. 0.38), and the
results split cleanly in half — not a single song appeared on both lists. This is exactly
what you would want from a recommender: the energy proximity score has enough range (up to
±2.0 pts) to completely separate the catalog into two camps. The lofi user never sees a pop
track; the pop user never sees a lofi track. Energy is doing most of the heavy lifting here,
which makes sense — getting the energy wrong in a real playlist (a 150 bpm banger during a
study session) is immediately jarring in a way that a genre mismatch is not.

## High-Energy Pop Fan vs. Deep Intense Rock

Both profiles prefer high energy (0.90 vs. 0.95), but different genres and valence
(0.85 vs. 0.40). Gym Hero (pop/intense) appeared in both top-5 lists — rank 2 for the pop
fan and rank 2 for the rock fan. This makes sense: Gym Hero has the second-highest energy
in the catalog (0.93), so it floats up for any high-energy profile regardless of genre. The
key difference is that the rock fan's top slot went to Storm Runner (genre+mood+energy
triple-match) while the pop fan's went to Sunrise City (same triple-match, different genre).
The lesson: when one song perfectly matches three features, it dominates the list, and the
rest of the top 5 is filled by numerical energy proximity rather than genre loyalty.

## Conflicted Raver (edge case) vs. Deep Intense Rock

Both profiles want very high energy (~0.95) and low valence (~0.25–0.40). The results
overlap in the middle: Iron Storm and Storm Runner appear in both lists. But the top
slots diverge because of genre: the rock fan gets Storm Runner first (+2.0 genre bonus),
while the conflicted raver gets Ultraviolet Drop first (+2.0 EDM genre bonus). The "sad
mood" preference on the raver profile (melancholy) had almost no effect — Crossroads
Lament (the only melancholy-tagged song) appeared at rank 4, not rank 1, because its
energy (0.30) was a terrible match for a user who wants 0.95. This reveals a real tension:
the system cannot serve someone who wants "intense AND sad" because no single song in this
catalog combines those two attributes.

## Classical Explorer vs. Chill Lofi Studier

Both want low-energy, acoustic-leaning music (energy 0.20 vs. 0.38), and their results
share the same ambient/lofi underbelly (Library Rain, Focus Flow, Spacewalk Thoughts appear
in both). But the classical fan gets Moonlight Reverie at #1 (genre+mood+energy = perfect
triple-match, score 7.44), while the lofi studier gets Library Rain at #1 (also a triple-
match, score 7.41). The tiny score difference (0.03 pts) comes from tempo: Library Rain at
72 bpm is closer to the lofi target of 78 bpm than Moonlight Reverie at 66 bpm is to the
classical target of 65 bpm. This shows that even small numerical differences can decide
rankings when the categorical features are evenly matched.

## Weight Experiment: doubled energy, halved genre

Running the High-Energy Pop Fan profile with genre weight halved (2.0 → 1.0) and energy
weight doubled (2.0 → 4.0) changed the bottom two results. Riddim Season fell out of the
top 5, replaced by Storm Runner (rock) — a song the original weights would never surface
for a pop fan. Ultraviolet Drop (EDM) also climbed from rank 5 to rank 4. The reason: Storm
Runner has energy 0.91, nearly identical to the user's target of 0.90, so the 4× energy
multiplier awarded it almost the maximum 4.0 pts, enough to overcome the missing +1.0 genre
bonus. The experiment confirms that weight choices are not neutral — changing a single number
can hand the recommendation to a completely different genre.
