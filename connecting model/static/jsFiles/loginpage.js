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

    document.getElementById('signup-form').addEventListener('submit', async function(event) {
        event.preventDefault();
        const username = document.getElementById('user_name').value;
        const email = document.getElementById('email').value;
        const newPassword = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

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

        // Check if username or email already exists
        const userExists = await checkUserExists(username, email);
        if (userExists) {
            alert('Username or email already exists.');
            return;
        }

        // Save user information if username and email are unique
        saveMessages(username, email, newPassword, confirmPassword);

        // Display success message and redirect after 2 seconds
        alert('Signup successful!');
        setTimeout(() => {
            window.location.href = '/login_page';
        }, 2000);
    });

    document.getElementById('loginForm').addEventListener('submit', async function(event) {
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

        const isValidUser = await checkUserCredentials(username, password);
        if (isValidUser) {
            alert('Login successful!');
            window.location.href = '/home_page';
        } else {
            alert('Invalid username or password. Please try again.');
        }
    });
});

// Function to check if username or email already exists
const checkUserExists = async (username, email) => {
    const snapshot = await firebase.database().ref('users').once('value');
    const users = snapshot.val();
    if (users) {
        // Check if username or email exists in the database
        const existingUser = Object.values(users).find(user => user.userName === username || user.email === email);
        return existingUser ? true : false;
    }
    return false;
};

// Check if user credentials are valid
const checkUserCredentials = async (username, password) => {
    const snapshot = await firebase.database().ref('users').once('value');
    const users = snapshot.val();
    console.log("Retrieved users:", users); // Debugging line
    if (users) {
        // Check for matching username and password
        const user = Object.values(users).find(user => user.userName === username && user.password === password);
        console.log("Found user:", user); // Debugging line
        return user ? true : false;
    }
    return false;
};

const saveMessages = (username, email, password, confirmPassword) => {
    var newhForm = hForm.child(username);

    newhForm.set({
        email: email,
        userName: username,
        password: password,
        confirmPassword: confirmPassword
    });
};
