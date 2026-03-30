import { showMessage, showBox, hideBox, closeBtn, getLocations } from './utils.js';
import { usertoken } from './login.js';

const emptyUser = {
    "user_id": "",
    "username": "",
    "firstname": "",
    "lastname": "",
    "password": "",
    "location_id": ""
};

let user = emptyUser;

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
    document.getElementById('profile-button').remove();
    document.getElementById('profile-box').remove();
});

document.addEventListener('loggedIn', async () => {
    document.getElementById('register-button').remove();
    document.getElementById('login-button').textContent = 'LOGOUT';
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
            if (response.status === 401) showMessage("Invalid credentials");
            if (response.status === 404) showMessage("Username does not exist");
            if (response.status === 500) showMessage("Something went wrong");
        } else {
            user = await response.json();
        }
    } catch (error) {
        showMessage(error);
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
            if (response.status === 401) showMessage("Unauthorized");
            if (response.status === 404) showMessage("User does not exist");
            if (response.status === 422) showMessage("Could not validate input");
            if (response.status === 500) showMessage("Something went wrong");
        } else {
            user = await response.json();
        }
    } catch (error) {
        showMessage(error);
    }
}

export const profileBtn = () => {
    const div = document.createElement('div');
    div.textContent = user["firstname"];
    div.id = 'profile-button';
    div.classList.add('button');
    div.addEventListener('click', () => {
        showBox('profile-box');
    });
    return div;
}

export const profileBox = async () => {
    const div = document.createElement('div');
    div.innerHTML = `
        <h3>${user["firstname"]} ${user["lastname"]}</h3>
        <h3>Username: ${user["username"]}</h3>
    `;

    const password = document.createElement('input');
    password.id = "new-password";
    password.type = "password";
    password.placeholder = "Change password";
    password.addEventListener('change', () => {
        user["password"] = password.value;
        document.getElementById('confirm-button')
            .style.visibility = 'visible';
    });


    div.append(password);
    div.append(await dropDownLocation());
    div.append(confirmBtn());
    div.prepend(closeBtn(() => {
        hideBox('profile-box');
        document.getElementById('confirm-button')
            .style.visibility = 'hidden';
    }));
    div.id = 'profile-box';
    div.classList.add('input-box');
    div.style.visibility = 'hidden';
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
        user["location_id"] = select.value;
        document.getElementById('confirm-button')
            .style.visibility = 'visible';
    });

    div.append(select);
    return div;
}

const confirmBtn = () => {
    const div = document.createElement('div');
    div.textContent = 'CONFIRM';
    div.id = 'confirm-button';
    div.classList.add('button');
    div.classList.add('submit-button');
    div.addEventListener('click', async () => {
        await updateUser();
    });
    div.style.visibility = 'hidden';
    return div;
}

