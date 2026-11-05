// Reuse the conference photo viewer, including keyboard controls and focus return.
if (document.querySelector('.meetup-photo-link')) {
  new ImgPopUp('.meetup-photo-link', { nav: true });
}
