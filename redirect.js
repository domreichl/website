// SPA Redirect Handler
// Redirects direct page access to the main SPA
(function() {
    // Check if this page is being accessed directly (not loaded via SPA)
    if (!document.getElementById('content')) {
        // Redirect to home page and then navigate to the correct page
        const currentPath = window.location.pathname;
        window.location.href = '/';
        
        // After redirect, navigate to the intended page
        setTimeout(() => {
            history.replaceState({ page: currentPath }, '', currentPath);
            if (typeof navigate === 'function') {
                navigate(currentPath);
            }
        }, 100);
    }
})();