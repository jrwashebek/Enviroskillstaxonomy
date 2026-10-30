// STUB: replaced by developer C. Licence: Apache-2.0.
import { h } from "../lib/dom.js";
const stub = (t) => async ({ params }) => ({ title: t, node: h("div", { class: "page-head" }, h("h1", { tabindex: "-1" }, `${t} (stub)`), h("p", JSON.stringify(params || {}))) });
export const renderTool = stub("Tool"), renderCredential = stub("Credential");
