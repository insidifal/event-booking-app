import { showAlert, showMessage, showBox, hideBox, closeBtn, getLocations } from './utils.js';
import { usertoken } from './login.js';
import { account } from './account.js';

const emptyUser = {
    "user_id": "",
    "username": "",
    "firstname": "",
    "lastname": "",
    "password": "",
    "location_id": ""
};

export let user = emptyUser;
let newPassword = "";
let newLocation = "";

export const loginEvent = new CustomEvent("loggedIn", {
    detail: user,
    bubbles: true,
    cancelable: true
});

export const logoutEvent = new CustomEvent("loggedOut", {
    detail: emptyUser,
    bubbles: true,
    cancelable: true
});

document.addEventListener('loggedOut', () => {
    user = emptyUser;
    hideBox(profileBtn());
    hideBox(profileBox());
});

export const getUser = async () => {
    if (usertoken === null) return null;
    try {
        const response = await fetch("/user/me", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${usertoken}`
            }
        });
        if (!response.ok) {
            if (response.status === 401) showAlert("Invalid credentials");
            if (response.status === 404) showAlert("Username does not exist");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            user = await response.json();
        }
    } catch (error) {
        showAlert(error);
    }
}

export const updateUser = async () => {
    if (usertoken === null) return null;
    try {
        const response = await fetch("/user", {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${usertoken}`
            },
            body: JSON.stringify({
                'user_id': user['user_id'],
                'username': user['username'],
                'firstname': user['firstname'],
                'lastname': user['lastname'],
                'password': user['password'],
                'location_id': user['location_id']
            })
        });
        if (!response.ok) {
            if (response.status === 401) showAlert("Unauthorized");
            if (response.status === 404) showAlert("User does not exist");
            if (response.status === 422) showAlert("Could not validate input");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            user = await response.json();
            showMessage("Updated");
        }
    } catch (error) {
        showAlert(error);
    }
}

export const profileBtn = () => {
    const div = document.createElement('div');
    div.textContent = user["firstname"];
    div.id = 'profile-button';
    div.classList.add('button');
    div.addEventListener('click', async () => {
        showBox(await profileBox());
    });
    return div;
}

export const profileBox = async () => {
    const div = document.createElement('div');
    div.innerHTML = `
        <h3>${user["firstname"]} ${user["lastname"]}</h3>
    `;

    const username = document.createElement('div');
    username.innerHTML = `
        <label for="profile-username">Username:</label>
        <span id="profile-username">${user["username"]}</span>
    `
    div.append(username);

    let accS = account["account_id"] === "" ? "Inactive" : "Active";
    const accountStatus = document.createElement('div');
    accountStatus.innerHTML = `
        <label for="account-status">Account:</label>
        <span id="account-status">${accS}</span>
    `
    div.append(accountStatus);

    const password = document.createElement('input');
    password.id = "new-password";
    password.type = "password";
    password.placeholder = "Change password";
    password.addEventListener('change', () => {
        newPassword = password.value;
        document.getElementById('confirm-profile')
            .style.visibility = 'visible';
    });
    div.append(password);

    div.append(await dropDownLocation());
    div.append(confirmBtn());
    div.prepend(closeBtn(async () => {
        hideBox(await profileBox());
        newPassword = "";
        newLocation = "";
    }));
    div.id = 'profile-box';
    div.classList.add('input-box');
    return div;
}

const dropDownLocation = async () => {
    const div = document.createElement('div');
    div.id = 'city-dropdown';
    div.classList.add('dropdownlist');

    const label = document.createElement('label');
    label.textContent = "Location";
    label.setAttribute("for", "cities");
    div.append(label);

    const select = document.createElement('select');
    select.id = "cities";
    select.name = "cities";

    const defaultOpt = document.createElement('option');
    if (user["location_id"] === null) {
        defaultOpt.value = "";
        defaultOpt.textContent = "City";
        defaultOpt.selected = true;
        defaultOpt.disabled = true;
        defaultOpt.hidden = true;
        select.append(defaultOpt);
    }

    const list = await getLocations();

    for (let city of list) {
        try {
            const opt = document.createElement('option');
            opt.value = city["location_id"];
            opt.textContent = city["city"];
            if (user["location_id"] === city["location_id"]) {
                opt.selected = true;
            }
            select.append(opt);
        } catch (error) {
            console.log(error);
            const msg = document.createElement('p');
            msg.textContent = "Something went wrong";
            div.append(msg);
        }
    }

    select.addEventListener('change', () => {
        newLocation = select.value;
        document.getElementById('confirm-profile')
            .style.visibility = 'visible';
    });

    div.append(select);
    return div;
}

const confirmBtn = () => {
    const div = document.createElement('div');
    div.textContent = 'CONFIRM';
    div.id = 'confirm-profile';
    div.classList.add('button');
    div.classList.add('submit-button');
    div.addEventListener('click', async () => {
        if (newPassword !== "") user["password"] = newPassword;
        if (newLocation !== "") user["location_id"] = newLocation;
        await updateUser();
        newPassword = "";
        newLocation = "";
        hideBox(await profileBox());
    });
    div.style.visibility = 'hidden';
    return div;
}

