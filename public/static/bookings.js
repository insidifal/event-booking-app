import { showAlert, showMessage, showBox, hideBox, closeBtn, deleteBtn } from './utils.js';
import { usertoken } from './login.js';
import { account } from './account.js';
import { user } from './profile.js';
import { getEvent } from './events.js';

const fragment = document.createDocumentFragment();

document.addEventListener('loggedOut', async () => {
    hideBox(bookingsBtn());
});

const getBookings = async () => {
    if (usertoken === null) return null;
    try {
        const response = await fetch("/booking", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${usertoken}`
            }
        });
        if (!response.ok) {
            if (response.status === 401) showAlert("Invalid credentials");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            return await response.json();
        }
    } catch (error) {
        showAlert(error);
    }
}

const openAccount = async () => {
    if (usertoken === null) return null;
    try {
        const response = await fetch("/user/account", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${usertoken}`
            }
        });
        if (!response.ok) {
            if (response.status === 401) showAlert("Invalid credentials");
            if (response.status === 404) showAlert("User does not exist");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            account = await response.json();
            showMessage("Account activated");
            document.dispatchEvent(activateEvent);
        }
    } catch (error) {
        showAlert(error);
    }
}

const updateAccount = async () => {
    if (usertoken === null) return null;
    try {
        const response = await fetch("/user/account", {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${usertoken}`
            },
            body: JSON.stringify({
                'account_id': account['account_id'],
                'user_id': account['user_id'],
                'balance': account['balance'],
                'currency': account['currency']
            })
        });
        if (!response.ok) {
            if (response.status === 401) showAlert("Invalid credentials");
            if (response.status === 404) showAlert("Not found");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            account = await response.json();
            showMessage("Account updated");
        }
    } catch (error) {
        showAlert(error);
    }
}

const cancelBooking = async (booking_id) => {
    if (usertoken === null) return null;
    try {
        const response = await fetch(`/booking/${booking_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${usertoken}`
            }
        });
        if (!response.ok) {
            if (response.status === 400) showAlert("Bad input");
            if (response.status === 401) showAlert("Invalid credentials");
            if (response.status === 404) showAlert("Booking does not exist");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            showMessage("Booking cancelled, account refunded");
        }
    } catch (error) {
        showAlert(error);
    }
}

export const bookingsBtn = () => {
    const div = document.createElement('div');
    div.textContent = "Bookings";
    div.addEventListener('click', async () => {
        showBox(await bookingsBox());
    });

    div.id = 'bookings-button';
    div.classList.add('button');
    return div;
}

const bookingCard = async (booking) => {
    const div = document.createElement('div');
    div.classList.add('booking-card');
    const event_id = booking["event_id"];

    try {
        const event = await getEvent(event_id);
        const name = document.createElement('h3');
        name.textContent = event["name"];
        div.append(name);

        const seats = document.createElement('p');
        seats.textContent = `${booking["seats"]} seats`;
        div.append(seats);

        const price = document.createElement('div');
        price.innerHTML = `
            <label for="seats">${booking["currency"]}</label>
            <span id="price">${booking["total_price"]}</span>
        `;
        div.append(price);

        div.append(deleteBtn("Cancel", async () => {
            await cancelBooking(booking["booking_id"]);
            div.remove();
        }));
    } catch (error) {
        const msg = document.createElement('p');
        msg.textContent = "Something went wrong";
        div.append(msg);
    }

    fragment.appendChild(div);
}

export const bookingsBox = async () => {
    const div = document.createElement('div');
    const header = document.createElement('h3');
    header.textContent = "Bookings";
    div.append(header);
    try {
        const bookings = await getBookings();
        for (let booking of bookings) {
            await bookingCard(booking);
        }
        div.appendChild(fragment);
    } catch (error) {
        showAlert(error);
    }

    div.prepend(closeBtn(async () => {
        div.remove();
    }));
    div.id = 'bookings-box';
    div.classList.add('input-box');
    return div;
}
