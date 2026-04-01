const main = document.getElementById('main');

export const showMessage = (message) => {
    const div = document.createElement('div');
    div.id = 'message-box';
    const text = document.createElement('span');
    text.id = 'message-text';
    text.textContent = message;
    div.append(text);
    div.prepend(closeBtn(() => hideBox(div)));
    showBox(div);
}

export const showAlert = (message) => {
    const div = document.createElement('div');
    div.id = 'alert-box';
    const text = document.createElement('span');
    text.id = 'alert-text';
    text.textContent = message;
    div.append(text);
    div.prepend(closeBtn(() => hideBox(div)));
    showBox(div);
}

export const areYouSure = async (warning, yesAction) => {
    const div = document.createElement('div');
    div.id = 'warning-box';

    const text = document.createElement('h2');
    text.id = 'warning-text';
    text.textContent = warning;
    div.append(text);

    const buttons = document.createElement('div');
    buttons.id = 'warning-buttons';
    const yes = document.createElement('button');
    yes.textContent = "YES";
    yes.classList.add('button');
    yes.classList.add('delete-button');
    yes.addEventListener('click', async () => {
        await yesAction();
        hideBox(div);
    });
    buttons.append(yes);

    const no = document.createElement('button');
    no.textContent = "NO";
    no.addEventListener('click', () => hideBox(div));
    no.classList.add('button');
    no.classList.add('delete-button');
    buttons.append(no);

    div.append(buttons);
    div.prepend(closeBtn(() => hideBox(div)));
    showBox(div);
}

export const showBox = (box) => {
    const exists = document.getElementById(box.id);
    if (exists === null) {
        main.append(box);
    } else {
        exists.remove();
        main.append(box);
    }
}

export const hideBox = (box) => {
    const exists = document.getElementById(box.id);
    if (exists !== null) {
        exists.remove();
    }
}

export const closeBtn = (action) => {
    const div = document.createElement('div');
    div.textContent = '⮌';
    div.id = 'close-button';
    div.classList.add('button');
    div.addEventListener('click', () => {
        action();
    });
    return div;
}

export const deleteBtn = (label, yes) => {
    const div = document.createElement('div');
    div.textContent = label;
    div.classList.add('button');
    div.classList.add('delete-button');
    div.addEventListener('click', async () => {
        await areYouSure("This cannot be undone", yes);
    });
    return div;
}

export const getLocations = async () => {
    try {
        const response = await fetch("/location", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            if (response.status === 422) showMessage("Bad query");
        } else {
            return await response.json();
        }
    } catch (error) {
        showMessage(error);
    }
}

export const getLocation = async (location_id) => {
    try {
        const response = await fetch(`/location/${location_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            if (response.status === 400) showMessage("Bad input");
            if (response.status === 404) showMessage("Location not found");
        } else {
            return await response.json();
        }
    } catch (error) {
        showMessage(error);
    }
}



