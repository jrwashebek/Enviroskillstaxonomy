// Breadcrumbs for paginated class pages (Apache-2.0).
export default { eleventyComputed: { crumbs: (d) => d.s ? [["/state-classes/", "State and local classes"], [null, `${d.s.title} (${d.s.jurisdiction} ${d.s.code})`]] : d.crumbs } };
