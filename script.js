function toggleContent(blockNumber) {
    var content = document.getElementById('content-' + blockNumber);
    content.classList.toggle('expanded');
}

// Load content via AJAX
function loadPage(pageUrl) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', pageUrl, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('content').innerHTML = xhr.responseText;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    };
    xhr.send();
}

// Handle navigation and history state
function navigate(pageUrl) {
    loadPageWithFallback(pageUrl);
    history.pushState({ page: pageUrl }, '', pageUrl);  // Push the state to history
}

// Automatically load appropriate page on initial load
window.onload = function() {
    const currentPath = location.pathname;
    let pageUrl;
    
    // Handle different URL patterns
    if (currentPath === '/' || currentPath.endsWith('/index.html') || currentPath === '') {
        pageUrl = '/home.html';
    } else if (currentPath.endsWith('.html')) {
        // Direct access to a page (e.g., /about.html, /pages/ml/stock_price_prediction.html)
        pageUrl = currentPath;
    } else {
        // Handle URLs without .html extension
        pageUrl = currentPath.endsWith('/') ? currentPath + 'index.html' : currentPath + '.html';
    }
    
    // Load the appropriate page content
    loadPageWithFallback(pageUrl);
    
    // Replace state for initial load so popstate works correctly
    history.replaceState({ page: pageUrl }, '', pageUrl);
};

// Enhanced page loading with fallback for missing pages
function loadPageWithFallback(pageUrl) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', pageUrl, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                document.getElementById('content').innerHTML = xhr.responseText;
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } else {
                // Page not found, load home page as fallback
                console.warn(`Page ${pageUrl} not found, loading home page`);
                loadPage('/home.html');
                // Update URL to reflect the actual loaded page
                history.replaceState({ page: '/home.html' }, '', '/home.html');
            }
        }
    };
    xhr.send();
}

// Handle back/forward navigation (popstate event)
window.onpopstate = function(event) {
    if (event.state && event.state.page) {
        loadPageWithFallback(event.state.page);  // Load the correct page content via AJAX
    } else {
        loadPageWithFallback('/home.html');  // Default to home page if no state is present
    }
};

async function runPython() {
    const inputValue = document.getElementById('userInput').value;
    try {
        const response = await fetch('https://dominicreichl.com/llm/run-python', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input_value: inputValue }),
        });
        const result = await response.json();

        if (response.ok) {
            document.getElementById('result').textContent = result.result;
        } else {
            document.getElementById('result').textContent = result.error;
        }
    } catch (error) {
        document.getElementById('result').textContent = 'Error: ' + error.message;
    }
}
