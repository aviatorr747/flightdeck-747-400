document.addEventListener("DOMContentLoaded", () => {
  const menu = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav");
  if (menu && nav) {
    menu.addEventListener("click", () => {
      const open = nav.classList.toggle("nav-open");
      menu.setAttribute("aria-expanded", String(open));
    });
  }

  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }

  document.querySelectorAll(".copy-prompt").forEach((button) => {
    button.addEventListener("click", async () => {
      const text = button.dataset.copy || "";
      const status = document.querySelector(".copy-status");
      try {
        await navigator.clipboard.writeText(text);
        if (status) status.textContent = "Copied to clipboard.";
        const original = button.dataset.original || button.textContent;
        button.dataset.original = original;
        button.textContent = "COPIED ✓";
        window.setTimeout(() => { button.textContent = original; }, 1400);
      } catch {
        if (status) status.textContent = "Clipboard access unavailable. Select and copy the prompt manually.";
      }
    });
  });
});
