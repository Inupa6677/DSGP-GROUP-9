const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const sign_in_btn2 = document.querySelector("#sign-in-btn2");
const sign_up_btn2 = document.querySelector("#sign-up-btn2");

sign_up_btn.addEventListener("click",() => {
    container.classList.add("sign-up-mode");
});
sign_in_btn.addEventListener("click",() => {
    container.classList.remove("sign-up-mode");
});
sign_up_btn2.addEventListener("click",() => {
    container.classList.add("sign-up-mode2");
});
sign_in_btn2.addEventListener("click",() => {
    container.classList.remove("sign-up-mode2");
});

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username');
    const password = document.getElementById('password');

    // Check if username is empty
    if (username.value.trim() === '') {
        username.classList.add('error');
    } else {
        username.classList.remove('error');
    }

    // Check if password is empty
    if (password.value.trim() === '') {
        password.classList.add('error');
    } else {
        password.classList.remove('error');
    }

    // If both fields are filled, you can proceed with form submission
    if (username.value.trim() !== '' && password.value.trim() !== '') {
        // Here, you can perform any additional login logic, AJAX requests, etc.
        console.log('Username:', username.value);
        console.log('Password:', password.value);
        // For now, I'm just alerting a message
        alert('Login successful!');
    }
});

document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const newPassword = document.getElementById('new-password');
    const confirmPassword = document.getElementById('confirm-password');

    // Check if any field is empty
    if (username.value.trim() === '' || email.value.trim() === '' || newPassword.value.trim() === '' || confirmPassword.value.trim() === '') {
        alert('All fields are required.');
        return;
    }

    // Check if passwords match
    if (newPassword.value !== confirmPassword.value) {
        alert('Passwords do not match.');
        return;
    }

    // If all checks pass, you can proceed with form submission
    console.log('Username:', username.value);
    console.log('Email:', email.value);
    console.log('Password:', newPassword.value);
    // For now, I'm just alerting a message
    alert('Sign up successful!');

});





