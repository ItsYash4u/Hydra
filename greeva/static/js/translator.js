// Ensure global access for the callback
window.googleTranslateElementInit = function () {
    try {
        new google.translate.TranslateElement({
            pageLanguage: 'en',
            includedLanguages: 'en,hi',
            autoDisplay: false
        }, 'google_translate_element');
        console.log("Google Translate Initialized");
    } catch (e) {
        console.error("Google Translate Init Error:", e);
    }
}

// Helper to trigger change event
function triggerTranslation(lang) {
    var combo = document.querySelector('.goog-te-combo');
    if (combo) {
        combo.value = lang;
        combo.dispatchEvent(new Event('change'));
    } else {
        // Fallback: If combo not found, maybe look inside the iframe?
        // But usually SIMPLE layout puts it in the div.
        console.warn("Google Translate widget not found. Retrying...");
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Event delegation for language switch
    document.body.addEventListener('click', function (e) {
        var target = e.target.closest('[data-translator-lang]');
        if (target) {
            e.preventDefault();
            var lang = target.getAttribute('data-translator-lang');

            // Check if widget is ready
            var combo = document.querySelector('.goog-te-combo');
            if (!combo) {
                alert("Translation service is loading. Please wait a moment and try again.");
                return;
            }

            // Update Topbar UI
            var label = document.getElementById('selected-language-text');
            if (label) {
                label.innerText = (lang === 'hi') ? 'HN' : 'EN';
            }

            // Trigger Google Translate
            triggerTranslation(lang);
        }
    });

    // Clean up Google's top bar frame if it appears
    var checkExist = setInterval(function () {
        var frame = document.querySelector('.goog-te-banner-frame');
        if (frame) {
            frame.style.display = 'none';
            document.body.style.top = '0px';
        }
    }, 1000);
});
