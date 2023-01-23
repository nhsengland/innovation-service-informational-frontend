/**
 * Header multilevel navigation component behaviours.
 */

// Handle menu opening and closing.
function headerOpenCloseNavigationMenu(e) {

  const navElement = document.getElementById('header-navigation').classList;
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
//         document.getElementById('header-navigation').classList.remove('children-items-height');
//       }
//     }
//   }

// }



/**
 * Accordion component behaviours.
 */
function updateAccordionShowHideAllButton(accordionElement) {

  const showHideAllButton = accordionElement.querySelector('.app-accordion__show-hide-all-button');
  const sectionsNumber = accordionElement.querySelectorAll('.app-accordion__section').length;
  const sectionsOpened = accordionElement.querySelectorAll('.app-accordion__section-button[aria-expanded="true"]').length;

  if (!showHideAllButton) {
    console.error('Missing element with "app-accordion__show-hide-all-button" class. Please, review any missing HTML nodes.');
  }

  if (sectionsNumber === sectionsOpened) {
    showHideAllButton.ariaExpanded = true;
    showHideAllButton.children[0].classList.remove('app-accordion__chevron--down');
    showHideAllButton.children[0].classList.add('app-accordion__chevron--up');
    showHideAllButton.children[1].innerHTML = 'Hide all sections';
  } else {
    showHideAllButton.ariaExpanded = false;
    showHideAllButton.children[0].classList.remove('app-accordion__chevron--up');
    showHideAllButton.children[0].classList.add('app-accordion__chevron--down');
    showHideAllButton.children[1].innerHTML = 'Show all sections';
  }

}

function handleAccordionSection(sectionElement, action = 'toggle') {

  const sectionButton = sectionElement.querySelector('.app-accordion__section-button');
  const sectionContent = sectionElement.querySelector('.app-accordion__section-content');
  const sectionChevron = sectionElement.querySelector('.app-accordion__chevron');

  if (!sectionButton && !sectionButton[0]) {
    console.error('Missing element with "app-accordion__section-button" class. Please, review any missing HTML nodes.');
    return;
  }
  if (!sectionContent && !sectionContent[0]) {
    console.error('Missing element with "app-accordion__section-content" class. Please, review any missing HTML nodes.');
    return;
  }
  if (!sectionChevron && !sectionChevron[0]) {
    console.error('Missing element with "app-accordion__chevron" class. Please, review any missing HTML nodes.');
    return;
  }

  if (action === 'toggle') {
    action = sectionButton.ariaExpanded === 'true' ? 'close' : 'open';
  }

  if (action === 'close') {

    sectionButton.ariaLabel = `${sectionElement.getAttribute('data-label')}, show this section`;
    sectionButton.ariaExpanded = false;

    sectionChevron.classList.add('app-accordion__chevron--down');
    sectionChevron.nextElementSibling.innerHTML = 'Show';

    sectionContent.classList.add('d-none');

  } else {

    sectionButton.ariaLabel = `${sectionElement.getAttribute('data-label')}, hide this section`;
    sectionButton.ariaExpanded = true;

    sectionChevron.classList.remove('app-accordion__chevron--down');
    sectionChevron.nextElementSibling.innerHTML = 'Hide';

    sectionContent.classList.remove('d-none');

  }

  document.activeElement?.blur();

}


// Initialize and attach onClick events to accordion buttons.
for (let accordionElement of document.querySelectorAll('.app-accordion')) {

  // Initialize show/hide all button.
  updateAccordionShowHideAllButton(accordionElement);

  // Attach show/hide all button events.
  const e = accordionElement.querySelector('.app-accordion__show-hide-all-button');
  e.onclick = function () {

    for (let e of accordionElement.querySelectorAll('.app-accordion__section')) {
      handleAccordionSection(e, this.ariaExpanded === 'true' ? 'close' : 'open');
    };

    updateAccordionShowHideAllButton(accordionElement);

  }

  // Initialize and attach sections show/hide button events.
  for (let sectionElement of accordionElement.querySelectorAll('.app-accordion__section')) {

    const sectionButton = sectionElement.querySelector('.app-accordion__section-button');
    handleAccordionSection(sectionElement, sectionButton.ariaExpanded === 'true' ? 'open' : 'close');

    sectionButton.onclick = function () {
      handleAccordionSection(sectionElement, 'toggle');
      updateAccordionShowHideAllButton(accordionElement);
    };

  }

}
