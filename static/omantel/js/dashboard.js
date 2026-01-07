window.addEventListener("DOMContentLoaded", () => {
  const statusEl = document.getElementById("statusChart");
  if (statusEl) {
    const open = Number(statusEl.dataset.open || 0);
    const inprog = Number(statusEl.dataset.inprogress || 0);
    new Chart(statusEl, {
      type: "doughnut",
      data: { labels: ["In Progress", "Open"], datasets: [{ data: [inprog, open] }] },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });
  }

  const priorityEl = document.getElementById("priorityChart");
  if (priorityEl) {
    const labels = (priorityEl.dataset.labels || "").split(",").filter(Boolean);
    const values = (priorityEl.dataset.values || "").split(",").map(Number);
    new Chart(priorityEl, {
      type: "bar",
      data: { labels, datasets: [{ data: values }] },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
      }
    });
  }

  const categoryEl = document.getElementById("categoryChart");
  if (categoryEl) {
    const labels = (categoryEl.dataset.labels || "").split(",").filter(Boolean);
    const values = (categoryEl.dataset.values || "").split(",").map(Number);
    new Chart(categoryEl, {
      type: "pie",
      data: { labels, datasets: [{ data: values }] },
      options: { responsive: true }
    });
  }
});
