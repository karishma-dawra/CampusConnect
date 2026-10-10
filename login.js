
const email = document.getElementById("email");

if (email) {
    email.addEventListener("invalid", function () {
        if (email.validity.valueMissing) {
            email.setCustomValidity("Please enter your college email.");
        } else if (email.validity.typeMismatch) {
            email.setCustomValidity("Please enter a valid email address.");
        }
    });

    email.addEventListener("input", function () {
        email.setCustomValidity("");
    });
}

const password = document.getElementById("password");

if (password) {
    password.addEventListener("input", function () {
        if (password.value.length < 8) {
            password.setCustomValidity("Password must contain at least 8 characters.");
        } else {
            password.setCustomValidity("");
        }
    });
}
