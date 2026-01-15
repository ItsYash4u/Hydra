// ============================================
// GLOBAL NAVIGATION ENHANCEMENT
// Ensures seamless navigation between all pages
// ============================================

(function () {
    'use strict';

    // Navigation state management
    const Navigation = {
        currentPage: null,

        init: function () {
            this.detectCurrentPage();
            this.setupNavigationListeners();
            this.handleBrowserNavigation();
            console.log('✅ Navigation system initialized');
        },

        detectCurrentPage: function () {
            const path = window.location.pathname;

            if (path.includes('/dashboard')) {
                this.currentPage = 'dashboard';
            } else if (path.includes('/analytics')) {
                this.currentPage = 'analytics';
            } else if (path.includes('/info')) {
                this.currentPage = 'info';
            } else if (path === '/' || path === '') {
                this.currentPage = 'dashboard';
            }

            console.log(`📍 Current page: ${this.currentPage}`);
        },

        setupNavigationListeners: function () {
            // Add click handlers to sidebar links
            document.querySelectorAll('.side-nav-link').forEach(link => {
                link.addEventListener('click', function (e) {
                    // Let the default navigation happen
                    // Just log for debugging
                    const href = this.getAttribute('href');
                    console.log(`🔗 Navigating to: ${href}`);
                });
            });
        },

        handleBrowserNavigation: function () {
            // Handle browser back/forward buttons
            window.addEventListener('popstate', function (event) {
                console.log('⬅️ Browser back/forward navigation detected');
                // Page will reload automatically with correct content
            });
        },

        updateActiveState: function () {
            // Remove active class from all links
            document.querySelectorAll('.side-nav-link').forEach(link => {
                link.classList.remove('active');
            });

            // Add active class to current page link
            const path = window.location.pathname;
            document.querySelectorAll('.side-nav-link').forEach(link => {
                const href = link.getAttribute('href');
                if (href && path.includes(href.split('/').pop())) {
                    link.classList.add('active');
                }
            });
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            Navigation.init();
        });
    } else {
        Navigation.init();
    }

    // Expose for debugging
    window.Navigation = Navigation;

})();

// ============================================
// ERROR HANDLING & FALLBACK
// ============================================

window.addEventListener('error', function (e) {
    // Log errors but don't break navigation
    console.error('Navigation error:', e.message);
});

// Prevent navigation loops
let navigationCount = 0;
const originalPushState = history.pushState;
history.pushState = function () {
    navigationCount++;
    if (navigationCount > 10) {
        console.warn('⚠️ Too many navigation attempts, possible loop detected');
        navigationCount = 0;
        return;
    }
    return originalPushState.apply(history, arguments);
};

// Reset counter after 2 seconds
setInterval(function () {
    navigationCount = 0;
}, 2000);

console.log('✅ Global navigation script loaded');
