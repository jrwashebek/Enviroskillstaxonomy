// Breadcrumbs for paginated gap-check pages (Apache-2.0).
export default { eleventyComputed: { crumbs: (d) => d.v ? [["/gap-check/", "Gap check"], [d.v.role.url, d.v.role.title], [null, d.v.actorLabel]] : d.crumbs } };
