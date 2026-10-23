// Breadcrumbs for paginated role and variant pages (Apache-2.0).
export default {
  eleventyComputed: {
    crumbs: (d) => d.v ? [["/roles/", "Roles"], [d.v.role.url, d.v.role.title], [null, d.v.actorLabel]]
      : d.role ? [["/roles/", "Roles"], [null, d.role.title]] : d.crumbs,
  },
};
