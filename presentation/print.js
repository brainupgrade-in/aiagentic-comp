/* =============================================================
   PRINT JAVASCRIPT HELPERS — Agentic AI Course Presentations
   Enhances print functionality with auto-expand and utilities
   ============================================================= */

(function() {
  'use strict';

  /* =============================================================
     CONFIGURATION
     ============================================================= */
  const CONFIG = {
    // Auto-add print button to slides
    addPrintButton: true,

    // Auto-expand all nested slides before printing
    autoExpandForPrint: true,

    // Show print preview dialog
    showPrintDialog: true,

    // Print button text
    printButtonText: 'Print Slides',

    // Keyboard shortcut for print (Ctrl+P is browser default)
    printShortcut: 'ctrl+shift+p'
  };

  /* =============================================================
     PRINT BUTTON - Add floating print button to presentations
     ============================================================= */
  function addPrintButton() {
    // Don't add button if already in print media or if disabled
    if (window.matchMedia('print').matches || !CONFIG.addPrintButton) {
      return;
    }

    // Check if button already exists
    if (document.querySelector('.print-button')) {
      return;
    }

    const printButton = document.createElement('button');
    printButton.className = 'print-button no-print screen-only';
    printButton.textContent = CONFIG.printButtonText;
    printButton.setAttribute('aria-label', 'Print presentation slides');
    printButton.setAttribute('title', 'Print this presentation (Ctrl+Shift+P)');

    printButton.addEventListener('click', handlePrint);

    document.body.appendChild(printButton);
    console.log('[Print] Print button added to presentation');
  }

  /* =============================================================
     EXPAND SLIDES - Flatten nested vertical slides for printing
     ============================================================= */
  function expandAllSlides() {
    if (!CONFIG.autoExpandForPrint) {
      return;
    }

    const slides = document.querySelectorAll('.reveal .slides section');

    slides.forEach(section => {
      // Make all sections visible (override Reveal.js display:none)
      section.style.display = 'block';
      section.style.visibility = 'visible';
      section.style.opacity = '1';

      // Remove transforms
      section.style.transform = 'none';

      // Ensure nested sections are also visible
      const nestedSections = section.querySelectorAll('section');
      nestedSections.forEach(nested => {
        nested.style.display = 'block';
        nested.style.visibility = 'visible';
        nested.style.opacity = '1';
        nested.style.transform = 'none';
      });
    });

    console.log(`[Print] Expanded ${slides.length} slides for printing`);
  }

  /* =============================================================
     PREPARE FOR PRINT - Clean up dynamic content
     ============================================================= */
  function prepareForPrint() {
    console.log('[Print] Preparing presentation for printing...');

    // Expand all slides
    expandAllSlides();

    // Remove any animations/transitions that might interfere
    const reveal = document.querySelector('.reveal');
    if (reveal) {
      reveal.style.transition = 'none';
    }

    // Ensure all code blocks are visible
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(code => {
      code.style.maxHeight = 'none';
      code.style.overflow = 'visible';
    });

    // Show all images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
      img.style.opacity = '1';
      img.style.visibility = 'visible';
    });

    // Expand any collapsed elements
    const details = document.querySelectorAll('details');
    details.forEach(detail => {
      detail.setAttribute('open', '');
    });

    console.log('[Print] Preparation complete');
  }

  /* =============================================================
     HANDLE PRINT - Main print function
     ============================================================= */
  function handlePrint(event) {
    if (event) {
      event.preventDefault();
    }

    console.log('[Print] Initiating print...');

    // Prepare the document
    prepareForPrint();

    // Small delay to ensure DOM updates are complete
    setTimeout(() => {
      if (CONFIG.showPrintDialog) {
        window.print();
      } else {
        console.log('[Print] Print dialog disabled in config');
      }
    }, 100);
  }

  /* =============================================================
     KEYBOARD SHORTCUTS
     ============================================================= */
  function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ctrl+Shift+P
      if (e.ctrlKey && e.shiftKey && e.key === 'P') {
        e.preventDefault();
        handlePrint();
      }
    });

    console.log('[Print] Keyboard shortcuts registered (Ctrl+Shift+P)');
  }

  /* =============================================================
     BEFORE PRINT EVENT - Browser native print event
     ============================================================= */
  function setupPrintEvents() {
    window.addEventListener('beforeprint', () => {
      console.log('[Print] Before print event fired');
      prepareForPrint();
    });

    window.addEventListener('afterprint', () => {
      console.log('[Print] After print event fired');
      // Optionally restore state here if needed
    });

    console.log('[Print] Print event listeners registered');
  }

  /* =============================================================
     GET SESSION INFO - Extract session details for print header
     ============================================================= */
  function getSessionInfo() {
    const titleElement = document.querySelector('title');
    if (!titleElement) {
      return { session: 'Unknown', title: 'Agentic AI Course' };
    }

    const titleText = titleElement.textContent;
    const match = titleText.match(/Session (\d+):\s*(.+)/i);

    if (match) {
      return {
        session: `Session ${match[1]}`,
        title: match[2].trim()
      };
    }

    return {
      session: 'Agentic AI',
      title: titleText
    };
  }

  /* =============================================================
     ADD PRINT METADATA - Inject metadata for better print output
     ============================================================= */
  function addPrintMetadata() {
    const sessionInfo = getSessionInfo();

    // Add meta tags for print
    const metaTags = [
      { name: 'print-date', content: new Date().toLocaleDateString() },
      { name: 'print-session', content: sessionInfo.session },
      { name: 'print-title', content: sessionInfo.title },
      { name: 'author', content: 'Rajesh Gheware' },
      { name: 'organization', content: 'brainupgrade.in' }
    ];

    metaTags.forEach(tag => {
      const meta = document.createElement('meta');
      meta.name = tag.name;
      meta.content = tag.content;
      document.head.appendChild(meta);
    });

    console.log('[Print] Metadata added:', sessionInfo);
  }

  /* =============================================================
     PRINT UTILITIES - Helper functions
     ============================================================= */
  const PrintUtils = {
    // Check if print media query is active
    isPrintMode: () => window.matchMedia('print').matches,

    // Get total slide count
    getSlideCount: () => {
      return document.querySelectorAll('.reveal .slides section').length;
    },

    // Get current date formatted for print
    getPrintDate: () => {
      const now = new Date();
      return now.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },

    // Export to PDF (browser native)
    exportToPDF: () => {
      console.log('[Print] Triggering PDF export...');
      handlePrint();
    },

    // Print current slide only (if needed)
    printCurrentSlide: () => {
      console.warn('[Print] Print current slide only - not yet implemented');
      // This would require hiding all other slides temporarily
    }
  };

  /* =============================================================
     INITIALIZATION
     ============================================================= */
  function init() {
    console.log('[Print] Initializing print system...');

    // Wait for Reveal.js to be ready
    if (typeof Reveal !== 'undefined') {
      Reveal.on('ready', () => {
        console.log('[Print] Reveal.js ready, setting up print features');
        addPrintButton();
        setupKeyboardShortcuts();
        setupPrintEvents();
        addPrintMetadata();
      });
    } else {
      // Reveal.js not loaded, setup anyway
      document.addEventListener('DOMContentLoaded', () => {
        console.log('[Print] DOM ready (Reveal.js not detected)');
        addPrintButton();
        setupKeyboardShortcuts();
        setupPrintEvents();
        addPrintMetadata();
      });
    }

    console.log('[Print] Print system initialized');
  }

  /* =============================================================
     EXPOSE PUBLIC API
     ============================================================= */
  window.RevealPrint = {
    print: handlePrint,
    expand: expandAllSlides,
    prepare: prepareForPrint,
    utils: PrintUtils,
    config: CONFIG
  };

  /* =============================================================
     AUTO-INIT
     ============================================================= */
  init();

})();

/* =============================================================
   USAGE EXAMPLES
   ============================================================= */
/*

// Manual print trigger from console:
window.RevealPrint.print();

// Expand all slides manually:
window.RevealPrint.expand();

// Get slide count:
window.RevealPrint.utils.getSlideCount();

// Disable auto print button:
window.RevealPrint.config.addPrintButton = false;

// Print via keyboard:
// Press Ctrl+Shift+P

*/
