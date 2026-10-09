const loader = document.getElementById("loader");
const logo = document.getElementById("loader-logo");
const spinner = document.getElementById("spinner");

let logoLoaded = false;
let pageLoaded = false;

function checkLoading() {
    if (logoLoaded && pageLoaded) {
        loader.classList.add("hidden");
    }
}

// When the logo finishes loading
function onLogoReady() {
    if (logoLoaded) return;

    logoLoaded = true;
    loader.classList.add("logo-ready");
    logo.classList.add("pulse");

    checkLoading();
}

logo.addEventListener("load", onLogoReady, { once: true });

// Handle a logo that is already cached
if (logo.complete && logo.naturalWidth > 0) {
    onLogoReady();
}

// If the logo fails to load, avoid getting stuck
logo.addEventListener("error", () => {
    spinner.style.display = "block";
    console.error("Logo failed to load.");
});

// Wait until the rest of the page loads
window.addEventListener("load", () => {
    pageLoaded = true;
    checkLoading();
});
