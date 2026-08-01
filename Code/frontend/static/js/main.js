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

// fades/slides .reveal elements in once they scroll into view, used for cards
// and the hero/stats content. no IntersectionObserver support just shows
// everything immediately instead of leaving it stuck invisible.
document.addEventListener("DOMContentLoaded", () => {
  const revealEls = document.querySelectorAll(".reveal");
  if (!revealEls.length) {
    return;
  }

  if (!("IntersectionObserver" in window)) {
    revealEls.forEach((el) => el.classList.add("revealed"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  revealEls.forEach((el) => observer.observe(el));
});

// counts a .stats__number up from 0 to its data-count once it scrolls into view
document.addEventListener("DOMContentLoaded", () => {
  const numbers = document.querySelectorAll(".stats__number");
  if (!numbers.length || !("IntersectionObserver" in window)) {
    return;
  }

  const countUp = (el) => {
    const target = parseInt(el.dataset.count, 10) || 0;
    const duration = 1200;
    const start = performance.now();

    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      el.textContent = Math.round(progress * target);
      if (progress < 1) {
        requestAnimationFrame(tick);
      }
    };
    requestAnimationFrame(tick);
  };

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          countUp(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.6 }
  );

  numbers.forEach((el) => observer.observe(el));
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
