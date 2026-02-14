/* =============================================================
   Reveal.js Initialization — Agentic AI Course
   Standardized configuration for all presentation slides
   ============================================================= */

(function() {
  'use strict';

  // Reveal.js configuration
  const config = {
    // Navigation
    hash: true,
    slideNumber: 'c/t',
    showSlideNumber: 'all',

    // Transitions
    transition: 'slide',
    transitionSpeed: 'default',

    // Layout - Use responsive sizing for proper browser zoom support
    center: false,
    progress: true,
    width: '100%',
    height: '100%',
    margin: 0.02,

    // Scaling - Allow browser zoom to work naturally
    minScale: 0.1,
    maxScale: 4.0,
    disableLayout: false,

    // Custom keyboard shortcuts
    keyboard: {
      // F key toggles fullscreen
      70: function() {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(err => {
            console.warn('Fullscreen request failed:', err);
          });
        } else {
          document.exitFullscreen();
        }
      }
    },

    // Plugins
    plugins: [
      RevealHighlight,
      RevealNotes,
      RevealSearch,
      RevealZoom
    ]
  };

  // Initialize Reveal.js when DOM is ready
  function initReveal() {
    if (typeof Reveal !== 'undefined') {
      Reveal.initialize(config);
    } else {
      console.error('Reveal.js library not loaded');
    }
  }

  // Wait for DOM and Reveal.js to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initReveal);
  } else {
    initReveal();
  }

})();
