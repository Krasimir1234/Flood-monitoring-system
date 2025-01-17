document.addEventListener("DOMContentLoaded", () => {
    const signupForm = document.getElementById("signupForm");

    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const realName = document.getElementById("realName").value;
        const lastName = document.getElementById("lastName").value;
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const userData = { realName, lastName, username, email, password };

        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailPattern.test(email)) {
            showSystemMessage("Invalid email format. Please enter a valid email.", false);
            return;
        }

        try {
            const response = await fetch("/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(userData),
            });

            const result = await response.json();

            if (response.ok) {
                showSystemMessage(result.message || "Signup successful! You can now log in.", true);
                signupForm.reset();
            } else {
                showSystemMessage(result.message || "Signup failed. Please try again.", false);
            }
        } catch (error) {
            console.error("Error during signup:", error);
            showSystemMessage("An unexpected error occurred. Please try again later.", false);
        }
    });

    function showSystemMessage(message, isSuccess) {
        let messageElement = document.getElementById("system-message");

        if (!messageElement) {
            messageElement = document.createElement("div");
            messageElement.id = "system-message";
            signupForm.parentNode.insertBefore(messageElement, signupForm);
        }

        messageElement.innerText = message;
        messageElement.className = isSuccess ? "system-message success" : "system-message error";

        setTimeout(() => {
            messageElement.innerText = "";
            messageElement.className = "";
        }, 3000);
    }
});
