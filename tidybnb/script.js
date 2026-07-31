// Mobile nav toggle
const toggle = document.querySelector(".nav-toggle");
const links = document.querySelector(".nav-links");

if (toggle && links) {
  toggle.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
  });

  // Close menu when a link is tapped
  links.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", () => {
      links.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    })
  );
}

// Current year in footer
const yearEl = document.getElementById("year");
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Pre-select the contact form's service when arriving from a "Get a quote" button
// (e.g. contact.html?service=Turnover+Cleaning)
const params = new URLSearchParams(window.location.search);
const requestedService = params.get("service");
if (requestedService) {
  const select = document.querySelector('.contact-form select[name="service"]');
  if (select) {
    const match = Array.from(select.options).find(
      (o) => o.value === requestedService || o.text === requestedService
    );
    if (match) select.value = match.value;
  }
}
