// In-memory UI state shared between views. Never written to storage or the URL (privacy rule).
// Licence: Apache-2.0.
export const state = {
  query: "",              // last search query (search results view reads it)
  roleFilters: null,      // {families:Set, actors:Set, depth:Set} preselected by the home page
  compFilters: null,
};
