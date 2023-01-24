
/**
 * Add CSS class to body if javacript is enabled.
 */
document.body.classList.add('js-enabled');


/**
 * Header multilevel navigation component behaviours.
 */

// Handle menu opening and closing.
function headerOpenCloseNavigationMenu(e) {

  const navElement = document.querySelector('#header-navigation').classList;
  const isMenuOpened = navElement.contains('children-items-height');

  if (isMenuOpened) {
    e.classList.replace('button-open', 'button-closed');
    e.nextElementSibling.classList.add('d-none');
    e.ariaLabel = `Open ${e.getAttribute('data-label')} menu`;
    e.ariaExpanded = false;
    document.activeElement?.blur();
  } else {
    e.classList.replace('button-closed', 'button-open');
    e.nextElementSibling.classList.remove('d-none');
    e.ariaLabel = `Close ${e.getAttribute('data-label')} menu`;
    e.ariaExpanded = true;
  }

  navElement.toggle('children-items-height');

}

// Attach onClick event to navigation menu buttons.
for (let e of document.getElementsByClassName('app-multilevel-navigation__toggle-button')) {
  e.onclick = function () { headerOpenCloseNavigationMenu(this) };
}

// Posssible behaviour: Close navigation menus dropdown if the user clicks outside of it
// window.onclick = function (event) {

//   if (!event.target.matches('.app-multilevel-navigation__toggle-button')) {

//     for (let e of document.getElementsByClassName('app-multilevel-navigation__toggle-button')) {

//       if (e.classList.contains('button-open')) {
//         e.classList.replace('button-open', 'button-closed');
//         e.nextElementSibling.classList.add('d-none');
//         e.ariaLabel = `Open ${e.getAttribute('data-label')} menu`;
//         e.ariaExpanded = false;
//         document.querySelector('#header-navigation').classList.remove('children-items-height');
//       }
//     }
//   }

// }


/**
 * Header cookies management behaviours.
 */
(function () {

  if (!getConsentCookie().consented) {
    document.querySelector('#cookie-banner').classList.remove('d-none');
  }

  document.querySelector('#save-cookies-button-ok')?.addEventListener('click', () => {
    document.querySelector('#cookie-banner').classList.add('d-none');
    document.querySelector('#cookie-banner-success').classList.remove('d-none');
    setConsentCookie(true);
  });

  document.querySelector('#save-cookies-button-nok')?.addEventListener('click', function () {
    document.querySelector('#cookie-banner').classList.add('d-none')
    document.querySelector('#cookie-banner-success').classList.remove('d-none');
    setConsentCookie(false);
    deleteAnalyticsCookies();
  });

})();
