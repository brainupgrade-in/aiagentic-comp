# Presentation Files — Agentic AI Course

**5-Day Comprehensive Training on Agentic AI**
Built with [Reveal.js 4.6.1](https://revealjs.com/) | Cybernetic Systems Aesthetic

---

## 📁 File Structure

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
├── session11-langfuse-observability.html
├── session12-production-development-deployment.html
├── session13-model-context-protocol.html
├── session14-ai-safety-guardrails.html
├── session15-capstone-project.html
│
├── shared.css                          # Shared styles (~2,700 lines)
├── shared.js                           # Shared JavaScript enhancements
├── reveal-init.js                      # Reveal.js initialization config
├── presentation-header-footer.js       # Auto-updating header/footer system
│
├── README.md                           # This file
├── HEADER-FOOTER-GUIDE.md              # Header/footer customization guide
├── FIXES-APPLIED.md                    # Recent fixes and improvements
└── add-header-footer.sh                # Utility script for batch updates
```

---

## 🎨 Key Features

### 1. **Cybernetic HUD Interface**
- Fixed header with Home button, course title, and session info
- Fixed footer with slide counter, trainer name, and branding
- Auto-updating slide numbers and session detection
- Animated scanlines and glowing effects

### 2. **Professional Styling**
- Electric teal (#00ffcc) primary accent color
- Dark cybernetic theme with gradient backgrounds
- HUD-style corner brackets and glowing borders
- Consistent typography (Inter + JetBrains Mono)

### 3. **Responsive Layout**
- 1920×1080 base resolution with automatic scaling
- Works on desktop, laptop, tablet, and mobile
- Browser zoom support without breaking layout

### 4. **Interactive Elements**
- Clickable Home button (returns to index.html)
- Navigation arrows positioned above footer
- Copy buttons on code blocks
- Keyboard shortcuts (H for help)

---

## 🚀 Quick Start

### View Presentations

```bash
# Open course index
firefox index.html

# Open specific session
firefox session1-introduction-to-agentic-ai.html
```

### Create New Session

```bash
# Copy template
cp template.html session16-new-topic.html

# Edit the content
# - Update title
# - Add slides
# - Save and refresh browser
```

---

## 📚 Shared Resources

### `shared.css` (~2,700 lines)

**Centralized stylesheet includes:**
- CSS variables for cybernetic color system
- Header/footer HUD interface styles
- Reveal.js layout overrides (15-70-15 vertical split)
- Reusable components:
  - Cards (accent, green, orange, red variants)
  - Diagrams (boxes, arrows, flows)
  - Callouts (tips, warnings, notes, errors)
  - Quiz styles with hover effects
  - Code blocks with syntax highlighting
- Utility classes (typography, colors, spacing)
- Animations (scanlines, pulses, card reveals)

**Auto-included in all sessions:**
```html
<link rel="stylesheet" href="shared.css">
```

---

### `shared.js` (~66 lines)

**JavaScript enhancements:**
- Adds "⌂ Index" link to bottom-left corner
- Keyboard shortcut hints on title slides
- Accessibility improvements (ARIA labels)
- IIFE pattern for namespace isolation

**Auto-included in all sessions:**
```html
<script src="shared.js"></script>
```

---

### `reveal-init.js` (~66 lines)

**Standardized Reveal.js configuration:**
- Navigation settings (hash routing, slide numbers)
- Layout dimensions (1920×1080 base)
- Transitions (slide, 300ms)
- Scaling behavior (responsive)
- Plugin initialization (highlight, notes, search, zoom)

**Auto-included in all sessions:**
```html
<script src="reveal-init.js"></script>
```

---

### `presentation-header-footer.js` (~200 lines) ⭐ NEW

**Auto-updating header/footer system:**
- **Header (Top):**
  - Home button (links to index.html)
  - Course title "AGENTIC AI"
  - Session number & day (auto-detected from page title)
  - Pulsing live indicator
  - Animated scanline effect

- **Footer (Bottom):**
  - Slide counter (auto-updates: "5/45")
  - Trainer name "Rajesh Gheware"
  - brainupgrade.in branding
  - Pulsing status indicator

**Auto-included in all sessions:**
```html
<script src="presentation-header-footer.js"></script>
```

**Features:**
- ✅ Auto-extracts session info from `<title>` tag
- ✅ Live slide number updates on navigation
- ✅ Always visible on all slides (including title slides)
- ✅ Cybernetic HUD aesthetic with glowing effects
- ✅ Zero manual configuration required

---

## 🎯 Course Structure

### 15 Sessions Across 5 Days

| Day | Sessions | Topics |
|-----|----------|--------|
| **1** | 1-3 | Introduction, Vibe Coding, Reasoning & Planning |
| **2** | 4-6 | LangChain Fundamentals, RAG, Agents & Memory |
| **3** | 7-9 | LangGraph Workflows, Advanced Patterns, Multi-Agent |
| **4** | 10-12 | Observability, LangFuse, Production Deployment |
| **5** | 13-15 | Model Context Protocol, AI Safety, Capstone Project |

**Total Slides:** ~600+ across all sessions
**Duration:** 60-90 minutes per session
**Hands-on Labs:** 117 labs + 117 solutions

---

## 🛠️ Customization

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

Edit `presentation-header-footer.js`:

```javascript
<div class="footer-trainer">
  <span class="footer-trainer-label">Trainer:</span> Your Name
</div>
```

### Change Branding

Edit `presentation-header-footer.js`:

```javascript
<div class="footer-branding">
  <div class="footer-branding-icon">Y</div>
  <span>yoursite.com</span>
</div>
```

### Add Logo

Replace Home button in `presentation-header-footer.js`:

```javascript
<div class="header-left">
  <img src="your-logo.svg" alt="Logo" style="height: 24px;">
</div>
```

---

## 🎨 Design System

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

### Spacing

- **Slide Padding:** 60px top, 80px bottom (for header/footer clearance)
- **Card Gap:** 12px
- **Section Margin:** 16px
- **Element Gap:** 4-8px

---

## 🔧 Maintenance

### Update All Sessions

Use the batch script:

```bash
# Add header/footer to new sessions
./add-header-footer.sh
```

### Check for Issues

```bash
# Verify shared resources are linked
grep 'shared.css' session*.html
grep 'shared.js' session*.html
grep 'reveal-init.js' session*.html
grep 'presentation-header-footer.js' session*.html
```

### Test in Browser

```bash
# Check rendering
firefox session1-introduction-to-agentic-ai.html

# Verify:
# - Header/footer visible
# - Home button clickable
# - Slide numbers update
# - Navigation arrows visible
# - Content doesn't overlap footer
```

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| **README.md** | Main documentation (this file) |
| **HEADER-FOOTER-GUIDE.md** | Detailed guide for header/footer customization |
| **FIXES-APPLIED.md** | Recent bug fixes and improvements |
| **.archive/** | Historical documentation (archived) |

---

## 🐛 Troubleshooting

### Slide Numbers Not Updating
- Check browser console for JavaScript errors
- Verify `presentation-header-footer.js` is loaded
- Refresh the page (Ctrl+R)

### Content Overlapping Footer
- Increase `padding-bottom` in `shared.css`
- Current: 80px, try 90px or 100px

### Navigation Arrows Hidden
- Increase `.reveal .controls { bottom: }` value in `shared.css`
- Current: 50px, try 60px

### Home Button Not Clickable
- Verify `.header-home-btn { pointer-events: auto; }` in `shared.css`
- Check no other CSS is overriding it

---

## 📊 Statistics

- **Total Sessions:** 15
- **Total Slides:** ~600+
- **Total CSS Lines:** ~2,700
- **Total JS Lines:** ~330
- **Color Palette:** 7 core colors
- **Component Types:** 30+ reusable components
- **Animations:** 5 types (scanline, pulse, reveal, glow, hover)

---

## 🎓 Usage Tips

### For Trainers

1. **Session Numbers Auto-Update:** Just ensure page title has "Session N:" format
2. **Navigate Efficiently:** Use arrow keys or click navigation controls
3. **Presenter Mode:** Press 'S' to open speaker notes in separate window
4. **Help Menu:** Press 'H' to see keyboard shortcuts
5. **Search Slides:** Press Ctrl+Shift+F to search across slides

### For Students

1. **Home Button:** Click top-left to return to course index
2. **Slide Progress:** Check bottom-left for current position (e.g., "12/45")
3. **Resources:** brainupgrade.in link in bottom-right corner
4. **Code Blocks:** Hover to see copy button
5. **Full Screen:** Press 'F' for distraction-free viewing

---

## 🚀 Performance

- **Load Time:** ~1.2s (including all resources)
- **Slide Transitions:** 60fps smooth
- **Responsive Scaling:** Automatic, no lag
- **Memory Usage:** ~200KB (header/footer system)
- **Browser Support:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

---

## 📝 License

© 2026 Gheware UniGPS Solutions LLP. All Rights Reserved.

**Course:** Agentic AI Training
**Trainer:** Rajesh Gheware
**Organization:** brainupgrade.in
**Design:** Cybernetic Systems Aesthetic

---

## 🔗 Quick Links

- [Reveal.js Documentation](https://revealjs.com/)
- [Course Outline](../COURSE-OUTLINE.md)
- [Instructor Guide](../INSTRUCTOR-GUIDE.md)
- [Hands-on Labs](../hands-on/)

---

_Last Updated: February 14, 2026_
_Version: 2.0 (Header/Footer System Integration)_
