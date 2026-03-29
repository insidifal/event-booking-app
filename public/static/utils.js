export const messageBox = () => {
    const div = document.createElement('div');
    const text = document.createElement('span');
    text.id = 'message-text';
    div.prepend(closeBtn(() => hideBox('messages')));
    div.append(text);
    div.id = 'messages';
    div.style.visibility = 'hidden';
    return div;
}

export const showMessage = (message) => {
    const text = document.getElementById('message-text');
    text.textContent = message;
    showBox('messages');
}

export const showBox = (boxId) => {
    const box = document.getElementById(boxId);
    if (box.style.visibility === 'hidden')
        box.style.visibility = 'visible';
}

export const hideBox = (boxId) => {
    const box = document.getElementById(boxId);
    if (box.style.visibility === 'visible')
        box.style.visibility = 'hidden';
}

export const closeBtn = (action) => {
    const div = document.createElement('div');
    div.textContent = 'x';
    div.id = 'close-button';
    div.classList.add('button');
    div.addEventListener('click', () => {
        action();
    });
    return div;
}

