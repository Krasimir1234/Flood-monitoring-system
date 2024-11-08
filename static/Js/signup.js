document.addEventListener("DOMContentLoaded", () => {
    const signupForm = document.getElementById("signupForm");

    signupForm.addEventListener("submit", (e) => {
        e.preventDefault(); 

        const realName = document.getElementById("realName").value;
        const lastName = document.getElementById("lastName").value;
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        
        const userData = { realName, lastName, username, email, password };

        console.log("Signup Data:", userData); 

        alert("Signup successful! You can now log in.");
        signupForm.reset(); 
    });
});
