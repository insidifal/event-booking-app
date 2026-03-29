import { showMessage, showBox, hideBox, closeBtn } from './utils.js';
import { usertoken } from './login.js';

const emptyUser = {
    "user_id": "",
    "username": "",
    "firstname": "",
    "lastname": ""
};

let user = emptyUser;

const loginEvent = new CustomEvent("loggedIn", {
    detail: user,
    bubbles: true,
    cancelable: true
});

export const logoutEvent = new CustomEvent("loggedOut", {
    detail: emptyUser,
    bubbles: true,
    cancelable: true
});


export const getUser = async () => {
    if (usertoken === null) return null;
    const response = await fetch("/user/me", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${usertoken}`
        }
    });
    if (!response.ok) {
        if (response.status === 401) showMessage("Invalid credentials");
        if (response.status === 404) showMessage("Username does not exist");
        if (response.status === 500) showMessage("Something went wrong");
    } else {
        user = await response.json();
        document.dispatchEvent(loginEvent);
    }
}

export const profileBtn = () => {
    const div = document.createElement('div');
    div.textContent = user["firstname"];
    div.id = 'profile-button';
    div.classList.add('button');
    return div;
}

