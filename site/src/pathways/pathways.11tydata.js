// Breadcrumbs for paginated pathway pages (Apache-2.0).
export default { eleventyComputed: { crumbs: (d) => d.v ? [["/pathways/", "Pathways"], [d.v.role.url, d.v.role.title], [null, d.v.actorLabel]] : d.crumbs } };
