document.addEventListener("DOMContentLoaded", function() {
    const sign_in_btn = document.querySelector("#sign-in-btn");
    const sign_up_btn = document.querySelector("#sign-up-btn");
    const container = document.querySelector(".container");
    const sign_in_btn2 = document.querySelector("#sign-in-btn2");
    const sign_up_btn2 = document.querySelector("#sign-up-btn2");

    sign_up_btn.addEventListener("click", () => {
        container.classList.add("sign-up-mode");
    });
    sign_in_btn.addEventListener("click", () => {
        container.classList.remove("sign-up-mode");
    });
    sign_up_btn2.addEventListener("click", () => {
        container.classList.add("sign-up-mode2");
    });
    sign_in_btn2.addEventListener("click", () => {
        container.classList.remove("sign-up-mode2");
    });

    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username');
        const password = document.getElementById('password');

        // Check if username is empty
        if (username.value.trim() === '') {
            alert('Username is required.');
            return;
        }

        // Check if password is empty
        if (password.value.trim() === '') {
            alert('Password is required.');
            return;
        }

        // If all checks pass, display success message
        alert('Login successful!');
        // Additional login logic can be placed here
    });

    document.getElementById('signup-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username');
        const email = document.getElementById('email');
        const newPassword = document.getElementById('new-password');
        const confirmPassword = document.getElementById('confirm-password');

        // Check if username is empty
        if (username.value.trim() === '') {
            alert('Username is required.');
            return;
        }

        // Check if email is empty
        if (email.value.trim() === '') {
            alert('Email is required.');
            return;
        }

        // Check if the entered value is in a valid email format using a regular expression
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email.value.trim())) {
            alert('Please enter a valid email address.');
            return;
        }

        // Check if new password is empty
        if (newPassword.value.trim() === '') {
            alert('New password is required.');
            return;
        }

        // Check if confirm password is empty
        if (confirmPassword.value.trim() === '') {
            alert('Confirm password is required.');
            return;
        }

        // Check if passwords match
        if (newPassword.value !== confirmPassword.value) {
            alert('Passwords do not match.');
            return;
        }

        // If all checks pass, display success message
        alert('Signup successful!');
        // Additional signup logic can be placed here
    });
});
