document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("site-nav");

  if (!toggle || !nav) {
    return;
  }

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("site-nav--open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  const currentPath = window.location.pathname;
  nav.querySelectorAll("a").forEach((link) => {
    if (link.getAttribute("href") === currentPath) {
      link.setAttribute("aria-current", "page");
    }
  });
});

// CTA click logging, fires in the background and never blocks the link from opening
document.addEventListener("DOMContentLoaded", () => {
  if (!navigator.sendBeacon) {
    return;
  }

  document.querySelectorAll(".js-track-click").forEach((link) => {
    link.addEventListener("click", () => {
      const payload = JSON.stringify({
        slug: link.dataset.clickSlug,
        lang: link.dataset.clickLang,
      });
      navigator.sendBeacon("/api/click", new Blob([payload], { type: "application/json" }));
    });
  });
});
