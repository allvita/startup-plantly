/* ============================================================
   PlantCare AI — front-end interactivity
   Count-up numbers, animated progress rings/bars, Chart.js charts,
   accent-color theming per plant, and HTMX re-initialization.
   ============================================================ */

const chartRegistry = {};

function animateCountUp(el) {
  const target = parseFloat(el.dataset.countup);
  const decimals = el.dataset.decimals ? parseInt(el.dataset.decimals) : 0;
  const suffix = el.dataset.suffix || "";
  const duration = 1100;
  const start = performance.now();

  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const value = target * eased;
    el.textContent = value.toFixed(decimals) + suffix;
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

function initCountUps(root = document) {
  root.querySelectorAll("[data-countup]").forEach(animateCountUp);
}

function initProgressRings(root = document) {
  root.querySelectorAll("[data-progress-ring]").forEach((svg) => {
    const value = parseFloat(svg.dataset.progressRing);
    const circle = svg.querySelector("circle.ring-value");
    if (!circle) return;
    const radius = circle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;
    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = circumference;
    requestAnimationFrame(() => {
      const offset = circumference - (value / 100) * circumference;
      circle.style.strokeDashoffset = offset;
    });
  });
}

function initBarFills(root = document) {
  root.querySelectorAll("[data-bar-fill]").forEach((bar) => {
    const value = bar.dataset.barFill;
    bar.style.width = "0%";
    requestAnimationFrame(() => {
      setTimeout(() => { bar.style.width = value + "%"; }, 60);
    });
  });
}

function destroyCharts() {
  Object.keys(chartRegistry).forEach((key) => {
    chartRegistry[key].destroy();
    delete chartRegistry[key];
  });
}

function buildLineChart(canvas) {
  const id = canvas.id;
  if (chartRegistry[id]) {
    chartRegistry[id].destroy();
  }
  const labels = JSON.parse(canvas.dataset.labels || "[]");
  const data = JSON.parse(canvas.dataset.values || "[]");
  const accent = canvas.dataset.accent || "#66E15A";
  const label = canvas.dataset.label || "";
  const isDark = document.documentElement.classList.contains("dark");

  const ctx = canvas.getContext("2d");
  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height || 220);
  gradient.addColorStop(0, hexToRgba(accent, 0.35));
  gradient.addColorStop(1, hexToRgba(accent, 0));

  chartRegistry[id] = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label,
        data,
        borderColor: accent,
        backgroundColor: gradient,
        borderWidth: 3,
        tension: 0.45,
        fill: true,
        pointRadius: 0,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: accent,
        pointHoverBorderColor: isDark ? "#171717" : "#ffffff",
        pointHoverBorderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 900, easing: "easeOutQuart" },
      plugins: { legend: { display: false }, tooltip: {
        backgroundColor: isDark ? "#171717" : "#ffffff",
        titleColor: isDark ? "#ffffff" : "#101312",
        bodyColor: isDark ? "#BEBEBE" : "#4b5045",
        borderColor: hexToRgba(accent, 0.4),
        borderWidth: 1,
        padding: 10,
        cornerRadius: 12,
        displayColors: false,
      }},
      scales: {
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: { color: isDark ? "#BEBEBE" : "#8a8f83", font: { size: 11 } },
        },
        y: {
          grid: { color: isDark ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.05)" },
          border: { display: false },
          ticks: { color: isDark ? "#BEBEBE" : "#8a8f83", font: { size: 11 } },
        },
      },
    },
  });
}

function initCharts(root = document) {
  root.querySelectorAll("canvas[data-chart]").forEach(buildLineChart);
}

function hexToRgba(hex, alpha) {
  const h = hex.replace("#", "");
  const bigint = parseInt(h.length === 3 ? h.split("").map(c => c + c).join("") : h, 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function applyAccent(root = document) {
  const marker = root.querySelector("[data-plant-accent]");
  if (marker) {
    document.documentElement.style.setProperty("--accent-secondary", marker.dataset.plantAccent);
  }
}

function initDashboardWidgets(root = document) {
  initCountUps(root);
  initProgressRings(root);
  initBarFills(root);
  initCharts(root);
  applyAccent(root);
  if (window.lucide) lucide.createIcons();
}

document.addEventListener("DOMContentLoaded", () => initDashboardWidgets(document));

document.body.addEventListener("htmx:afterSwap", (evt) => {
  initDashboardWidgets(evt.detail.target);
});

/* Sidebar mobile toggle */
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  if (sidebar) sidebar.classList.toggle("-translate-x-full");
}

/* Password visibility toggle on login page */
function togglePasswordVisibility(inputId, iconEl) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const isPassword = input.type === "password";
  input.type = isPassword ? "text" : "password";
  iconEl.setAttribute("data-lucide", isPassword ? "eye-off" : "eye");
  if (window.lucide) lucide.createIcons();
}
