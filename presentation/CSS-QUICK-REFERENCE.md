# CSS Quick Reference Guide

## CSS Variables

```css
/* Accent Colors */
--accent         /* #4fc3f7 - Primary blue */
--accent-light   /* #80d8ff - Light blue */
--accent-dark    /* #0091ea - Dark blue */
--accent2        /* #81c784 - Green */
--accent3        /* #ffb74d - Orange */
--accent4        /* #e57373 - Red */

/* Semantic Colors */
--success        /* #26a69a - Teal (labs) */
--warning        /* #ffa726 - Orange (quizzes) */
--danger         /* #ef5350 - Red (errors) */

/* Backgrounds & Text */
--bg-card        /* Semi-transparent white */
--bg-dark        /* #0a0f1a */
--text-primary   /* #e0e6ed */
--text-muted     /* #8899aa */
```

## Font Sizes

```css
.text-052   /* 0.52em */
.text-054   /* 0.54em */
.text-xs    /* 0.55em */
.text-060   /* 0.6em */
.text-sm    /* 0.65em */
.text-068   /* 0.68em */
.text-070   /* 0.7em */
.text-072   /* 0.72em */
.text-base  /* 0.75em */
.text-078   /* 0.78em */
.text-080   /* 0.8em */
.text-082   /* 0.82em */
.text-085   /* 0.85em */
.text-lg    /* 0.9em */
.text-100   /* 1em */
.text-xl    /* 1.05em */
.text-110   /* 1.1em */
.text-120   /* 1.2em */
.text-130   /* 1.3em */
.text-140   /* 1.4em */
.text-150   /* 1.5em */
.text-160   /* 1.6em */
.text-2xl   /* 2.5em */
.text-280   /* 2.8em */
.text-3xl   /* 3em */
```

## Colors

```css
.color-accent      /* Primary blue */
.color-green       /* Green */
.color-orange      /* Orange */
.color-red         /* Red */
.color-purple      /* Purple */
.color-lightblue   /* Light blue */
.color-black       /* #111 */
.color-dim         /* #999 - Gray */
.color-muted       /* #aaa - Medium gray */
.color-light       /* #ccc - Light gray */
.color-white       /* #fff */
```

## Border Colors

```css
.border-accent
.border-green
.border-orange
.border-red
.border-purple
.border-dim
```

## Combined Text Utilities

```css
.text-base-dim      /* 0.75em, #ccc */
.text-lg-dim        /* 0.9em, #ccc */
.text-080-dim       /* 0.8em, #999 */
.text-080-muted     /* 0.8em, #aaa */
.text-080-light     /* 0.8em, #ccc */
.text-sm-muted      /* 0.65em, #aaa */
.text-sm-light      /* 0.65em, #ccc */
.text-070-dim       /* 0.7em, #999 */
.text-070-light     /* 0.7em, #ccc */
.text-xs-muted      /* 0.55em, #aaa */
.text-060-muted     /* 0.6em, #aaa */
.text-110-accent    /* 1.1em, accent color */
.text-130-dim       /* 1.3em, #999 */
```

## Layout Classes

### Grid Layouts
```html
<!-- 2 columns -->
<div class="card-grid">
  <div class="card">...</div>
  <div class="card">...</div>
</div>

<!-- 3 columns -->
<div class="card-grid-3">
  <div class="card">...</div>
  <div class="card">...</div>
  <div class="card">...</div>
</div>

<!-- Alternative 2-column -->
<div class="two-col">
  <div>...</div>
  <div>...</div>
</div>

<!-- Alternative 3-column -->
<div class="three-col">
  <div>...</div>
  <div>...</div>
  <div>...</div>
</div>
```

## Cards

```html
<div class="card card-accent">
  <h4>Card Title</h4>
  <p>Card content</p>
</div>

<div class="card card-green">...</div>
<div class="card card-orange">...</div>
<div class="card card-red">...</div>
```

## Tags/Badges

```html
<span class="tag">Default</span>
<span class="tag-green">Green</span>
<span class="tag-orange">Orange</span>
<span class="tag-red">Red</span>
<span class="tag-success">Lab</span>
<span class="tag-warning">Quiz</span>
<span class="tag-danger">Error</span>
```

## Callouts

### Original Style (Detailed)
```html
<div class="takeaway">
  Automatically shows "Key Takeaway" label
</div>

<div class="tip-callout">
  Shows 💡 Tip label
</div>

<div class="warning-callout">
  Shows ⚠️ Warning label
</div>

<div class="note-callout">
  Shows 📝 Note label
</div>

<div class="error-callout">
  Shows Warning label in red
</div>

<div class="analogy">
  Shows "Think of it like..." label
</div>

<div class="answer-explain">
  For quiz answer explanations
</div>
```

### Alternative Style (Simple)
```html
<div class="highlight-box">
  Default highlight
</div>

<div class="highlight-box success">
  Success highlight
</div>

<div class="highlight-box warning">
  Warning highlight
</div>

<div class="highlight-box danger">
  Danger highlight
</div>
```

## Special Slide Types

```html
<!-- Title slide -->
<section class="title-slide">
  <h1>Course Title</h1>
  <p class="subtitle">Session 1 · Day 1</p>
  <p class="duration">90 minutes</p>
  <p class="branding">Trainer: Rajesh Gheware</p>
</section>

<!-- Lab slide -->
<section class="lab-slide">
  <h2>Hands-On Lab</h2>
  <div class="highlight-box">Lab instructions</div>
</section>

<!-- Quiz slide -->
<section class="quiz-slide">
  <h2>Knowledge Check</h2>
  <div class="quiz-badge">Quiz</div>
  <p class="quiz-question">Question text?</p>
  <div class="quiz-options">...</div>
</section>

<!-- Center-aligned slide -->
<section class="center-slide">
  <h2>Centered Title</h2>
  <p>Centered content</p>
</section>
```

