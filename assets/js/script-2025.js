const header = document.querySelector('.header');
const headerMenuWrapper = header.querySelector('.header__menu-wrapper');
const headerInner = header.querySelector('.header__inner');
const burgerBtn = header.querySelector('.burger-btn');
const mobileMenu = header.querySelector('.mobile-menu');
const mobileMenuLinks = [...mobileMenu.querySelectorAll('.mobile-menu__link')];
const body = document.querySelector('body');

let headerHeight;

function updateHeaderHeight() {
    headerHeight = headerMenuWrapper.clientHeight;
    header.style.height = headerHeight + 'px';
}

function updateMobileMenuPosition() {
    mobileMenu.style.top = headerMenuWrapper.getBoundingClientRect().bottom + 'px';
}


function fixMenu() {
    !headerMenuWrapper.classList.contains('header__menu-wrapper_fixed')
    && headerMenuWrapper.classList.add('header__menu-wrapper_fixed');
}

function unfixMenu() {
    headerMenuWrapper.classList.contains('header__menu-wrapper_fixed')
    && headerMenuWrapper.classList.remove('header__menu-wrapper_fixed');
}

function scrollHandler() {
    window.scrollY > headerHeight ? fixMenu() : unfixMenu();
    updateMobileMenuPosition();
}

function resizeHandler() {
    console.log('resize');
    if (headerHeight === headerMenuWrapper.clientHeight) return;
    console.log(headerHeight);
    updateHeaderHeight();
    console.log(headerHeight);
}

function openMobileMenu() {
    burgerBtn.classList.add('burger-btn_active');
    mobileMenu.classList.add('mobile-menu_active');
    body.classList.add('no-scroll');
    mobileMenuLinks.forEach(link => link.addEventListener('click', closeMobileMenu));
}

function closeMobileMenu() {
    burgerBtn.classList.remove('burger-btn_active');
    mobileMenu.classList.remove('mobile-menu_active');
    body.classList.remove('no-scroll');
    mobileMenuLinks.forEach(link => link.removeEventListener('click', closeMobileMenu));
}

function burgerBtnClickHandler() {
    burgerBtn.classList.contains('burger-btn_active')
        ? closeMobileMenu()
        : openMobileMenu();
}

function init() {
    updateHeaderHeight();
    updateMobileMenuPosition();
    window.addEventListener("scroll", scrollHandler);
    window.addEventListener("resize", resizeHandler);
    burgerBtn.addEventListener("click", burgerBtnClickHandler);
}

init();