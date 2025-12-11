/**
 * BMECatDemo Frontend - Minimal JavaScript helpers
 */

// Modal functions
function openModal() {
    document.getElementById('product-modal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById('product-modal').classList.add('hidden');
    document.body.style.overflow = '';
}

// Close modal on escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
        hideAutocomplete();
    }
});

// Autocomplete functions
function selectSuggestion(suggestion) {
    const searchInput = document.getElementById('search-input');
    searchInput.value = suggestion;
    hideAutocomplete();
    // Trigger HTMX search
    htmx.trigger(searchInput, 'search');
}

function hideAutocomplete() {
    const autocomplete = document.getElementById('autocomplete-results');
    if (autocomplete) {
        autocomplete.classList.add('hidden');
        autocomplete.innerHTML = '';
    }
}

// Show autocomplete when results arrive
document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.detail.target.id === 'autocomplete-results') {
        const autocomplete = document.getElementById('autocomplete-results');
        if (autocomplete.innerHTML.trim()) {
            autocomplete.classList.remove('hidden');
        } else {
            autocomplete.classList.add('hidden');
        }
    }
});

// Hide autocomplete when clicking outside
document.addEventListener('click', function(event) {
    const autocomplete = document.getElementById('autocomplete-results');
    const searchInput = document.getElementById('search-input');

    if (autocomplete && searchInput) {
        if (!autocomplete.contains(event.target) && event.target !== searchInput) {
            hideAutocomplete();
        }
    }
});

// Hide autocomplete when search input loses focus (with delay for click handling)
document.getElementById('search-input')?.addEventListener('blur', function() {
    setTimeout(hideAutocomplete, 200);
});

// Scroll to top when pagination changes
document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.detail.target.id === 'results-container') {
        // Check if this was a pagination click (page parameter in URL)
        const requestUrl = event.detail.pathInfo?.requestPath || '';
        if (requestUrl.includes('page=')) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }
});
