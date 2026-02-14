# Presentation Files — Agentic AI Course

This directory contains all presentation slides for the 5-day Agentic AI course, built with [Reveal.js](https://revealjs.com/).

## File Structure

```
presentation/
├── index.html                    # Course landing page with session links
├── template.html                 # Standard template for new sessions
├── session1-*.html              # Session 1 presentation
├── session2-*.html              # Session 2 presentation
├── ...                          # Sessions 3-15
├── shared.css                   # Shared styles for all sessions
├── shared.js                    # Shared JavaScript enhancements
├── reveal-init.js              # Reveal.js initialization config
└── README.md                    # This file
```

## Shared Resources

### 1. `shared.css` (1,315 lines)
Centralized stylesheet with:
- CSS variables for consistent theming
- Reveal.js overrides and 15-70-15 vertical layout
- Reusable components (cards, diagrams, callouts, quiz styles)
- Utility classes (typography, colors, spacing, layout)

**Usage:** Already included in all session HTML files via:
```html
<link rel="stylesheet" href="shared.css">
```

### 2. `shared.js` (66 lines)
JavaScript enhancements for all presentations:
- Adds index link (⌂ Index) to bottom-left corner
- Adds keyboard shortcut hints on title slide
- IIFE pattern for namespace isolation
- Accessibility improvements (aria-labels)

**Usage:** Already included in all session HTML files via:
```html
<script src="shared.js"></script>
```

### 3. `reveal-init.js` (NEW - 66 lines)
Standardized Reveal.js initialization config:
- Navigation settings (hash, slide numbers)
- Layout dimensions (1920×1080)
- Transitions and scaling
- Custom keyboard shortcuts (F for fullscreen)
- Plugin loading (Highlight, Notes, Search, Zoom)

**Usage:** Include after Reveal.js plugins:
```html
<script src="reveal-init.js"></script>
```

## Creating New Presentations

### Option 1: Use the Template
Copy `template.html` and customize:
```bash
cp template.html session16-new-topic.html
# Edit session16-new-topic.html
```

### Option 2: Standard HTML Structure
All session HTML files follow this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Session X: Your Title</title>

  <!-- Reveal.js CSS -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/reveal.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/theme/black.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/highlight/monokai.min.css">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap">

  <!-- Custom Styles -->
  <link rel="stylesheet" href="shared.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <!-- Your slides here -->
    </div>
  </div>

  <!-- Reveal.js Core -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/reveal.min.js"></script>

  <!-- Reveal.js Plugins -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/highlight/highlight.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/notes/notes.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/search/search.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/zoom/zoom.min.js"></script>

  <!-- Reveal.js Initialization -->
  <script src="reveal-init.js"></script>

  <!-- Custom Enhancements -->
  <script src="shared.js"></script>
</body>
</html>
```

## Migrating Existing Files

To use `reveal-init.js` in existing session files:

1. **Remove** the inline `<script>` block with `Reveal.initialize({...})`
2. **Add** `<script src="reveal-init.js"></script>` before `shared.js`

Example:
```diff
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.6.1/plugin/zoom/zoom.min.js"></script>
- <script>
-   Reveal.initialize({
-     hash: true,
-     slideNumber: 'c/t',
-     ...
-   });
- </script>
+ <script src="reveal-init.js"></script>
  <script src="shared.js"></script>
```

## Customization

### Reveal.js Configuration
Edit `reveal-init.js` to change global settings for all presentations:
- Slide dimensions (width/height)
- Transitions and timing
- Keyboard shortcuts
- Plugin configuration

### Styling
Edit `shared.css` to modify:
- Color scheme (CSS variables in `:root`)
- Component styles (cards, diagrams, callouts)
- Utility classes (spacing, typography)

### JavaScript Enhancements
Edit `shared.js` to add:
- Custom event handlers
- Navigation enhancements
- UI improvements

## Available CSS Components

### Layout
- `.card-grid` — 2-column card grid
- `.card-grid-3` — 3-column card grid
- `.diagram` — Horizontal flow diagrams
- `.diagram-vertical` — Vertical flow diagrams

### Cards
- `.card` — Base card style
- `.card-accent` — Blue accent border
- `.card-green` — Green accent border
- `.card-orange` — Orange accent border
- `.card-red` — Red accent border

### Callouts
- `.takeaway` — Key takeaway box (green)
- `.tip-callout` — 💡 Tip callout (green)
- `.warning-callout` — ⚠️ Warning callout (orange)
- `.note-callout` — 📝 Note callout (blue)
- `.error-callout` — Error/warning callout (red)
- `.analogy` — "Think of it like..." box (blue)

### Quiz Elements
- `.quiz-badge` — Quiz question badge
- `.quiz-question` — Question text
- `.quiz-options` — 2×2 grid of options
- `.quiz-option` — Individual option
- `.quiz-option.correct` — Correct answer highlight
- `.quiz-option.wrong` — Wrong answer (dimmed)
- `.answer-explain` — Answer explanation box

### Diagrams
- `.layer-stack` — Layered architecture diagram
- `.pipe-flow` — Pipeline flow diagram
- `.branch-diagram` — Branch/decision diagram
- `.evolution` — Timeline/evolution diagram
- `.agent-hub` — Multi-agent supervisor pattern
- `.peer-ring` — Peer-to-peer agent diagram

### Utilities
See `shared.css` lines 1250-1315 for complete utility class reference:
- Typography: `.text-xs`, `.text-sm`, `.text-base`, `.text-lg`, etc.
- Colors: `.color-accent`, `.color-green`, `.color-orange`, `.color-red`
- Spacing: `.mt-{size}`, `.mb-{size}`, `.p-{size}`
- Layout: `.w-full`, `.max-w-{size}`, `.text-center`, `.text-left`

## Keyboard Shortcuts

Default Reveal.js shortcuts:
- **Arrow keys** — Navigate slides
- **Space** — Next slide
- **?** — Show help overlay
- **S** — Speaker notes view
- **O** or **Esc** — Overview mode
- **B** or **.** — Pause/blackout

Custom shortcuts (via `reveal-init.js`):
- **F** — Toggle fullscreen

## Browser Compatibility

Tested on:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Performance Tips

1. **Images:** Use optimized images (WebP format, compressed)
2. **Code blocks:** Limit to ~50 lines per slide for readability
3. **Fragments:** Use sparingly to avoid performance issues
4. **Plugins:** Only load plugins you need

## Troubleshooting

### Slides don't scale properly
- Check that `width: 1920` and `height: 1080` in `reveal-init.js`
- Verify no inline CSS overriding Reveal.js transforms

### Custom styles not applying
- Ensure `shared.css` is loaded after Reveal.js CSS
- Check browser console for CSS syntax errors
- Verify class names match (case-sensitive)

### JavaScript errors
- Load `reveal-init.js` AFTER Reveal.js and plugins
- Load `shared.js` LAST
- Check browser console for specific error messages

### Fullscreen not working
- Press F key (custom shortcut)
- Or use Reveal.js menu → Fullscreen
- Browser must support Fullscreen API

## Contributing

When making changes to shared files:

1. **Test across all sessions** — Changes affect 15+ presentations
2. **Document in README** — Update this file for new features
3. **Maintain backwards compatibility** — Don't break existing slides
4. **Use semantic class names** — Follow existing naming conventions

## License

© Gheware UniGPS Solutions LLP, All Rights Reserved

---

**Last Updated:** 2026-02-14
**Reveal.js Version:** 4.6.1
**Total Sessions:** 15
