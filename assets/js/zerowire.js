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

  function applyFilter(filter) {
    var feed = document.querySelector(".zw-feed");
    if (!feed) return;
    feed.querySelectorAll(".zw-card").forEach(function (card) {
      var show =
        filter === "all" ||
        (filter === "kev"
          ? card.dataset.kev === "true"
          : card.dataset.severity === filter);
      card.classList.toggle("zw-hidden", !show);
    });
    // Hide date dividers whose whole day is filtered out.
    feed.querySelectorAll(".zw-date-divider").forEach(function (divider) {
      var anyVisible = false;
      var node = divider.nextElementSibling;
      while (node && !node.classList.contains("zw-date-divider")) {
        if (node.classList.contains("zw-card") && !node.classList.contains("zw-hidden")) {
          anyVisible = true;
          break;
        }
        node = node.nextElementSibling;
      }
      divider.classList.toggle("zw-hidden", !anyVisible);
    });
  }

  function initFilters() {
    var bar = document.querySelector(".zw-filters");
    if (!bar) return;
    bar.addEventListener("click", function (ev) {
      var btn = ev.target.closest(".zw-filter");
      if (!btn) return;
      bar.querySelectorAll(".zw-filter").forEach(function (b) {
        b.classList.toggle("active", b === btn);
      });
      applyFilter(btn.dataset.filter);
    });
  }

  function initExpanders() {
    document.querySelectorAll(".zw-card-summary").forEach(function (summary) {
      if (summary.scrollHeight <= summary.clientHeight + 2) return;
      var btn = document.createElement("button");
      btn.className = "zw-more";
      btn.type = "button";
      btn.textContent = "more";
      btn.addEventListener("click", function () {
        var expanded = summary.classList.toggle("zw-expanded");
        btn.textContent = expanded ? "less" : "more";
      });
      summary.insertAdjacentElement("afterend", btn);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initFilters();
    initExpanders();

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
