/* =============================================================
   Shared Presentation Scripts — Agentic AI Course
   Include in all session HTML files (before </body>):
     <script src="shared.js"></script>
   ============================================================= */

(function() {
  'use strict';

  // Constants
  const SELECTORS = {
    reveal: '.reveal',
    titleSlide: '.reveal .slides > section:first-child'
  };

  const SHORTCUTS_HINT = 'Use ← → to navigate · Press ? for shortcuts · Press F for fullscreen · Press S for speaker notes';

  /**
   * Creates and appends the index link to bottom-left corner
   */
  function createIndexLink(container) {
    const link = document.createElement('a');
    link.className = 'index-link';
    link.href = 'index.html';
    link.textContent = '⌂ Index';
    link.setAttribute('aria-label', 'Return to course index');
    container.appendChild(link);
  }

  /**
   * Adds keyboard shortcut hint to title slide
   */
  function addKeyboardHint(titleSlide) {
    const hint = document.createElement('p');
    hint.className = 'keyboard-hint';
    hint.style.cssText = 'font-size:0.45em; color:rgba(255,255,255,0.3); margin-top:16px; text-align:center;';
    hint.textContent = SHORTCUTS_HINT;
    hint.setAttribute('aria-label', 'Keyboard shortcuts help');
    titleSlide.appendChild(hint);
  }

  /**
   * Adds copy buttons to all code blocks
   */
  function addCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');

    codeBlocks.forEach((codeBlock) => {
      const pre = codeBlock.parentElement;

      // Skip if copy button already exists
      if (pre.querySelector('.copy-btn')) return;

      // Detect language from class (e.g., language-python, language-javascript)
      const languageClass = Array.from(codeBlock.classList).find(cls => cls.startsWith('language-'));
      const language = languageClass ? languageClass.replace('language-', '') : '';

      // Set language as data attribute for the ::before pseudo-element
      if (language) {
        pre.setAttribute('data-lang', language);
      }

      // Create copy button
      const copyBtn = document.createElement('button');
      copyBtn.className = 'copy-btn';
      copyBtn.textContent = 'Copy';
      copyBtn.setAttribute('aria-label', 'Copy code to clipboard');

      // Copy functionality
      copyBtn.addEventListener('click', async (e) => {
        e.preventDefault();

        const code = codeBlock.textContent;

        try {
          await navigator.clipboard.writeText(code);

          // Show success feedback
          copyBtn.textContent = 'Copied';
          copyBtn.classList.add('copied');

          // Reset after 2 seconds
          setTimeout(() => {
            copyBtn.textContent = 'Copy';
            copyBtn.classList.remove('copied');
          }, 2000);

        } catch (err) {
          console.error('Failed to copy code:', err);

          // Fallback for older browsers
          const textArea = document.createElement('textarea');
          textArea.value = code;
          textArea.style.position = 'fixed';
          textArea.style.left = '-999999px';
          document.body.appendChild(textArea);
          textArea.select();

          try {
            document.execCommand('copy');
            copyBtn.textContent = 'Copied';
            copyBtn.classList.add('copied');

            setTimeout(() => {
              copyBtn.textContent = 'Copy';
              copyBtn.classList.remove('copied');
            }, 2000);
          } catch (err2) {
            console.error('Fallback copy failed:', err2);
            copyBtn.textContent = 'Failed';

            setTimeout(() => {
              copyBtn.textContent = 'Copy';
            }, 2000);
          } finally {
            document.body.removeChild(textArea);
          }
        }
      });

      // Add button to pre element
      pre.appendChild(copyBtn);
    });
  }

  /**
   * Initialize presentation enhancements
   */
  function init() {
    const revealEl = document.querySelector(SELECTORS.reveal);
    if (!revealEl) return;

    // Add index link
    createIndexLink(revealEl);

    // Add keyboard hints on title slide
    const titleSlide = document.querySelector(SELECTORS.titleSlide);
    if (titleSlide) {
      addKeyboardHint(titleSlide);
    }

    // Add copy buttons to code blocks
    addCopyButtons();

    // Re-add copy buttons when Reveal.js triggers slide changes
    // (in case slides are dynamically loaded)
    if (typeof Reveal !== 'undefined') {
      Reveal.on('slidechanged', () => {
        addCopyButtons();
      });
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
