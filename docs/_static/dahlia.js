function color() {
  return document.querySelectorAll(".format-code").forEach((v) => {
    v.querySelectorAll("tbody td").forEach((td) => {
      const text = td.textContent.trim();
      if (text.startsWith("#")) {
        td.style.setProperty("--clr", text);
      }
    });
  });
}

function dataHighlight() {
  return document.querySelectorAll("#data-highlight").forEach((pre) => {
    pre.querySelectorAll("span").forEach((span) => {
      const color = span.getAttribute("color");
      if (!color) return;
      span.style.color = color;
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  color();
  dataHighlight();
});
