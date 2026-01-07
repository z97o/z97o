document.addEventListener("DOMContentLoaded", function () {
  // --- Map setup
  const map = L.map("map").setView([21.4735, 55.9754], 6); // Oman center
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© OpenStreetMap contributors",
  }).addTo(map);

  const markers = L.markerClusterGroup();
  map.addLayer(markers);

  // --- Controls: legend (moved into map corner)
  const legendEl = document.getElementById("legend");
  const LegendControl = L.Control.extend({
    options: { position: "bottomleft" },
    onAdd: function () {
      const div = L.DomUtil.create("div", "leaflet-control legend-control");
      div.innerHTML = legendEl.innerHTML;
      div.style.background = "#fff";
      div.style.padding = "10px";
      div.style.borderRadius = "8px";
      div.style.boxShadow = "0 0 10px #00000022";
      div.style.fontSize = "13px";
      // prevent map drag when interacting with control
      L.DomEvent.disableClickPropagation(div);
      return div;
    },
  });
  map.addControl(new LegendControl());

  // --- DOM
  const regionSel = document.getElementById("regionFilter");
  const techSel = document.getElementById("techFilter");
  const signalSel = document.getElementById("signalFilter");
  const windowSel = document.getElementById("windowFilter");
  const applyBtn = document.getElementById("applyFilter");
  const resetBtn = document.getElementById("resetFilter");

  // --- Helpers
  const urlParams = new URLSearchParams(window.location.search);
  function getParam(name) {
    return urlParams.get(name) || "";
  }
  function setParams(params) {
    const sp = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => { if (v) sp.set(k, v); });
    const q = sp.toString();
    const newUrl = q ? `${window.location.pathname}?${q}` : window.location.pathname;
    window.history.replaceState({}, "", newUrl);
  }

  function colorBySignal(signal) {
    switch ((signal || "").toLowerCase()) {
      case "good": return "#22c55e";
      case "moderate": return "#facc15";
      case "poor": return "#ef4444";
      case "down": return "#9ca3af";
      default: return "#3b82f6";
    }
  }

  function makeIcon(color) {
    // Round colored dot
    return L.divIcon({
      className: "marker-dot",
      html:
        `<div style="
          width:14px;height:14px;border-radius:50%;
          background:${color};
          border:2px solid #fff; box-shadow:0 0 4px #00000055;"></div>`,
      iconSize: [14, 14],
      iconAnchor: [7, 7],
    });
  }

  // --- Load filters dynamically
  fetch(`/dashboard/api/map-filters/`)
    .then(r => r.json())
    .then(({ regions, technologies, signals, windows }) => {
      // Populate selects
      regions.forEach(v => regionSel.add(new Option(v, v)));
      technologies.forEach(v => techSel.add(new Option(v, v)));
      // Sort signals into preferred order if they match known set
      const knownOrder = ["Good", "Moderate", "Poor", "Down"];
      const orderedSignals = signals.slice().sort((a, b) => {
        const ia = knownOrder.indexOf(a);
        const ib = knownOrder.indexOf(b);
        if (ia === -1 && ib === -1) return a.localeCompare(b);
        if (ia === -1) return 1;
        if (ib === -1) return -1;
        return ia - ib;
      });
      orderedSignals.forEach(v => signalSel.add(new Option(v, v)));

      // Apply URL params to selects (deep link)
      regionSel.value = getParam("region");
      techSel.value = getParam("technology");
      signalSel.value = getParam("signal");
      const w = getParam("window");
      if (w) windowSel.value = w;

      // Initial data load
      loadData();
    });

  // --- Fetch and draw data
  function loadData() {
    const region = regionSel.value;
    const technology = techSel.value;
    const signal = signalSel.value;
    const windowVal = windowSel.value;

    const qs = new URLSearchParams();
    if (region) qs.set("region", region);
    if (technology) qs.set("technology", technology);
    if (signal) qs.set("signal", signal);
    if (windowVal) qs.set("window", windowVal);

    fetch(`/dashboard/api/map-data/?${qs.toString()}`)
      .then(r => r.json())
      .then(geo => {
        markers.clearLayers();

        const features = geo.features || [];
        const bounds = [];

        features.forEach(f => {
          const p = f.properties || {};
          const [lon, lat] = f.geometry.coordinates;

          const color = colorBySignal(p.signal);
          const icon = makeIcon(color);

          const popup = `
            <div style="min-width:210px">
              <div style="font-weight:600;margin-bottom:4px">${p.name || "Tower"}</div>
              <div><strong>Region:</strong> ${p.region || "-"}</div>
              <div><strong>Tech:</strong> ${p.technology || "-"}</div>
              <div><strong>Signal:</strong> <span style="color:${color}">${p.signal || "-"}</span></div>
              <div><strong>Latency:</strong> ${p.latency ?? "-"} ms</div>
              <div><strong>Download:</strong> ${p.download ?? "-"} Mbps</div>
              <div style="margin-top:6px">
                <a href="/dashboard/tower/${p.tower_id}/">View details →</a>
              </div>
            </div>`;

          const marker = L.marker([lat, lon], { icon }).bindPopup(popup);
          markers.addLayer(marker);
          bounds.push([lat, lon]);
        });

        if (bounds.length) {
          const b = L.latLngBounds(bounds);
          map.fitBounds(b, { padding: [40, 40] });
        }
      });

    // update deep-link
    setParams({ region, technology, signal, window: windowVal });
  }

  // --- Events
  applyBtn.addEventListener("click", () => loadData());
  resetBtn.addEventListener("click", () => {
    regionSel.value = "";
    techSel.value = "";
    signalSel.value = "";
    windowSel.value = "";
    loadData();
  });
});
