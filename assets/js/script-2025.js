const header = document.querySelector('.header');
const headerMenuWrapper = header.querySelector('.header__menu-wrapper');
const headerInner = header.querySelector('.header__inner');

let headerHeight;

function updateHeaderHeight() {
    if (headerHeight === headerMenuWrapper.offsetHeight) return;
    headerHeight = headerMenuWrapper.offsetHeight;
    header.style.height = headerHeight + 'px';
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
}

function resizeHandler() {
    if (headerHeight === headerMenuWrapper.offsetHeight) return;
    updateHeaderHeight();
}

function init() {
    updateHeaderHeight();
    window.addEventListener("scroll", scrollHandler);
    window.addEventListener("resize", resizeHandler);
}

init();