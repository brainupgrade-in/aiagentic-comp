/* =============================================================
   Shared Presentation Scripts — Agentic AI Course
   Include in all session HTML files (before </body>):
     <script src="shared.js"></script>
   ============================================================= */

document.addEventListener('DOMContentLoaded', function() {

  // ── Index link (bottom-left corner) ──────────────────────────
  var link = document.createElement('a');
  link.className = 'index-link';
  link.href = 'index.html';
  link.textContent = '\u2302 Index';   // ⌂ Index
  document.querySelector('.reveal').appendChild(link);

  // ── Copy button on every .code-block ─────────────────────────
  document.querySelectorAll('.code-block').forEach(function(block) {
    if (block.parentElement.classList.contains('code-block-wrapper')) return;

    var wrapper = document.createElement('div');
    wrapper.className = 'code-block-wrapper';
    block.parentNode.insertBefore(wrapper, block);
    wrapper.appendChild(block);

    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      var text = block.innerText || block.textContent;
      navigator.clipboard.writeText(text).then(function() {
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function() {
          btn.textContent = 'Copy';
          btn.classList.remove('copied');
        }, 2000);
      }).catch(function() {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function() {
          btn.textContent = 'Copy';
          btn.classList.remove('copied');
        }, 2000);
      });
    });
    wrapper.appendChild(btn);
  });

});
