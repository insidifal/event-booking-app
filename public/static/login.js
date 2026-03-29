import { showMessage, showBox, hideBox, closeBtn } from './utils.js';
import { getUser, logoutEvent } from './profile.js';

export let usertoken = null;

const authenticate = async (username, password) => {
    const response = await fetch("/auth/login", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'username': username, 'password': password })
    });
    if (!response.ok) {
        if (response.status === 401) showMessage("Invalid credentials");
        if (response.status === 404) showMessage("Username does not exist");
    } else {
        const payload = await response.json();
        usertoken = payload["X-Token"];
    }
}

const addUser = async (firstname, lastname, username, password) => {
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
        if (response.status === 409) showMessage("Username already exists");
        if (response.status === 500) showMessage("Something went wrong");
    } else {
        const newuser = await response.json();
        return newuser;
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
            hideBox('login-box');
            document.getElementById('login-button').textContent = 'LOGOUT';
        }
    });
    return div;
}

export const loginBox = () => {
    const div = document.createElement('div');
    div.innerHTML = `
        <input id="username-input" type="text" placeholder="Username">
        <input id="password-input" type="password" placeholder="Password">
    `;
    div.prepend(closeBtn(() => hideBox('login-box')));
    div.append(login());
    div.id = 'login-box';
    div.classList.add('input-box');
    div.style.visibility = 'hidden';
    return div;
}

export const loginBtn = () => {
    const div = document.createElement('div');
    div.textContent = 'LOGIN';
    div.id = 'login-button';
    div.classList.add('button');
    div.addEventListener('click', () => {
        if (usertoken === null) {
            showBox('login-box');
        } else {
            usertoken = null; // logout
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
            hideBox('register-box');
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
    div.prepend(closeBtn(() => hideBox('register-box')));
    div.append(register());
    div.id = 'register-box';
    div.classList.add('input-box');
    div.style.visibility = 'hidden';
    return div;
}

export const registerBtn = () => {
    const div = document.createElement('div');
    div.textContent = 'REGISTER';
    div.id = 'register-button';
    div.classList.add('button');
    div.addEventListener('click', () => {
        showBox('register-box');
    });
    return div;
}

