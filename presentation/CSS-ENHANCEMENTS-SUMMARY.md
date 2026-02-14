# CSS Enhancements from Linux Presentations

## Overview
Enhanced shared.css by incorporating useful patterns from `/home/rajesh/Training/linux-edge-k3s-mqtt/linux-presentations/`

## New Features Added

### 1. Enhanced CSS Variables
```css
--accent-light: #80d8ff        /* Lighter accent variant */
--accent-dark: #0091ea         /* Darker accent variant */
--bg-dark: #0a0f1a             /* Dark background */
--text-primary: #e0e6ed        /* Primary text color */
--text-muted: #8899aa          /* Muted text color */
--success: #26a69a             /* Success/lab color */
--warning: #ffa726             /* Warning color */
--danger: #ef5350              /* Danger/error color */
```

**Use cases:**
- `--success` for lab slides and positive callouts
- `--warning` for quiz slides and caution messages
- `--danger` for error states and critical warnings

### 2. Inline Code Styling
```css
.reveal code:not(pre code)
```
Enhanced styling for inline code with:
- Background: `rgba(79, 195, 247, 0.12)`
- Accent-light color
- Proper padding and border-radius
- Monospace font family

**Example:** `<code>npm install</code>` now has better visual distinction

### 3. Grid Layout Classes

#### Two-Column Layout
```css
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
```

#### Three-Column Layout
```css
.three-col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
```

**Usage:**
```html
<div class="two-col">
  <div>Column 1</div>
  <div>Column 2</div>
</div>
```

### 4. Tag/Badge System

**Classes:** `.tag`, `.tag-green`, `.tag-orange`, `.tag-red`, `.tag-success`, `.tag-warning`, `.tag-danger`

```html
<span class="tag">Default</span>
<span class="tag-success">Lab</span>
<span class="tag-warning">Quiz</span>
<span class="tag-danger">Warning</span>
```

**Styling:**
- Semi-transparent backgrounds with matching colors
- Rounded corners (12px border-radius)
- Compact size (0.7em font-size)
- Inline-block display

### 5. Title Slide Enhancements

```css
.title-slide            /* Centers content */
.title-slide .duration  /* For session duration */
.title-slide .branding  /* For trainer/company info */
```

**Example:**
```html
<section class="title-slide">
  <h1>Course Title</h1>
  <p class="subtitle">Session 1 · Day 1</p>
  <p class="duration">90 minutes</p>
  <p class="branding">Trainer: Rajesh Gheware</p>
</section>
```

### 6. Heading Enhancements

```css
.reveal h2.with-border
```
Adds underline border to h2 headings:
- 3px solid border in accent-dark color
- 10px padding-bottom
- 20px margin-bottom

**Usage:** `<h2 class="with-border">Section Title</h2>`

### 7. Diagram Components

#### Diagram Box
```css
.diagram-box
```
Styled box for diagrams with:
- Background: `var(--bg-card)`
- Border: 2px solid accent-dark
- Center-aligned text
- Accent-light color

#### Diagram Arrow
```css
.diagram-arrow
```
Center-aligned arrows in accent color for flow diagrams

**Example:**
```html
<div class="diagram-box">Input</div>
<div class="diagram-arrow">↓</div>
<div class="diagram-box">Process</div>
```

### 8. Special Slide Types

#### Lab Slides
```css
.lab-slide h2          /* Green heading */
.lab-slide .highlight-box  /* Green highlight */
```

#### Quiz Slides
```css
.quiz-slide h2         /* Orange/warning heading */
```

#### Center Slides
```css
.center-slide          /* Center-aligned content */
.center-slide h2       /* No border-bottom */
```

**Usage:**
```html
<section class="lab-slide">
  <h2>Hands-On Lab</h2>
  <!-- Lab content -->
</section>
```

### 9. Navigation Buttons

#### Home Button
```css
.home-btn
```
Fixed position navigation button with:
- Top-left positioning
- Backdrop blur effect
- Hover animations
- SVG icon support

**Example:**
```html
<a href="index.html" class="home-btn">
  <svg>...</svg>
  Home
</a>
```

### 10. Enhanced Table Styling

```css
table.comparison-alt
```
Alternative table styling with:
- Accent-dark header background
- Alternating row colors
- Hover effects
- Smaller font size (0.72em)

