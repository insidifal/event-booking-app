import { showAlert, showMessage, showBox, hideBox, closeBtn, deleteBtn } from './utils.js';
import { usertoken } from './login.js';

const emptyAccount = {
    "account_id": "",
    "user_id": "",
    "balance": 0,
    "currency": "USD"
}

export let account = emptyAccount;
let newBalance = null;
let newCurrency = "";

export const activateEvent = new CustomEvent("activated", {
    detail: account,
    bubbles: true,
    cancelable: true
});

export const deactivateEvent = new CustomEvent("deactivated", {
    detail: emptyAccount,
    bubbles: true,
    cancelable: true
});

document.addEventListener('loggedOut', async () => {
    account = emptyAccount;
    hideBox(await accountBtn());
    hideBox(await accountBox());
});

document.addEventListener('activated', async () => {
    hideBox(await accountBtn());
    hideBox(activateBox());
});

document.addEventListener('deactivated', async () => {
    account = emptyAccount;
    hideBox(await accountBtn());
    hideBox(await accountBox());
});

export const getAccount = async () => {
    if (usertoken === null) return null;
    try {
        const response = await fetch("/user/account", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${usertoken}`
            }
        });
        if (!response.ok) {
            if (response.status === 401) showAlert("Invalid credentials");
            // if (response.status === 404) showAlert("Account does not exist");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            account = await response.json();
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

const deleteAccount = async () => {
    if (usertoken === null) return null;
    if (account["account_id"] === "") return null;
    try {
        const response = await fetch(`/user/account/${account["account_id"]}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${usertoken}`
            }
        });
        if (!response.ok) {
            if (response.status === 400) showAlert("Bad input");
            if (response.status === 401) showAlert("Invalid credentials");
            if (response.status === 404) showAlert("Account does not exist");
            if (response.status === 500) showAlert("Something went wrong");
        } else {
            account = emptyAccount;
            showMessage("Account deleted");
        }
    } catch (error) {
        showAlert(error);
    }
}

export const accountBtn = async () => {
    await getAccount();
    const div = document.createElement('div');
    if (account["account_id"] === "") {
        div.textContent = "Activate";
        div.addEventListener('click', () => {
            showBox(activateBox());
        });
    } else {
        div.textContent = "Account";
        div.addEventListener('click', async () => {
            showBox(await accountBox());
        });
    }
    div.addEventListener('activated', () => {
        div.textContent = "Account";
        div.addEventListener('click', async () => {
            showBox(await accountBox());
        });
    });
    div.addEventListener('deactivated', () => {
        div.textContent = "Activate";
        div.addEventListener('click', async () => {
            showBox(activateBox());
        });
    });

    div.id = 'account-button';
    div.classList.add('button');
    return div;
}

export const activateBox = () => {
    const div = document.createElement('div');
    const header = document.createElement('h3');
    header.textContent = "Activate your account";
    div.append(header);

    div.append(activateBtn());
    div.prepend(closeBtn(() => {
        hideBox(activateBox());
    }));
    div.id = 'activate-box';
    div.classList.add('input-box');
    return div;
}

const activateBtn = () => {
    const div = document.createElement('div');
    div.textContent = 'ACTIVATE';
    div.id = 'activate-account';
    div.classList.add('button');
    div.classList.add('submit-button');
    div.addEventListener('click', async () => {
        await openAccount();
    });
    return div;
}

export const accountBox = async () => {
    await getAccount();
    const div = document.createElement('div');
    const header = document.createElement('h3');
    header.textContent = "Manage your account";
    div.append(header);

    const balance = document.createElement('div');
    balance.innerHTML = `
        <label for="account-balance">Balance:</label>
        <span id="account-balance">${account["currency"]} ${account["balance"]}</span>
    `;
    div.append(balance);

    const deposit = document.createElement('div');
    deposit.innerHTML = `
        <label for="account-deposit">Add / Withdraw</label>
        <input id="account-deposit" type="number" min="${-1 * account["balance"]}" placeholder="0.00">
    `;
    deposit.addEventListener('change', () => {
        newBalance = document.getElementById('account-deposit').value;
        document.getElementById('confirm-account')
            .style.visibility = 'visible';
    });
    div.append(deposit);

    div.append(dropDownCurrency());
    div.append(confirmBtn());
    div.append(deleteBtn("DELETE ACCOUNT", async () => {
        await deleteAccount();
        document.dispatchEvent(deactivateEvent);
    }));

    div.prepend(closeBtn(async () => {
        hideBox(await accountBox());
        newBalance = null;
        newCurrency = "";
    }));
    div.id = 'account-box';
    div.classList.add('input-box');
    return div;
}

const dropDownCurrency = () => {
    const div = document.createElement('div');
    div.id = 'currency-dropdown';
    div.classList.add('dropdownlist');

    const label = document.createElement('label');
    label.textContent = "Currency";
    label.setAttribute("for", "currencies");
    div.append(label);

    const select = document.createElement('select');
    select.id = "currencies";
    select.name = "currencies";

    const list = ["USD"];

    for (let currency of list) {
        try {
            const opt = document.createElement('option');
            opt.value = currency;
            opt.textContent = currency;
            if (account["currency"] === currency) {
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
        newCurrency = select.value;
        document.getElementById('confirm-account')
            .style.visibility = 'visible';
    });

    div.append(select);
    return div;
}

const confirmBtn = () => {
    const div = document.createElement('div');
    div.textContent = 'CONFIRM';
    div.id = 'confirm-account';
    div.classList.add('button');
    div.classList.add('submit-button');
    div.addEventListener('click', async () => {
        if (newBalance !== null) account["balance"] = Number(account["balance"]) + Number(newBalance);
        if (newCurrency !== "") account["currency"] = newCurrency;
        await updateAccount();
        newBalance = null;
        newCurrency = "";
        hideBox(await accountBox());
    });
    div.style.visibility = 'hidden';
    return div;
}
