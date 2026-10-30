// Formatting helpers. Licence: Apache-2.0.
export const fmt = (n) => (n === null || n === undefined || Number.isNaN(n) ? "—" : Number(n).toLocaleString("en-US"));
export const plural = (n, one, many = one + "s") => `${fmt(n)} ${n === 1 ? one : many}`;
export const cap = (s) => (s ? s[0].toUpperCase() + s.slice(1) : "");
export function truncate(s, n) {
  s = String(s || "");
  if (s.length <= n) return s;
  const cut = s.slice(0, n);
  const sp = cut.lastIndexOf(" ");
  return (sp > n * 0.6 ? cut.slice(0, sp) : cut).replace(/[,;:.\s]+$/, "") + "…";
}
export function dateLong(iso) {
  if (!iso) return "";
  const [y, m, d] = String(iso).split("-").map(Number);
  if (!y) return String(iso);
  const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  return d ? `${d} ${months[m - 1]} ${y}` : m ? `${months[m - 1]} ${y}` : String(y);
}
export const levelName = (core, code) => core?.labels?.level?.[code] || code;
export const byTitle = (a, b) => String(a.title || a.t || "").localeCompare(String(b.title || b.t || ""));
