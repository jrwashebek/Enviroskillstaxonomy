// Breadcrumbs for paginated competency pages (computed per page; Apache-2.0).
export default {
  eleventyComputed: {
    crumbs: (d) => (d.c ? [[d.c.isModule ? "/modules/" : "/competencies/", d.c.isModule ? "Module sections" : "Competencies"], ...(d.c.isModule ? [[`/modules/${d.c.module}/`, d.c.moduleLabel]] : []), [null, d.c.title]] : d.crumbs),
  },
};
