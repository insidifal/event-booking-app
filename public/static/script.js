import { loginBtn, registerBtn } from './login.js';
import { profileBtn } from './profile.js';
import { displayEvents } from './events.js';
import { accountBtn } from './account.js';

const banner = document.getElementById('buttons');
const main = document.getElementById('main');

window.addEventListener('DOMContentLoaded', async () => {
    banner.append( loginBtn(), registerBtn() );
    main.append( await displayEvents() );
});

document.addEventListener('loggedIn', async () => {
    banner.prepend(await accountBtn(), profileBtn());
});
document.addEventListener('loggedOut', () => {
    banner.append( registerBtn() );
});

document.addEventListener('activated', async () => {
    banner.prepend(await accountBtn());
});
document.addEventListener('deactivated', async () => {
    banner.prepend(await accountBtn());
});

