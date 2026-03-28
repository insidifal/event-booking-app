const loadPage = async () => {
    const banner = document.getElementById('banner')
    const main = document.getElementById('main')
    banner.append(loginBtn());
    main.append(await loginBox(), messageBox());
}

window.addEventListener('DOMContentLoaded', () => {
    loadPage();
});

