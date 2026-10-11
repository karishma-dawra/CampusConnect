// const form = document.querySelector("form");

// form.addEventListener("submit", async function (event) {
//     event.preventDefault();

//     const inputs = form.querySelectorAll("input");
//     const name = inputs[0].value.trim();
//     const email = inputs[1].value.trim();
//     const password = inputs[2].value;
//     const confirmPassword = inputs[3].value;

//     if (password !== confirmPassword) {
//         alert("Passwords do not match");
//         return;
//     }

//     try {
//         const response = await fetch("http://127.0.0.1:8000/register", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({
//                 name: name,
//                 email: email,
//                 password: password
//             })
//         });

//         const data = await response.json();

//        if (response.ok) {
//     alert(data.message);
//     window.location.assign("./login.html");
// } else {
//     alert(data.detail || data.message || "Registration failed");
// }
//             // alert(data.detail || data.message || "Registration failed");
//         // }
//     } catch (error) {
//         alert("Could not connect to the backend. Make sure it is running.");
//         console.error(error);
//     }
// });


const form = document.querySelector("form");
const emailInput = document.getElementById("email");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    // Trigger the browser's built-in validation popup
    if (!form.reportValidity()) {
        return;
    }

    const inputs = form.querySelectorAll("input");
    const name = inputs[0].value.trim();
    const email = emailInput.value.trim();
    const password = inputs[2].value;
    const confirmPassword = inputs[3].value;



    emailInput.setCustomValidity("");

    if (password !== confirmPassword) {
        alert("Passwords do not match");
        return;
    }

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/register",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            window.location.assign("./login.html");
        } else {
            alert(
                data.detail ||
                data.message ||
                "Registration failed"
            );
        }

    } catch (error) {
        alert(
            "Could not connect to the backend. Make sure it is running."
        );
        console.error(error);
    }
});

// Clear the custom error when the user edits the email
emailInput.addEventListener("input", function () {
    emailInput.setCustomValidity("");
});
