const main = document.getElementById('main');

export const messageBox = (message) => {
    const div = document.createElement('div');
    const text = document.createElement('span');
    text.id = 'message-text';
    text.textContent = message;
    div.prepend(closeBtn(() => hideBox(messageBox())));
    div.append(text);
    div.id = 'message-box';
    return div;
}

export const showMessage = (message) => {
    try {
        showBox(messageBox(message));
    } catch (error) {
        console.log(error);
    }
}

export const showBox = (box) => {
    const exists = document.getElementById(box.id);
    if (exists === null) {
        main.append(box);
    } else {
        exists.remove();
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
    div.textContent = 'x';
    div.id = 'close-button';
    div.classList.add('button');
    div.addEventListener('click', () => {
        action();
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



