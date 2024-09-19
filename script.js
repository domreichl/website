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
    loadPage(pageUrl);
    history.pushState({ page: pageUrl }, '', pageUrl);  // Push the state to history
}

// Automatically load 'home.html' on initial load
window.onload = function() {
    const pageUrl = location.pathname.split("/").pop() || 'home.html';

    // Prevent reloading if the user is already on the home page
    if (pageUrl === 'index.html' || pageUrl === '') {
        loadPage('/home.html');
    } else {
        loadPage(pageUrl);
    }
    
    // Replace state for initial load so popstate works correctly
    history.replaceState({ page: pageUrl }, '', pageUrl);
};

// Handle back/forward navigation (popstate event)
window.onpopstate = function(event) {
    if (event.state && event.state.page) {
        loadPage(event.state.page);  // Load the correct page content via AJAX
    } else {
        loadPage('/home.html');  // Default to home page if no state is present
    }
};