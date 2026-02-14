/**
 * Cyberpunk Terminal Code Blocks Enhancement
 * Transforms code blocks into HUD-style terminal interfaces
 */

(function() {
  'use strict';

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    enhanceAllCodeBlocks();
    setupCopyButtons();
  }

  /**
   * Enhance all code blocks with cyberpunk terminal styling
   */
  function enhanceAllCodeBlocks() {
    const codeBlocks = document.querySelectorAll('.reveal pre');

    codeBlocks.forEach((pre, index) => {
      // Skip if already enhanced
      if (pre.classList.contains('enhanced')) return;

      pre.classList.add('enhanced');

      // Add scanline effect - DISABLED for cleaner look
      // const scanline = document.createElement('div');
      // scanline.className = 'scanline';
      // pre.appendChild(scanline);

      // Create terminal header
      const header = createTerminalHeader(pre, index);
      pre.insertBefore(header, pre.firstChild);

      // Add data stream effect (subtle)
      addDataStreamEffect(pre);
    });
  }

  /**
   * Create terminal header with language badge and status indicators
   */
  function createTerminalHeader(pre, index) {
    const header = document.createElement('div');
    header.className = 'terminal-header';

    // Language badge
    const langBadge = document.createElement('div');
    langBadge.className = 'lang-badge';

    // Extract language from data-lang attribute or code class
    const codeElement = pre.querySelector('code');
    let language = pre.getAttribute('data-lang') || '';

    if (!language && codeElement) {
      const classList = Array.from(codeElement.classList);
      const langClass = classList.find(cls => cls.startsWith('language-'));
      if (langClass) {
        language = langClass.replace('language-', '');
      }
    }

    langBadge.textContent = language || 'CODE';
    header.appendChild(langBadge);

    // Create copy button and add it to header
    const copyBtn = createCopyButton(codeElement);
    header.appendChild(copyBtn);

    // Status indicators
    const statusContainer = document.createElement('div');
    statusContainer.className = 'status-indicators';

    for (let i = 0; i < 3; i++) {
      const dot = document.createElement('div');
      dot.className = 'status-dot';
      statusContainer.appendChild(dot);
    }

    header.appendChild(statusContainer);

    return header;
  }

  /**
   * Add subtle data stream effect
   */
  function addDataStreamEffect(pre) {
    // Random characters streaming effect (very subtle)
    const codeElement = pre.querySelector('code');
    if (!codeElement) return;

    // Add on hover only to prevent performance issues
    pre.addEventListener('mouseenter', () => {
      if (!pre.dataset.streamActive) {
        pre.dataset.streamActive = 'true';
        // Effect is now pure CSS via holographic-shimmer animation
      }
    });
  }

  /**
   * Create a copy button for a code element
   */
  function createCopyButton(codeElement) {
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.textContent = 'COPY';
    copyBtn.setAttribute('aria-label', 'Copy code to clipboard');

    // Add click handler
    copyBtn.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const codeText = codeElement.textContent;

      try {
        await navigator.clipboard.writeText(codeText);

        // Success feedback
        copyBtn.textContent = 'COPIED';
        copyBtn.classList.add('copied');

        // Reset after delay
        setTimeout(() => {
          copyBtn.textContent = 'COPY';
          copyBtn.classList.remove('copied');
        }, 2000);

      } catch (err) {
        console.error('Failed to copy code:', err);

        // Fallback for older browsers
        fallbackCopyTextToClipboard(codeText, copyBtn);
      }
    });

    return copyBtn;
  }

  /**
   * Setup enhanced copy buttons for code blocks (legacy support)
   */
  function setupCopyButtons() {
    // Copy buttons are now added in createTerminalHeader
    // This function is kept for backwards compatibility
    // and handles any code blocks that might not have headers yet
    const codeBlocks = document.querySelectorAll('.reveal pre code');

    codeBlocks.forEach(code => {
      const pre = code.parentElement;
      const header = pre.querySelector('.terminal-header');

      // Skip if copy button already exists
      if (pre.querySelector('.copy-btn')) return;

      // If no header exists, skip (shouldn't happen after enhancement)
      if (!header) return;
    });
  }

  /**
   * Fallback copy method for browsers that don't support clipboard API
   */
  function fallbackCopyTextToClipboard(text, button) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      const successful = document.execCommand('copy');
      if (successful) {
        button.textContent = 'COPIED';
        button.classList.add('copied');

        setTimeout(() => {
          button.textContent = 'COPY';
          button.classList.remove('copied');
        }, 2000);
      }
    } catch (err) {
      console.error('Fallback copy failed:', err);
      button.textContent = 'FAILED';

      setTimeout(() => {
        button.textContent = 'COPY';
      }, 2000);
    }

    document.body.removeChild(textArea);
  }

  // Re-enhance code blocks when Reveal.js slides change
  // This handles dynamically loaded content
  if (window.Reveal) {
    Reveal.on('ready', () => {
      enhanceAllCodeBlocks();
      setupCopyButtons();
    });

    Reveal.on('slidechanged', () => {
      // Small delay to ensure content is rendered
      setTimeout(() => {
        enhanceAllCodeBlocks();
        setupCopyButtons();
      }, 100);
    });
  }

})();
