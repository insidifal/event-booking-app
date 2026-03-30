import { messageBox } from './utils.js';
import { loginBtn, loginBox, registerBtn, registerBox } from './login.js';
import { profileBtn, profileBox } from './profile.js';
import { displayEvents } from './events.js';

const banner = document.getElementById('buttons');
const main = document.getElementById('main');

window.addEventListener('DOMContentLoaded', async () => {
    banner.append( loginBtn(), registerBtn() );
    main.append( messageBox(), await displayEvents(), loginBox(), registerBox() );
});

document.addEventListener('loggedIn', async () => {
    banner.prepend(profileBtn());
    main.append(await profileBox());
});

document.addEventListener('loggedOut', () => {
    banner.append( registerBtn() );
});
