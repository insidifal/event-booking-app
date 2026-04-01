import { showBox, showAlert, showMessage, closeBtn, getLocation } from './utils.js';
import { usertoken, loginBox } from './login.js';
import { account, activateBox } from './account.js';
import { user } from './profile.js';

const fragment = document.createDocumentFragment();
const main = document.getElementById('main');

export const postBooking = async (event, seats, total_price) => {
    if (usertoken === null) return null;
    try {
        const response = await fetch("/booking", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${usertoken}`
            },
            body: JSON.stringify({
                'user_id': user['user_id'],
                'event_id': event["event_id"],
                'seats': seats,
                'total_price': total_price,
                'currency': event["currency"]
            })
        });
        if (!response.ok) {
            if (response.status === 401) showAlert("Unauthorized");
            if (response.status === 409) showAlert("Booking exists");
            if (response.status === 422) showAlert("Validation error");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            const booking = await response.json();
            showMessage(`Booking Ref: ${booking["booking_id"]}`);
            return booking;
        }
    } catch (error) {
        showAlert(error);
    }
}

const getEvents = async () => {
    try {
        const response = await fetch("/event", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            } 
        });
        if (!response.ok) {
            if (response.status === 400) showAlert("Invalid search");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            return await response.json();
        }
    } catch (error) {
        showAlert(error);
    }
}

const getEvent = async (event_id) => {
    try {
        const response = await fetch(`/event/${event_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            if (response.status === 400) showAlert("Invalid search");
            if (response.status === 404) showAlert("Event not found");
            if (response.status === 422) showAlert("Something went wrong");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            return await response.json();
        }
    } catch (error) {
        showAlert(error);
    }
}

const location = async (event) => {
    const div = document.createElement('div');
    const l = await getLocation(event["location_id"]);
    const country = l["country"];
    const city = l["city"];
    div.innerHTML = `
        <label for="event-location">Where:</label>
        <span id="event-location">${city}, ${country}</span>
    `;
    return div;
}

const date = (event) => {
    const div = document.createElement('div');
    const d = new Date(event["start"]);
    const hh = String(d.getHours()).padStart(2, '0');
    const mm = String(d.getMinutes()).padStart(2, '0');
    div.innerHTML = `
        <label for="event-date">When:</label>
        <span id="event-date">${d.toDateString()} ${hh}:${mm}</span>
    `;
    return div;
}

const remaining = (event) => {
    const div = document.createElement('p');
    const value = event["capacity"] - event["booked"];
    div.innerHTML = `
        <label for="event-seats">${value}</label>
        <span id="event-seats">seats remaining</span>
    `;
    return div;
}

const price = (event) => {
    const div = document.createElement('p');
    div.innerHTML = `
        <span id="event-price">${event["currency"]}</span>
        <label for="event-price">${event["price"]}</label>
    `;
    return div;
}

const desc = (event) => {
    const div = document.createElement('p');
    div.innerHTML = `
        <span id="event-desc">${event["description"]}</span>
    `;
    return div;
}

const viewBtn = () => {
    const div = document.createElement('span');
    div.textContent = "BOOK TICKETS";
    div.classList.add('view-button');
    div.classList.add('button');
    return div;
}

const eventCard = async (event) => {
    const div = document.createElement('div');
    div.classList.add('event-card');

    try {
        const name = document.createElement('h2');
        name.textContent = event["name"];
        div.append(name);
        div.append(await location(event));
        div.append(date(event));
        div.append(remaining(event));
        div.append(price(event));
        div.append(viewBtn());
        div.addEventListener('click', async () => {
            main.prepend(await viewEvent(event["event_id"]));
            document.getElementById('events-display').remove();
        });
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
        showAlert(error);
    }
    return div;
}

export const viewEvent = async (event_id) => {
    const div = document.createElement('div');
    div.classList.add('event-view');
    try {
        const event = await getEvent(event_id);
        const name = document.createElement('h2');
        name.textContent = event["name"];
        try {
            div.append(name);
            div.append(desc(event));
            div.append(await location(event));
            div.append(date(event));
            div.append(remaining(event));
            div.append(price(event));
            const book = viewBtn();
            book.id = 'book-button';
            if (account["account_id"] === "") book.textContent = "ACTIVATE YOUR ACCOUNT TO BOOK";
            if (usertoken === null) book.textContent = "LOGIN TO BOOK";
            div.append(book);

            book.addEventListener('click', () => {
                if (usertoken === null) { // not logged in
                    showBox(loginBox());
                } else if (account["account_id"] === "") { // not activated
                    showBox(activateBox());
                } else {
                    div.append(bookEvent(event));
                    book.remove();
                }
            });
        } catch (error) {
            const msg = document.createElement('p');
            msg.textContent = "Something went wrong";
            div.append(msg);
        }
        div.prepend(closeBtn(async () => {
            div.remove();
            main.append(await displayEvents());
        }));
    } catch (error) {
        showAlert(error);
    }
    return div;
}

export const bookEvent = (event) => {
    const div = document.createElement('div');
    div.id = 'booking-panel';
    div.classList.add('event-view');
    try {
        const title = document.createElement('h3');
        title.textContent = "Make booking";

        const seatsInput = document.createElement('div');
        const value = event["capacity"] - event["booked"];
        seatsInput.innerHTML = `
            <label for="booking-seats"># Seats</label>
            <input id="booking-seats" type="number" min="1" max="${value}">
        `;
        seatsInput.addEventListener('change', () => {
            let total = document.getElementById('booking-seats').value * event["price"];
            document.getElementById('booking-price').textContent = total.toFixed(2);
            document.getElementById('book-button').style.visibility = 'visible';
        });
        div.append(seatsInput);

        const price = document.createElement('div');
        price.innerHTML = `
            <label for="booking-seats">${event["currency"]}</label>
            <span id="booking-price">${event["price"]}</span>
        `;
        div.append(price);

        const book = viewBtn();
        book.id = 'book-button';
        book.style.visibility = 'hidden';
        div.append(book);

        book.addEventListener('click', async () => {
            await postBooking(event, document.getElementById('booking-seats').value, document.getElementById('booking-price').textContent);
        });
    } catch (error) {
        showAlert(error);
    }
    return div;
}

document.addEventListener('activated', async () => {
    const exists = document.getElementById('book-button');
    if (exists !== null) {
        exists.textContent = "BOOK TICKETS";
    }
});
document.addEventListener('deactivated', async () => {
    const exists = document.getElementById('book-button');
    if (exists !== null) {
        exists.textContent = "ACTIVATE YOUR ACCOUNT TO BOOK";
    }
});

document.addEventListener('loggedIn', async () => {
    const exists = document.getElementById('book-button');
    if (exists !== null) {
        exists.textContent = "BOOK TICKETS";
    }
});
document.addEventListener('loggedOut', async () => {
    const exists = document.getElementById('book-button');
    if (exists !== null) {
        exists.textContent ="LOGIN TO BOOK";
    }
});