## Diagrams

### Boxes and Arrows
```html
<div class="diagram">
  <div class="box">Input</div>
  <span class="arrow">→</span>
  <div class="box box-green">Process</div>
  <span class="arrow">→</span>
  <div class="box box-orange">Output</div>
</div>

<div class="diagram-vertical">
  <div class="box">Start</div>
  <span class="arrow-down">↓</span>
  <div class="box">End</div>
</div>
```

### Alternative Diagram Style
```html
<div class="diagram-box">Component 1</div>
<div class="diagram-arrow">↓</div>
<div class="diagram-box">Component 2</div>
```

### Pipe Flow
```html
<div class="pipe-flow">
  <div class="pipe-box">Input</div>
  <span class="pipe-sym">|</span>
  <div class="pipe-box pipe-box-green">Transform</div>
  <span class="pipe-sym">|</span>
  <div class="pipe-box pipe-box-orange">Output</div>
</div>
```

### Branch Diagram
```html
<div class="branch-diagram">
  <div class="branch-row">
    <div class="branch-node">Start</div>
  </div>
  <div class="branch-row">
    <span class="branch-arrow">↓</span>
  </div>
  <div class="branch-row">
    <div class="branch-node branch-node-green">Option 1</div>
    <div class="branch-node branch-node-orange">Option 2</div>
  </div>
</div>
```

## Tables

### Standard Comparison
```html
<table class="compare-table">
  <thead>
    <tr>
      <th>Feature</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Item 1</td>
      <td>Details</td>
    </tr>
  </tbody>
</table>
```

### Alternative Comparison
```html
<table class="comparison-alt">
  <!-- Same structure as above -->
</table>
```

## Code Blocks

### Inline Code
```html
Use the <code>npm install</code> command
```

### Code Blocks with Copy Button
```html
<div class="code-block-wrapper">
  <button class="copy-btn">Copy</button>
  <pre class="code-block">
const example = "code";
  </pre>
</div>
```

## Lists

### Standard Lists
```html
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
```

### Styled Lists (Alternative)
```html
<ul class="styled-list">
  <li>First level
    <ul>
      <li>Second level</li>
    </ul>
  </li>
</ul>
```

## Headings

```html
<!-- Standard -->
<h1>Main Title</h1>
<h2>Section Title</h2>
<h3>Subsection</h3>

<!-- With border -->
<h2 class="with-border">Section with Underline</h2>
```

## Navigation

```html
<!-- Home button (top-left) -->
<a href="index.html" class="home-btn">
  <svg>...</svg>
  Home
</a>

<!-- Index link (bottom-left) -->
<a href="index.html" class="index-link">← Index</a>
```

## Spacing Utilities

### Margins
```css
.mt-0, .mt-6, .mt-8, .mt-10, .mt-12, .mt-14, .mt-16, .mt-20, .mt-30
.mb-0, .mb-8, .mb-14, .mb-20
.mx-auto  /* Horizontal center */
```

### Padding
```css
.p-8, .p-10, .p-14, .p-16, .p-20, .p-24
```

### Other
```css
.w-full        /* 100% width */
.max-w-500     /* 500px max width */
.max-w-700     /* 700px max width */
.gap-sm        /* 8px gap */
.opacity-50    /* 50% opacity */
.border-thick  /* 3px border */
```

## Multi-Agent System Diagrams

```html
<!-- Supervisor Pattern -->
<div class="agent-hub">
  <div class="agent-supervisor">Supervisor</div>
  <div class="agent-arrows">
    <span>↙</span><span>↓</span><span>↘</span>
  </div>
  <div class="agent-workers">
    <div class="agent-worker">Worker 1</div>
    <div class="agent-worker agent-worker-orange">Worker 2</div>
    <div class="agent-worker agent-worker-red">Worker 3</div>
  </div>
</div>

<!-- Peer-to-Peer -->
<div class="peer-ring">
  <div class="peer-node">Agent 1</div>
  <span class="peer-connector">↔</span>
  <div class="peer-node peer-node-green">Agent 2</div>
  <span class="peer-connector">↔</span>
  <div class="peer-node peer-node-orange">Agent 3</div>
</div>

<!-- Handoff Flow -->
<div class="handoff-flow">
  <div class="handoff-agent">Agent A</div>
  <div class="handoff-arrow">→ handoff</div>
  <div class="handoff-agent handoff-agent-green">Agent B</div>
  <div class="handoff-arrow">→ handoff</div>
  <div class="handoff-agent handoff-agent-orange">Agent C</div>
</div>
```

## Quick Tips

1. **Prefer utility classes** over inline styles for font-size and color
2. **Use semantic colors** (.tag-success) for labs, (.tag-warning) for quizzes
3. **Combine classes** for complex styling: `class="card card-accent text-lg"`
4. **Use .with-border** on h2 for section separators
5. **Use .two-col or .three-col** for simple layouts without cards
6. **Use .highlight-box** for simple callouts, detailed callouts for complex messages
7. **Add .title-slide** to first slide for better title formatting
8. **Use var(--accent)** in custom styles to maintain theme consistency

## Browser Compatibility

All styles tested on:
- Chrome/Edge (Chromium)
- Firefox
- Safari

Scrollbar styling uses both WebKit and standard properties for maximum compatibility.
