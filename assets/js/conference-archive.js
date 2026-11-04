// Native details stays usable without JavaScript; start compact on small screens.
const archiveContents = document.querySelector('.archive-sidebar details');
if (archiveContents) {
  const smallScreen = window.matchMedia('(max-width: 900px)');
  const sizeContents = () => { archiveContents.open = !smallScreen.matches; };
  sizeContents();
  smallScreen.addEventListener('change', sizeContents);
}
