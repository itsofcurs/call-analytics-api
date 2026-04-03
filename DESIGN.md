# Design System Specification: The Ethereal Intelligence Framework

## 1. Overview & Creative North Star: "The Predictive Prism"
This design system moves beyond the rigid, boxy layouts of traditional enterprise dashboards. Our Creative North Star is **The Predictive Prism**. 

In a Call Center Analytics environment, data is fluid and constant. We treat the UI not as a static container, but as a lens that clarifies noise into signal. We break the "template" look by using intentional asymmetry, where data visualizations bleed into the margins, and high-contrast typography scales that prioritize "the headline insight" over the "data table." This system is built on depth, utilizing glassmorphism and tonal layering to suggest a sophisticated, AI-driven intelligence working behind the glass.

---

## 2. Colors & Surface Philosophy
The palette is a sophisticated interplay of deep charcoals and high-energy electric accents.

### The "No-Line" Rule
Standard 1px solid borders are strictly prohibited for sectioning. Structural definition must be achieved through **Background Color Shifts** or **Tonal Transitions**. Use `surface-container-low` against a `surface` background to define regions.

### Surface Hierarchy & Nesting
Treat the UI as physical layers of frosted obsidian. 
- **Base Layer:** `surface` (#0b1326)
- **Sectioning:** `surface-container-low` (#131b2e) or `surface-container` (#171f33)
- **Interactive/Primary Cards:** `surface-container-highest` (#2d3449)

### The Glass & Gradient Rule
AI-driven features must utilize glassmorphism to feel "active" and "sentient."
- **Glass Base:** `surface-variant` (#2d3449) at 40-60% opacity with `backdrop-blur-xl`.
- **Signature Glow:** For primary CTAs and AI Insights, use a linear gradient: `primary-container` (#0f69dc) to `secondary-container` (#571bc1). This provides a visual "soul" that flat colors cannot replicate.

---

## 3. Typography: Editorial Authority
We use a dual-font strategy to balance technical precision with executive authority.

- **Display & Headlines (Manrope):** Used for high-level metrics and section headers. Manrope’s geometric nature provides a modern, "tech-forward" feel.
- **Body & Labels (Inter):** Used for all data points, transcripts, and UI controls. Inter provides maximum readability at small scales.

| Token | Font | Size | Weight | Usage |
| :--- | :--- | :--- | :--- | :--- |
| `display-lg` | Manrope | 3.5rem | 700 | Hero AI metrics |
| `headline-md` | Manrope | 1.75rem | 600 | Card titles / Section headers |
| `title-sm` | Inter | 1rem | 500 | Component labels / Nav items |
| `body-md` | Inter | 0.875rem | 400 | Data tables / Transcripts |
| `label-sm` | Inter | 0.6875rem | 600 | Micro-metadata / Overlines |

---

## 4. Elevation & Depth: Tonal Layering
Depth is achieved through the **Layering Principle** rather than shadows. 

- **The Stacking Rule:** Place a `surface-container-lowest` element on top of a `surface-container-low` section to create a "recessed" look. Place a `surface-container-highest` element on a `surface` background to create a "raised" look.
- **Ambient Shadows:** For floating modals, use a tinted shadow: `shadow-[0_20px_50px_rgba(0,26,66,0.3)]`. This mimics light reflecting off the deep blue charcoal surfaces.
- **The "Ghost Border":** For necessary accessibility, use `outline-variant` (#434655) at 15% opacity. This creates a "suggestion" of a boundary without breaking the fluid glass aesthetic.

---

## 5. Components & Interaction Patterns

### Glassmorphic Cards
- **Backdrop:** `bg-surface-container/60` with `backdrop-blur-md`.
- **Border:** `border border-outline-variant/20`.
- **Spacing:** `p-6` (1.5rem) standard internal padding.
- **Note:** Never use dividers. Use `mb-8` (2rem) vertical spacing to separate content groups.

### Buttons (The "Sleek Glow" Variant)
- **Primary:** `bg-primary-container` with a subtle outer glow using `box-shadow: 0 0 15px theme('colors.primary.DEFAULT' / 0.3)`.
- **Secondary:** Transparent background with the "Ghost Border" and `on-surface` text.
- **Interaction:** On hover, increase `backdrop-blur` or shift gradient intensity.

### AI Status Indicators
- **Active AI:** A breathing animation using `secondary` (#d0bcff) with a 4px blur glow.
- **Processing:** A subtle CSS "shimmer" effect moving across the `surface-container-highest` background.

### Integrated Charts
- **Stroke:** Use `tertiary` (#4cd7f6) for line charts.
- **Fill:** Use a gradient of `tertiary` to transparent.
- **Grid Lines:** If required, use `outline-variant` at 5% opacity.

---

## 6. Do’s and Don’ts

### Do
- **Do** use `leading-relaxed` for call transcripts to ensure readability.
- **Do** use `rounded-xl` (1.5rem) for main dashboard containers to soften the professional look.
- **Do** allow AI insights to overlap slightly with the charts they describe, creating a sense of "layered intelligence."
- **Do** use `surface-bright` (#31394d) for hover states on list items.

### Don’t
- **Don't** use pure black (#000000). Always use the charcoal `surface` tokens to maintain depth.
- **Don't** use 100% opaque borders; they shatter the glassmorphism illusion.
- **Don't** use standard "drop shadows" on cards; use tonal shifts and ghost borders instead.
- **Don't** use more than three accent colors in a single view. Stick to Primary (Blue) and Secondary (Violet).

---

## 7. Implementation (Tailwind CSS Snippet)