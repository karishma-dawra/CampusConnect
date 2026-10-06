const email = document.getElementById("email");

email.addEventListener("invalid", function () {
    if (email.validity.valueMissing) {
        email.setCustomValidity("Please enter your offical email.");
    } 
    else if (email.validity.typeMismatch || email.validity.patternMismatch) {
        email.setCustomValidity(
            "Please enter a valid offical email like name1234.branch@chitkara.edu.in"
        );
    }
});

// _______________________________________________________________________


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
const confirmpassword = document.getElementById("confirmpassword");

password.addEventListener("input", function () {
    if (password.value.length < 8) {
        password.setCustomValidity("Password must contain at least 8 characters.");
    } else {
        password.setCustomValidity("");
    }

    checkPasswordMatch();
});

confirmpassword.addEventListener("input", checkPasswordMatch);

function checkPasswordMatch() {
    if (confirmpassword.value !== password.value) {
        confirmpassword.setCustomValidity("Passwords do not match.");
    } else {
        confirmpassword.setCustomValidity("");
    }
}
