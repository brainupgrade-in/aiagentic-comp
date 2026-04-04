# Presentation Files — Agentic AI Course

**5-Day Comprehensive Training on Agentic AI**
Built with [Reveal.js 4.6.1](https://revealjs.com/) | Cybernetic Systems Aesthetic

---

## File Structure

```
presentation/
├── index.html                          # Course landing page with all session links
├── template.html                       # Template for creating new sessions
│
├── session1-introduction-to-agentic-ai.html
├── session2-ai-coding-assistants-vibe-coding.html
├── session3-reasoning-planning-tool-use.html
├── session4-langchain-fundamentals.html
├── session5-building-rag-applications.html
├── session6-langchain-agents-memory.html
├── session7-langgraph-stateful-workflows.html
├── session8-advanced-langgraph-workflows.html
├── session9-multi-agent-systems.html
├── session10-observability-fundamentals.html
├── session11-production-development-deployment.html
├── session12-langfuse-observability.html
├── session13-model-context-protocol.html
├── session14-ai-safety-guardrails.html
├── session15-capstone-project.html
│
├── shared.css                          # Shared styles (~2,700 lines)
├── shared.js                           # Shared JavaScript enhancements
├── reveal-init.js                      # Reveal.js initialization config
├── presentation-header-footer.js       # Auto-updating header/footer system
├── code-blocks-enhanced.js             # Cyberpunk terminal code block enhancements
│
├── print.css                           # Print stylesheet (~1,000 lines)
├── print.js                            # Print helper functions (~400 lines)
├── performance-optimizations.css       # Performance tuning styles
│
└── README.md                           # This file
```

---

## Key Features

### Cybernetic HUD Interface
- Fixed header with Home button, course title, and session info
- Fixed footer with slide counter, trainer name, and branding
- Auto-updating slide numbers and session detection
- Animated scanlines and glowing effects

### Professional Styling
- Electric teal (#00ffcc) primary accent color
- Dark cybernetic theme with gradient backgrounds
- HUD-style corner brackets and glowing borders
- Consistent typography (Inter + JetBrains Mono)

### Responsive Layout
- 1920×1080 base resolution with automatic scaling
- Works on desktop, laptop, tablet, and mobile
- Browser zoom support without breaking layout

### Interactive Elements
- Clickable Home button (returns to index.html)
- Navigation arrows positioned above footer
- Copy buttons on code blocks
- Keyboard shortcuts (H for help)

### Print Support
- Print-optimized layout showing all slides vertically
- High-contrast colors optimized for paper/PDF export
- Smart page breaks between sections
- Print button in bottom-right corner (screen only)
- Keyboard shortcuts: Ctrl+Shift+P or Ctrl+P

---

## Quick Start

### View Presentations

```bash
# Open course index
firefox index.html

# Open specific session
firefox session1-introduction-to-agentic-ai.html
```

### Print Presentations

```bash
# Method 1: Click the Print button (bottom-right corner)
# Method 2: Press Ctrl+Shift+P (custom shortcut)
# Method 3: Press Ctrl+P (browser default)
# All slides appear in print preview with professional layout
```

### Create New Session

```bash
# Copy template
cp template.html session16-new-topic.html
# Edit the content — update title, add slides, save and refresh browser
```

---

## Shared Resources

### `shared.css` (~2,700 lines)

Centralized stylesheet including CSS variables for the cybernetic color system, header/footer HUD interface styles, Reveal.js layout overrides, and 30+ reusable components (cards, diagrams, callouts, quiz styles, code blocks).

Auto-included in all sessions:
```html
<link rel="stylesheet" href="shared.css">
```

### `shared.js` (~66 lines)

JavaScript enhancements: index link, keyboard shortcuts, accessibility improvements.

```html
<script src="shared.js"></script>
```

### `reveal-init.js` (~66 lines)

Standardized Reveal.js configuration: navigation, layout (1920×1080), transitions, plugins.

```html
<script src="reveal-init.js"></script>
```

### `presentation-header-footer.js` (~200 lines)

Auto-updating header/footer system. Extracts session info from `<title>`, updates slide counter live, shows trainer name and branding. Zero manual configuration required.

```html
<script src="presentation-header-footer.js"></script>
```

### `code-blocks-enhanced.js`

Cyberpunk terminal code block enhancements: HUD-style corner brackets, terminal header bars, animated scanlines, copy buttons.

```html
<script src="code-blocks-enhanced.js"></script>
```

---

## Course Structure

### 15 Sessions Across 5 Days

| Day | Sessions | Topics |
|-----|----------|--------|
| **1** | 1-3 | Introduction, Vibe Coding, Reasoning & Planning |
| **2** | 4-6 | LangChain Fundamentals, RAG, Agents & Memory |
| **3** | 7-9 | LangGraph Workflows, Advanced Patterns, Multi-Agent |
| **4** | 10-12 | Observability, Production Deployment, LangFuse |
| **5** | 13-15 | Model Context Protocol, AI Safety, Capstone Project |

**Total Slides:** ~600+ across all sessions
**Duration:** 60-90 minutes per session
**Hands-on Labs:** 119 labs + 119 solutions

---

## Customization

### Change Colors

Edit CSS variables in `shared.css`:

```css
:root {
  --accent: #00ffcc;       /* Electric teal - change to your brand color */
  --accent2: #ff6b35;      /* Neon orange */
  --accent3: #a855f7;      /* Deep purple */
  --accent4: #f43f5e;      /* Rose red */
}
```

### Change Trainer Name

Edit `presentation-header-footer.js` — find the `footer-trainer` div and update the name.

### Change Branding

Edit `presentation-header-footer.js` — find the `footer-branding` div and update the site name.

---

## Design System

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Electric Teal | #00ffcc | Primary accent, glows, borders |
| Neon Orange | #ff6b35 | Secondary accent, warnings |
| Deep Purple | #a855f7 | Tertiary accent, highlights |
| Rose Red | #f43f5e | Danger, errors |
| Deep Dark | #0a0f1a | Background base |
| Primary Text | #e0e6ed | Main content |
| Muted Text | #8899aa | Secondary labels |

### Typography

| Purpose | Font | Weight | Size |
|---------|------|--------|------|
| Headings | Inter | 700 | 2.2em (h1), 1.6em (h2) |
| Body Text | Inter | 400 | 0.75-0.85em |
| Code/Data | JetBrains Mono | 400-600 | 0.8em |
| Monospace UI | JetBrains Mono | 600 | 11-13px |

---

## Maintenance

### Verify Shared Resources

```bash
# Verify shared resources are linked in all sessions
grep 'shared.css' session*.html
grep 'shared.js' session*.html
grep 'reveal-init.js' session*.html
grep 'presentation-header-footer.js' session*.html
```

### Test in Browser

```bash
firefox session1-introduction-to-agentic-ai.html
# Verify: header/footer visible, Home button clickable,
# slide numbers update, navigation arrows visible
```

---

## Troubleshooting

### Slide Numbers Not Updating
- Check browser console for JavaScript errors
- Verify `presentation-header-footer.js` is loaded
- Refresh the page (Ctrl+R)

### Content Overlapping Footer
- Increase `padding-bottom` in `shared.css` (current: 80px, try 90-100px)

### Navigation Arrows Hidden
- Increase `.reveal .controls { bottom: }` in `shared.css` (current: 50px, try 60px)

### Home Button Not Clickable
- Verify `.header-home-btn { pointer-events: auto; }` in `shared.css`

---

## Usage Tips

### For Trainers

1. Session numbers auto-update — ensure page title has "Session N:" format
2. Navigate with arrow keys or click navigation controls
3. Press 'S' to open speaker notes in a separate window
4. Press 'H' to see keyboard shortcuts
5. Press Ctrl+Shift+F to search across slides

### For Students

1. Home button in top-left returns to the course index
2. Slide progress shown at bottom-left (e.g., "12/45")
3. Hover over code blocks to see copy button
4. Press 'F' for full-screen viewing

---

## License

© 2026 Gheware UniGPS Solutions LLP. All Rights Reserved.
