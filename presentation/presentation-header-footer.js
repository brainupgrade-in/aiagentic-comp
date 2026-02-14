/**
 * Presentation Header & Footer - Auto-Update System
 * Cybernetic HUD Interface for Agentic AI Course
 *
 * Auto-extracts session info from page metadata and updates slide numbers
 */

(function() {
  'use strict';

  /**
   * Extract session number and day from the page title or meta tags
   * Examples: "Session 1: Introduction" -> { session: 1, day: 1 }
   *           "Session 13: Model Context Protocol" -> { session: 13, day: 5 }
   */
  function extractSessionInfo() {
    const title = document.title || '';
    const sessionMatch = title.match(/Session\s+(\d+)/i);

    if (sessionMatch) {
      const sessionNum = parseInt(sessionMatch[1], 10);
      // Map sessions to days: 1-3=Day1, 4-6=Day2, 7-9=Day3, 10-12=Day4, 13-15=Day5
      const day = Math.ceil(sessionNum / 3);
      return {
        session: sessionNum,
        day: day
      };
    }

    return { session: null, day: null };
  }

  /**
   * Create and inject header HTML
   */
  function createHeader() {
    const header = document.createElement('div');
    header.className = 'presentation-header';

    const sessionInfo = extractSessionInfo();
    const sessionDisplay = sessionInfo.session
      ? `<span class="header-session-label">Session</span> <span class="header-session-number">${sessionInfo.session}</span> · Day ${sessionInfo.day}`
      : '<span class="header-session-label">Session</span> <span class="header-session-number">--</span>';

    header.innerHTML = `
      <div class="header-left">
        <a href="index.html" class="header-home-btn" title="Back to Course Index">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <span>Home</span>
        </a>
      </div>
      <div class="header-center">
        <div class="header-course-title">Agentic AI</div>
      </div>
      <div class="header-right">
        <div class="header-session">
          ${sessionDisplay}
        </div>
        <div class="data-indicator"></div>
      </div>
      <!-- <div class="scan-line"></div> -->
    `;

    return header;
  }

  /**
   * Create and inject footer HTML
   */
  function createFooter() {
    const footer = document.createElement('div');
    footer.className = 'presentation-footer';

    footer.innerHTML = `
      <div class="footer-left">
        <div class="footer-slide-number">
          <span class="current">1</span>
          <span class="separator">/</span>
          <span class="total">--</span>
        </div>
      </div>
      <div class="footer-center">
        <div class="footer-trainer">
          <span class="footer-trainer-label">Trainer:</span> Rajesh Gheware
        </div>
      </div>
      <div class="footer-right">
        <div class="footer-branding">
          <div class="footer-branding-icon">B</div>
          <span>brainupgrade.in</span>
        </div>
        <div class="data-indicator"></div>
      </div>
    `;

    return footer;
  }

  /**
   * Update slide numbers in footer
   */
  function updateSlideNumbers(reveal) {
    const indices = reveal.getIndices();
    const totalSlides = reveal.getTotalSlides();

    // Use Reveal.js's getSlidePastCount if available (Reveal.js 4.0+)
    let currentSlide;
    if (typeof reveal.getSlidePastCount === 'function') {
      currentSlide = reveal.getSlidePastCount() + 1;
    } else {
      // Fallback: Calculate current slide number manually
      currentSlide = 0;
      const horizontalSlides = document.querySelectorAll('.reveal .slides>section');

      for (let h = 0; h < horizontalSlides.length; h++) {
        const horizontalSlide = horizontalSlides[h];
        const verticalSlides = horizontalSlide.querySelectorAll('section');

        if (h < indices.h) {
          // Count all slides in previous horizontal stacks
          currentSlide += verticalSlides.length > 0 ? verticalSlides.length : 1;
        } else if (h === indices.h) {
          // Count slides in current horizontal stack up to current vertical
          currentSlide += indices.v + 1;
          break;
        }
      }
    }

    const currentElem = document.querySelector('.footer-slide-number .current');
    const totalElem = document.querySelector('.footer-slide-number .total');

    if (currentElem) currentElem.textContent = currentSlide;
    if (totalElem) totalElem.textContent = totalSlides;
  }

  /**
   * Toggle header/footer visibility - Now always visible
   */
  function toggleHeaderFooterVisibility(reveal) {
    const header = document.querySelector('.presentation-header');
    const footer = document.querySelector('.presentation-footer');

    if (!header || !footer) return;

    // Always show header and footer on all slides
    header.style.opacity = '1';
    footer.style.opacity = '1';
    header.style.pointerEvents = 'auto';
    footer.style.pointerEvents = 'auto';
  }

  /**
   * Initialize header and footer
   */
  function init() {
    // Wait for Reveal.js to be ready
    if (typeof Reveal === 'undefined') {
      console.warn('Reveal.js not found. Header/Footer not initialized.');
      return;
    }

    Reveal.on('ready', function() {
      const revealContainer = document.querySelector('.reveal');

      if (!revealContainer) {
        console.warn('Reveal container not found.');
        return;
      }

      // Create and inject header and footer
      const header = createHeader();
      const footer = createFooter();

      revealContainer.appendChild(header);
      revealContainer.appendChild(footer);

      // Initial update
      updateSlideNumbers(Reveal);
      toggleHeaderFooterVisibility(Reveal);

      // Update on slide change
      Reveal.on('slidechanged', function() {
        updateSlideNumbers(Reveal);
        toggleHeaderFooterVisibility(Reveal);
      });

      console.log('✓ Presentation Header & Footer initialized');
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
