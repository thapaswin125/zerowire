// ZeroWire client behavior: Pagefind search mount plus keyboard shortcut.
// Pagefind assets exist only after a production build (npx pagefind --site _site),
// so everything degrades to a plain disabled input during local jekyll serve.
(function () {
  "use strict";

  function focusSearch() {
    var input = document.querySelector(
      ".zw-search .pagefind-ui__search-input, .zw-search input"
    );
    if (input) {
      input.focus();
      input.select();
    }
  }

  document.addEventListener("keydown", function (ev) {
    var tag = (ev.target.tagName || "").toLowerCase();
    var typing = tag === "input" || tag === "textarea" || ev.target.isContentEditable;
    if ((ev.key === "/" && !typing) || ((ev.ctrlKey || ev.metaKey) && ev.key === "k")) {
      ev.preventDefault();
      focusSearch();
    }
  });

  document.addEventListener("DOMContentLoaded", function () {
    var mount = document.getElementById("zw-search");
    if (!mount) return;

    if (window.PagefindUI) {
      new window.PagefindUI({
        element: "#zw-search",
        showSubResults: false,
        showImages: false,
        resetStyles: false,
        translations: { placeholder: "Search the wire" }
      });
    } else {
      var input = document.createElement("input");
      input.className = "zw-search-fallback";
      input.type = "search";
      input.placeholder = "Search (deployed site only)";
      input.title = "Pagefind indexes the built site, so search works after deploy";
      input.setAttribute("aria-label", "Search");
      mount.appendChild(input);
    }
  });
})();
