const mainMenu = document.querySelector('.mainMenu');
const closeMenu = document.querySelector('.closeMenu');
const openMenu = document.querySelector('.openMenu');



openMenu.addEventListener('click', show);
closeMenu.addEventListener('click', close);

function show() {
    mainMenu.style.display = 'flex';
    mainMenu.style.top = '0';
    document.getElementById('offwhenreq').style.display = 'none';
    // document.getElementsByTagName('body').style.display = 'none';
}

function close() {
    mainMenu.style.top = '-125%';
    document.getElementById('offwhenreq').style.display = 'inline-block';
}