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

// contact form submit, posts JSON to /api/contact and shows inline validation
// errors and a status message instead of reloading the page
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contact-form");
  if (!form) {
    return;
  }

  const status = document.getElementById("contact-status");
  const submitButton = form.querySelector('button[type="submit"]');
  const sendLabel = submitButton.textContent;

  const errorMessages = {
    name: form.dataset.errName,
    email: form.dataset.errEmail,
    message: form.dataset.errMessage,
  };

  const setStatus = (text, kind) => {
    status.textContent = text || "";
    status.hidden = !text;
    status.className = "contact-form__status" + (kind ? ` contact-form__status--${kind}` : "");
  };

  const clearErrors = () => {
    form.querySelectorAll(".contact-form__error").forEach((el) => {
      el.textContent = "";
    });
  };

  const showErrors = (errors) => {
    clearErrors();
    Object.keys(errors).forEach((field) => {
      const el = form.querySelector(`[data-error-for="${field}"]`);
      if (el) {
        el.textContent = errorMessages[field] || "";
      }
    });
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearErrors();
    setStatus("");

    const data = Object.fromEntries(new FormData(form).entries());

    submitButton.disabled = true;
    submitButton.textContent = form.dataset.msgSending;

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const result = await response.json();

      if (result.ok) {
        form.reset();
        setStatus(form.dataset.msgSuccess, "success");
      } else if (result.errors) {
        showErrors(result.errors);
      } else if (response.status === 429) {
        setStatus(form.dataset.msgRateLimited, "error");
      } else {
        setStatus(form.dataset.msgError, "error");
      }
    } catch (err) {
      setStatus(form.dataset.msgError, "error");
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = sendLabel;
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
