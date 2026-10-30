// STUB: replaced by the developer who owns this view (see docs/DESIGN_SPEC.md §0). Licence: Apache-2.0.
import { h } from "../lib/dom.js";
export async function render({ params }) {
  return { title: "about", node: h("div", { class: "page-head" }, h("h1", { tabindex: "-1" }, "about (stub)"), h("p", JSON.stringify(params || {}))) };
}