**Usage:**
```html
<table class="comparison-alt">
  <thead>
    <tr><th>Feature</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td>Item 1</td><td>Details</td></tr>
  </tbody>
</table>
```

### 11. Slide Viewport Containment

Enhanced scrollbar styling for slides:
- Thin scrollbars
- Accent-colored thumbs
- Transparent tracks
- Hover effects

**Benefits:**
- Better handling of overflow content
- Consistent scrollbar appearance
- Improved visual feedback

### 12. Enhanced List Styling

```css
.reveal ul.styled-list
```
Custom bullet points with:
- Triangle bullets (▸) for first level
- Circle bullets (○) for second level
- Accent color bullets
- Better spacing

**Usage:**
```html
<ul class="styled-list">
  <li>First level item
    <ul>
      <li>Second level item</li>
    </ul>
  </li>
</ul>
```

### 13. Highlight Box (Alternative Callout)

```css
.highlight-box
.highlight-box.success
.highlight-box.warning
.highlight-box.danger
```

Simpler callout style compared to existing callouts:
- Left border accent
- Semi-transparent background
- Rounded corners on right side only
- Multiple color variants

**Example:**
```html
<div class="highlight-box">
  Default highlight box
</div>
<div class="highlight-box success">
  Success message
</div>
```

## Comparison: Oracle vs Linux Presentation Styles

| Feature | Oracle Original | Linux Style | Now Available |
|---------|----------------|-------------|---------------|
| **Color System** | 4 accent colors | Semantic naming (success/warning/danger) | Both ✓ |
| **Grid Layouts** | .card-grid, .card-grid-3 | .two-col, .three-col | Both ✓ |
| **Tags/Badges** | .quiz-badge, .phase-badge | .tag with variants | Both ✓ |
| **Tables** | .compare-table | .comparison-alt | Both ✓ |
| **Callouts** | .takeaway, .tip-callout, etc. | .highlight-box | Both ✓ |
| **Navigation** | .index-link (bottom-left) | .home-btn (top-left) | Both ✓ |
| **Slide Types** | Generic sections | .lab-slide, .quiz-slide | Both ✓ |
| **Inline Code** | Basic styling | Enhanced with background | Enhanced ✓ |
| **Scrollbars** | Basic code blocks | Slides + code blocks | Enhanced ✓ |

## When to Use Each Style

### Use Original Oracle Styles For:
- **Cards:** Complex content with titles and descriptions
- **Callouts:** Detailed explanations with icons (💡, ⚠️, 📝)
- **Quiz Options:** Multiple choice with letter badges
- **Agent Diagrams:** Supervisor/worker patterns
- **Phase Badges:** Capstone project phases

### Use Linux-Inspired Styles For:
- **Tags:** Quick labels and categories
- **Simple Grids:** Two/three column layouts without cards
- **Highlight Boxes:** Simple emphasized text blocks
- **Lab/Quiz Slides:** Special slide type indicators
- **Diagram Boxes:** Flow diagrams and process steps
- **Comparison Tables:** Alternative table styling

### Combine Both For:
- **Rich Presentations:** Use cards with tags
- **Labs:** Use .lab-slide with .card-grid
- **Quizzes:** Use .quiz-slide with existing quiz-option styles
- **Diagrams:** Mix .diagram-box with .pipe-flow or .branch-diagram

## Migration Guide

No breaking changes! All existing Oracle presentation styles remain intact. New styles are additive only.

### Optional Enhancements:
1. Add `.with-border` to h2 elements for underline effect
2. Replace generic divs with `.two-col` or `.three-col` for simpler grids
3. Use `.tag-*` for inline labels instead of custom spans
4. Add `.title-slide` class to first slide for better formatting
5. Use `.highlight-box` for simple callouts where full .tip-callout is too heavy

## File Size Impact

- **Before:** ~62 KB
- **After:** ~72 KB (+10 KB)
- **Lines Added:** ~200 lines

Additional 10 KB provides significant flexibility for future presentations.

## Summary

✓ All original Oracle styles preserved
✓ 13 new component types added
✓ Better semantic color naming
✓ Enhanced inline code and scrollbar styling
✓ More layout options (grids, columns)
✓ Special slide types (lab, quiz, center)
✓ Alternative table and callout styles
✓ Navigation button support

The enhanced shared.css now supports both detailed enterprise presentations (Oracle style) and cleaner technical presentations (Linux style).
