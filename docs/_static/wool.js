function color() {
  console.log("COLORING");
  return document.querySelectorAll(".format-code").forEach((v) => {
    v.querySelectorAll("tbody td").forEach((td) => {
      const text = td.textContent.trim();
      if (text.startsWith("#")) {
        td.style.setProperty("--clr", text);
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  color();
  console.log("LOADED");
});
