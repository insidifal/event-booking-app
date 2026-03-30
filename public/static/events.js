import { showMessage, getLocation } from './utils.js';

const fragment = document.createDocumentFragment();

const getEvents = async () => {
    try {
        const response = await fetch("/event", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            if (response.status === 400) showMessage("Invalid search");
            if (response.status === 500) showMessage("Something went wrong");
        } else {
            return await response.json();
        }
    } catch (error) {
        showMessage(error);
    }
}

const eventCard = async (event) => {
    const div = document.createElement('div');
    div.classList.add('event-card');

    try {
        const name = document.createElement('h2');
        name.textContent = event["name"];
        div.append(name);

        const location = document.createElement('h3');
        const l = await getLocation(event["location_id"]);
        const country = l["country"];
        const city = l["city"];
        location.textContent = `${city}, ${country}`;
        div.append(location);

        const date = document.createElement('h3');
        const d = new Date(event["start"]);
        date.textContent = d.toDateString();
        div.append(date);

        const time = document.createElement('p');
        const t = new Date(event["start"]);
        const hours = String(t.getHours()).padStart(2, '0');
        const minutes = String(t.getMinutes()).padStart(2, '0');
        time.textContent = `${hours}:${minutes}`;
        div.append(time);

        const remaining = document.createElement('p');
        const value = event["capacity"] - event["booked"];
        remaining.textContent = `${value} seats remaining`;
        div.append(remaining);

        const price = document.createElement('p');
        price.textContent = `${event["currency"]} ${event["price"]}`;
        div.append(price);
    } catch (error) {
        console.log(error);
        const msg = document.createElement('p');
        msg.textContent = "Something went wrong";
        div.append(msg);
    }

    fragment.appendChild(div);
}

export const displayEvents = async () => {
    const div = document.createElement('div');
    div.id = 'events-display';
    try {
        const events = await getEvents();
        for (let event of events) {
            await eventCard(event);
        }
        div.appendChild(fragment);
    } catch (error) {
        showMessage(error);
    }
    return div;
}


