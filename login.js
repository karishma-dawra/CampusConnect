const form = document.getElementById("loginForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
        alert("Please enter your email and password.");
        return;
    }

    try {
        const response = await 
            // fetch("http://127.0.0.1:8000/login", 
            fetch("https://campusconnect-backend-msmw.onrender.com/login",
            {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Invalid email or password.");
            return;
        }

        alert("Welcome, " + data.name + "!");

        // Save the logged-in user's details for the next page
        sessionStorage.setItem("user_id", data.user_id);
        sessionStorage.setItem("user_name", data.name);
        sessionStorage.setItem("user_email", data.email);

        // Change this if your destination page has another name
        window.location.href = "./dashboard.html";

    } catch (error) {
        console.error("Login error:", error);
        alert("Cannot connect to the server. Make sure FastAPI is running.");
    }
});
