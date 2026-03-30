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
    try {
        text.textContent = message;
        showBox('messages');
    } catch (error) {
        console.log(error);
    }
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



