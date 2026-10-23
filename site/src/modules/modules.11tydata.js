// Breadcrumbs for paginated module pages (Apache-2.0).
export default { eleventyComputed: { crumbs: (d) => d.md ? [["/modules/", "Module sections"], [null, d.md.label]] : d.crumbs } };
