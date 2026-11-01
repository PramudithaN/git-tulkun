# Evolution Stages & Growth Mechanics

`git-tulkun` uses a **logarithmic growth curve** modeled to provide continuous, rewarding visual progression throughout the year.

The growth parameter $g \in [0, 1]$ is computed as:

$$g = \min\left(1.0, \left(\frac{\text{contributions}}{2800}\right)^{0.45}\right)$$

---

## The 5 Biological Life Stages

| Stage | Contributions (`annual` or `rolling`) | Spine Length | Anatomical Features Unlocked |
|---|---|---|---|
| **Stage 1: Baby Calf** | **`0 – 149`** | $64\text{ px}$ | Compact, rounded torso; blunt snout with a flat sensor dimple; pale cream dorsal swirl patches and stubby flippers with light cream caudal flukes. |
| **Stage 2: Yearling Calf** | **`150 – 499`** | $95\text{ px}$ | Slender body profile; *kuru* neural whips sprout behind the anterior opercular flippers; caudal flukes darken at the base. |
| **Stage 3: Adolescent Tulkun** | **`500 – 1,199`** | $130\text{ px}$ | Sensor crest organ begins elevating forward; all 6 pectoral and ventral flippers elongate with ivory leading edges; secondary pelvic accessory paddles widen. |
| **Stage 4: Mature Tulkun** | **`1,200 – 2,499`** | $160\text{ px}$ | Charcoal carapace replaces juvenile dorsal swirls; sloped crimson sensor crest with an olive-gold tip; 5 sharp sawtooth jaw triangles. |
| **Stage 5: Adult Male Bull** | **`2,500+`** | $186\text{ px}$ | Maximum leviathan length and full scythe-wing span; towering vertical hooked hammer-crest with concave rear overhang; 6 serrated jaw triangles; white carapace battle scars. |

---

## Seasonal Reset vs. Rolling Window

- **`annual` (Default)**: On **January 1st**, the contribution counter resets to zero, turning every user's Tulkun into a Baby Calf. This gamifies annual coding consistency.
- **`rolling`**: Uses your trailing 365-day contribution total. Your whale reflects your active 1-year development pace without seasonal resets.
