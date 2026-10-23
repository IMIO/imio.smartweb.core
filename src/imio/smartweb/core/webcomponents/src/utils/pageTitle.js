// Title rendered by Plone for the page hosting the view. The detail views replace it with the
// title of the item, so the list views have to put it back when the visitor comes back to them.
// Captured when this module is first evaluated, i.e. before any view had a chance to change it.
const initialTitle = document.title;

export const restoreInitialTitle = () => {
    document.title = initialTitle;
};
