import { showAlert, showMessage, showBox, hideBox, closeBtn } from './utils.js';
import { getUser, loginEvent, logoutEvent } from './profile.js';

export let usertoken = null;

document.addEventListener('loggedIn', async () => {
    hideBox(registerBtn());
    hideBox(registerBox());
    hideBox(loginBox());
    document.getElementById('login-button').textContent = 'LOGOUT';
});

const authenticate = async (username, password) => {
    try {
        const response = await fetch("/auth/login", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'username': username, 'password': password })
        });
        if (!response.ok) {
            if (response.status === 401) showAlert("Invalid credentials");
            if (response.status === 404) showAlert("Username does not exist");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            const payload = await response.json();
            usertoken = payload["X-Token"];
            showMessage(`Logged in as ${username}`);
        }
    } catch(error) {
        showAlert(error);
    }
}

const addUser = async (firstname, lastname, username, password) => {
    try {
        const response = await fetch("/user", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'firstname': firstname,
                'lastname': lastname,
                'username': username,
                'password': password
            })
        });
        if (!response.ok) {
            if (response.status === 409) showAlert("Username already exists");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            const newuser = await response.json();
            showMessage("New user created");
            return newuser;
        }
    } catch (error) {
        showAlert(error);
    }
}

const login = () => {
    const div = document.createElement('div');
    div.textContent = 'LOGIN';
    div.id = 'login-submit';
    div.classList.add('button');
    div.classList.add('submit-button');
    div.addEventListener('click', async () => {
        const username = document.getElementById('username-input').value;
        const password = document.getElementById('password-input').value;
        if (username !== "" && password !== "") {
            await authenticate(username, password);
        }
        if (usertoken !== null) {
            await getUser(); // profile.js
            hideBox(loginBox());
            document.dispatchEvent(loginEvent);
        }
    });
    return div;
}

export const loginBox = () => {
    const div = document.createElement('div');

    const username = document.createElement('input');
    username.id = "username-input";
    username.type = "text";
    username.placeholder = "Username";

    const password = document.createElement('input');
    password.id = "password-input";
    password.type = "password";
    password.placeholder = "Password";

    password.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            document.getElementById('login-submit').click();
        }
    });

    div.prepend(closeBtn(() => hideBox(loginBox())));
    div.append(username);
    div.append(password);
    div.append(login());
    div.id = 'login-box';
    div.classList.add('input-box');

    return div;
}

export const loginBtn = () => {
    const div = document.createElement('div');
    div.textContent = 'LOGIN';
    div.id = 'login-button';
    div.classList.add('button');
    div.addEventListener('click', () => {
        if (usertoken === null) { // not logged in
            showBox(loginBox());
        } else {
            usertoken = null; // logout
            showMessage("Logged out");
            document.dispatchEvent(logoutEvent);
            div.textContent = 'LOGIN';
        }
    });
    return div;
}

const register = () => {
    const div = document.createElement('div');
    div.textContent = 'REGISTER';
    div.id = 'register-submit';
    div.classList.add('button');
    div.classList.add('submit-button');
    div.addEventListener('click', async () => {
        const firstname = document.getElementById('register-firstname').value;
        const lastname = document.getElementById('register-lastname').value;
        const username = document.getElementById('register-username').value;
        const password = document.getElementById('register-password').value;
        if (firstname !== "" && lastname !== "" && username !== "" && password !== "") {
            const newuser = await addUser(firstname, lastname, username, password);
            if (newuser) await authenticate(username, password); // gets a JWT for the user
        }
        if (usertoken !== null) {
            await getUser(); // profile.js - triggers login
            hideBox(registerBox());
            document.dispatchEvent(loginEvent);
        }
    });
    return div;
}

export const registerBox = () => {
    const div = document.createElement('div');
    div.innerHTML = `
        <input id="register-firstname" type="text" placeholder="First name">
        <input id="register-lastname" type="text" placeholder="Last name">
        <input id="register-username" type="text" placeholder="Username">
        <input id="register-password" type="password" placeholder="Password">
    `;
    div.prepend(closeBtn(() => hideBox(registerBox())));
    div.append(register());
    div.id = 'register-box';
    div.classList.add('input-box');
    return div;
}

export const registerBtn = () => {
    const div = document.createElement('div');
    div.textContent = 'REGISTER';
    div.id = 'register-button';
    div.classList.add('button');
    div.addEventListener('click', () => {
        showBox(registerBox());
    });
    return div;
}

