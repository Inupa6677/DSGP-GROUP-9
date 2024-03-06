// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCFW3syoPBgLC4goFsMOmuib08MLa8Cw68",
  authDomain: "accitracker-f6711.firebaseapp.com",
  databaseURL: "https://accitracker-f6711-default-rtdb.firebaseio.com",
  projectId: "accitracker-f6711",
  storageBucket: "accitracker-f6711.appspot.com",
  messagingSenderId: "282142705468",
  appId: "1:282142705468:web:3a79557c0f1ed58b584039",
  measurementId: "G-9J9B72P17N"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const database = firebase.database();
alert(database)

var hForm = firebase.database().ref('users');


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
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Check if username is empty
        if (username.trim() === '') {
            alert('Username is required.');
            return;
        }

        // Check if password is empty
        if (password.trim() === '') {
            alert('Password is required.');
            return;
        }

        // If all checks pass, display success message
        alert('Login successful!');
        // Additional login logic can be placed here
    });

    document.getElementById('signup-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('user_name').value; // Get the value of the username input
        const email = document.getElementById('email').value; // Get the value of the email input
        const newPassword = document.getElementById('new-password').value; // Get the value of the new password input
        const confirmPassword = document.getElementById('confirm-password').value; // Get the value of the confirm password input

        // Check if username is empty
        if (username.trim() === '') {
            alert('Username is required.');
            return;
        }

        // Check if email is empty
        if (email.trim() === '') {
            alert('Email is required.');
            return;
        }

        // Check if the entered value is in a valid email format using a regular expression
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            alert('Please enter a valid email address.');
            return;
        }

        // Check if new password is empty
        if (newPassword.trim() === '') {
            alert('New password is required.');
            return;
        }

        // Check if confirm password is empty
        if (confirmPassword.trim() === '') {
            alert('Confirm password is required.');
            return;
        }

        // Check if passwords match
        if (newPassword !== confirmPassword) {
            alert('Passwords do not match.');
            return;
        }
        saveMessages(username, email, password, confirmPassword);
        // If all checks pass, display success message
        alert('Signup successful!');
        setTimeout(() => {
  window.location.href = '/login_page';
    }, 2000);
        // Additional signup logic can be placed here
    });
});


const saveMessages = (username, email, password, confirmPassword) => {
  var newhForm = hForm.child(username);

  newhForm.set({
    email: email,
    userName: username,
    password: password,
    confirmPassword: confirmPassword
  });
};



