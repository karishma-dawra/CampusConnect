const username = document.getElementById("username");

username.addEventListener("invalid", function () {
    if (username.validity.valueMissing) {
        username.setCustomValidity("Please enter your username.");
    }
    else if (username.validity.patternMismatch) {
        username.setCustomValidity("Enter your 10-digit roll number.");
    }
});

username.addEventListener("input", function () {
    username.setCustomValidity("");
});


// _________________________________________________________________________

const password = document.getElementById("password");

password.addEventListener("input", function () {
    if (password.value.length < 8) {
        password.setCustomValidity("Password must contain at least 8 characters.");
    } else {
        password.setCustomValidity("");
    }

});
