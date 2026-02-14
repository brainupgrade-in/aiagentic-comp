/* =============================================================
   Shared Presentation Scripts — Agentic AI Course
   Include in all session HTML files (before </body>):
     <script src="shared.js"></script>
   ============================================================= */

document.addEventListener('DOMContentLoaded', function () {

  // ── Index link (bottom-left corner) ──────────────────────────
  var revealEl = document.querySelector('.reveal');
  if (revealEl) {
    var link = document.createElement('a');
    link.className = 'index-link';
    link.href = 'index.html';
    link.textContent = '\u2302 Index';   // ⌂ Index
    revealEl.appendChild(link);

    // ── Keyboard shortcut hint on title slide ───────────────────
    var titleSlide = document.querySelector('.reveal .slides > section:first-child');
    if (titleSlide) {
      var hint = document.createElement('p');
      hint.style.cssText = 'font-size:0.45em; color:rgba(255,255,255,0.3); margin-top:16px; text-align:center;';
      hint.textContent = 'Use \u2190 \u2192 to navigate \u00B7 Press ? for shortcuts \u00B7 Press F for fullscreen \u00B7 Press S for speaker notes';
      titleSlide.appendChild(hint);
    }
  }

});
