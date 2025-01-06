document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");


    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const emailOrUsername = document.getElementById("emailOrUsername").value;
        const password = document.getElementById("password").value;

        const loginData = { emailOrUsername, password };

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(loginData),
            });

            const result = await response.json();

            if (response.ok) {
                const messageElement = document.createElement("p");
                messageElement.innerText = result.message || "Login successful!";
                document.body.appendChild(messageElement);

                window.location.href = result.redirect;
            } else {
                const errorElement = document.createElement("p");
                errorElement.innerText = result.message || "Invalid username/email or password.";
                document.body.appendChild(errorElement);
            }
        } catch (error) {
            console.error("Error during login:", error);
            const errorElement = document.createElement("p");
            errorElement.innerText = "An unexpected error occurred. Please try again later.";
            document.body.appendChild(errorElement);
        }
    });


    const signupLink = document.getElementById("signupLink");
    signupLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.location.href = "/";
    });
});
