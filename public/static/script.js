import { messageBox } from './utils.js';
import { loginBtn, loginBox, registerBtn, registerBox } from './login.js';
import { profileBtn } from './profile.js';

const banner = document.getElementById('buttons');
const main = document.getElementById('main');

window.addEventListener('DOMContentLoaded', () => {
    banner.append( loginBtn(), registerBtn() );
    main.append( loginBox(), registerBox(), messageBox() );
});

document.addEventListener('loggedIn', () => {
    banner.prepend(profileBtn());
    document.getElementById('register-button').remove();
});

document.addEventListener('loggedOut', () => {
    document.getElementById('profile-button').remove();
});

