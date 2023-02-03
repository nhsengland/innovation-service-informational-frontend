/**
 * Accordion component behaviours.
 */
function updateAccordionShowHideAllButton(accordionElement) {

  const showHideAllButton = accordionElement.querySelector('button[data-type="show-hide-all-sections"]');
  const sectionsNumber = accordionElement.querySelectorAll('.app-accordion__section').length;
  const sectionsOpened = accordionElement.querySelectorAll('button[data-type="show-hide-section"][aria-expanded="true"]').length;

  if (!showHideAllButton) {
    console.error('Missing element button[data-type="show-hide-all-sections"]. Please, review any missing HTML nodes.');
  }

  if (sectionsNumber === sectionsOpened) {
    showHideAllButton.ariaExpanded = true;
    showHideAllButton.children[0].innerHTML = `Hide all ${showHideAllButton.getAttribute('data-label')}`;
    showHideAllButton.children[1].classList.remove('app-accordion__chevron--down');
    showHideAllButton.children[1].classList.add('app-accordion__chevron--up');
  } else {
    showHideAllButton.ariaExpanded = false;
    showHideAllButton.children[0].innerHTML = `Show all ${showHideAllButton.getAttribute('data-label')}`;
    showHideAllButton.children[1].classList.remove('app-accordion__chevron--up');
    showHideAllButton.children[1].classList.add('app-accordion__chevron--down');

  }

}

function handleAccordionSection(sectionElement, action) {

  const localStorageVariable = `${sectionElement.parentElement.id}-accordion-component`;
  const sectionButton = sectionElement.querySelector('button[data-type="show-hide-section"]');
  const sectionContent = sectionElement.querySelector('.app-accordion__section-content');

  if (!sectionButton || !sectionButton.children[0] || !sectionButton.children[1]) {
    console.error('Missing element button[data-type="show-hide-section"] (or one of its children). Please, review any missing HTML nodes.');
    return;
  }
  if (!sectionContent) {
    console.error('Missing element with "app-accordion__section-content" class. Please, review any missing HTML nodes.');
    return;
  }

  let componentStorage = {};
  try {
    componentStorage = JSON.parse(localStorage.getItem(localStorageVariable)) ?? {};
  } catch (error) {
    console.error('Error reading localStorgage');
  }

  switch (action) {
    case 'toggle':
      action = sectionButton.ariaExpanded === 'true' ? 'close' : 'open';
      break;
    case 'default':
      const localStorageValue = componentStorage[sectionButton.getAttribute('aria-controls')];
      action = localStorageValue ?? sectionButton.ariaExpanded === 'true' ? 'open' : 'close';
      break;
    default:
      break;
  }


  if (action === 'close') {

    sectionButton.ariaLabel = `Show ${sectionButton.getAttribute('data-label')}`;
    sectionButton.ariaExpanded = false;
    sectionButton.children[0].innerHTML = 'Show';
    sectionButton.children[1].classList.add('app-accordion__chevron--down');

    sectionContent.classList.add('d-none');

    componentStorage[sectionButton.getAttribute('aria-controls')] = false;

  } else {

    sectionButton.ariaLabel = `Hide ${sectionButton.getAttribute('data-label')}`;
    sectionButton.ariaExpanded = true;
    sectionButton.children[0].innerHTML = 'Hide';
    sectionButton.children[1].classList.remove('app-accordion__chevron--down');

    sectionContent.classList.remove('d-none');

    componentStorage[sectionButton.getAttribute('aria-controls')] = true;

  }

  document.activeElement?.blur();

  localStorage.setItem(localStorageVariable, JSON.stringify(componentStorage));

}


// Initialize and attach onClick events to accordion buttons.
for (let accordionElement of document.querySelectorAll('.app-accordion')) {

  // Initialize and attach sections show/hide button events.
  for (let sectionElement of accordionElement.querySelectorAll('.app-accordion__section')) {

    const sectionButton = sectionElement.querySelector('button[data-type="show-hide-section"]');
    handleAccordionSection(sectionElement, 'default');

    sectionButton.onclick = function () {
      handleAccordionSection(sectionElement, 'toggle');
      updateAccordionShowHideAllButton(accordionElement);
    };

  }

  // Initialize show/hide all button.
  updateAccordionShowHideAllButton(accordionElement);

  // Attach show/hide all button events.
  const e = accordionElement.querySelector('button[data-type="show-hide-all-sections"]');
  e.onclick = function () {

    for (let e of accordionElement.querySelectorAll('.app-accordion__section')) {
      handleAccordionSection(e, this.ariaExpanded === 'true' ? 'close' : 'open');
    };

    updateAccordionShowHideAllButton(accordionElement);

  }

  // Display component.
  accordionElement.parentElement.querySelector('.app-loader').classList.add('d-none');
  accordionElement.classList.remove('d-none');

}
