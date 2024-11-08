document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", (e) => {
        e.preventDefault(); 

        const emailOrUsername = document.getElementById("emailOrUsername").value;
        const password = document.getElementById("password").value;

       
        const loginData = { emailOrUsername, password };

      

        console.log("Login data:", loginData);

        if (emailOrUsername && password) {
            alert("Login successful!");
            loginForm.reset(); 
        } else {
            alert("Please enter both a username/email and password.");
        }
    });
});
