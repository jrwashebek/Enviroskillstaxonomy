// Breadcrumbs for paginated series pages (Apache-2.0).
export default { eleventyComputed: { crumbs: (d) => d.s ? [["/federal-series/", "Federal series"], [null, `${d.s.code} ${d.s.title}`]] : d.crumbs } };
