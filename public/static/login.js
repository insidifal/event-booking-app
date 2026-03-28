let usertoken = null;

const messageBox = () => {
    const div = document.createElement('div');
    const text = document.createElement('span');
    text.id = 'message-text';
    div.prepend(closeBtn(() => hideBox('messages')));
    div.append(text);
    div.id = 'messages';
    div.style.visibility = 'hidden';
    return div;
}

const showMessage = (message) => {
    const text = document.getElementById('message-text');
    text.textContent = message;
    showBox('messages');
}

const authenticate = async (username, password) => {
    const response = await fetch("/auth/login", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'username': username, 'password': password })
    });
    if (!response.ok) {
        showMessage(response.status);
    } else {
        payload = await response.json();
        usertoken = payload["X-Token"];
    }
}

const login = async () => {
    const div = document.createElement('div');
    div.textContent = 'LOGIN';
    div.id = 'login-submit';
    div.classList.add('button');
    div.addEventListener('click', async () => {
        const username = document.getElementById('username-input').value;
        const password = document.getElementById('password-input').value;
        await authenticate(username, password);
        if (usertoken !== null) hideBox('login-box');
    });
    return div;
}

const loginBox = async () => {
    const div = document.createElement('div');
    div.innerHTML = `
        <input id="username-input" type="text" placeholder="Username">
        <input id="password-input" type="password" placeholder="Password">
    `;
    div.prepend(closeBtn(() => hideBox('login-box')));
    div.append(await login());
    div.id = 'login-box';
    div.style.visibility = 'hidden';
    return div;
}

const showBox = (boxId) => {
    const box = document.getElementById(boxId);
    if (box.style.visibility === 'hidden')
        box.style.visibility = 'visible';
}

const hideBox = (boxId) => {
    const box = document.getElementById(boxId);
    if (box.style.visibility === 'visible')
        box.style.visibility = 'hidden';
}

const loginBtn = () => {
    const div = document.createElement('div');
    div.textContent = 'LOGIN';
    div.id = 'login-button';
    div.classList.add('button');
    div.addEventListener('click', () => {
        showBox('login-box');
    });
    return div;
}

const closeBtn = (action) => {
    const div = document.createElement('div');
    div.textContent = 'x';
    div.id = 'close-button';
    div.classList.add('button');
    div.addEventListener('click', () => {
        action();
    });
    return div;
}

