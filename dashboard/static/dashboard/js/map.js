document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ map.js loaded");

  const map = L.map("map").setView([21.4735, 55.9754], 6);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© OpenStreetMap contributors"
  }).addTo(map);

  const markers = L.markerClusterGroup();
  map.addLayer(markers);

  // Legend
  const legendEl = document.getElementById("legend");
  const LegendControl = L.Control.extend({
    options: { position: "bottomleft" },
    onAdd: function () {
      const div = L.DomUtil.create("div", "legend");
      div.innerHTML = legendEl.innerHTML;
      div.style.background = "#fff";
      div.style.padding = "10px";
      div.style.borderRadius = "8px";
      div.style.boxShadow = "0 0 8px #0002";
      return div;
    }
  });
  map.addControl(new LegendControl());

  const regionSel = document.getElementById("regionFilter");
  const techSel = document.getElementById("techFilter");
  const signalSel = document.getElementById("signalFilter");
  const windowSel = document.getElementById("windowFilter");
  const applyBtn = document.getElementById("applyFilter");
  const resetBtn = document.getElementById("resetFilter");

  function makeIcon(color) {
    return L.divIcon({
      className: "marker-dot",
      html: `<div style="width:14px;height:14px;border-radius:50%;background:${color};
              border:2px solid #fff;box-shadow:0 0 4px #0004;"></div>`,
      iconSize: [14, 14],
      iconAnchor: [7, 7],
    });
  }

  fetch(`/dashboard/api/map-filters/`)
    .then(r => r.json())
    .then(({ regions, technologies, signals, windows }) => {
      regions.forEach(v => regionSel.add(new Option(v, v)));
      technologies.forEach(v => techSel.add(new Option(v, v)));
      signals.forEach(v => signalSel.add(new Option(v, v)));
      windows.forEach(v => windowSel.add(new Option(v, v)));
      loadData();
    });

  function loadData() {
    const qs = new URLSearchParams();
    if (regionSel.value) qs.set("region", regionSel.value);
    if (techSel.value) qs.set("technology", techSel.value);
    if (signalSel.value) qs.set("signal", signalSel.value);

    fetch(`/dashboard/api/map-data/?${qs.toString()}`)
      .then(r => r.json())
      .then(geo => {
        markers.clearLayers();
        const bounds = [];
        (geo.features || []).forEach(f => {
          const p = f.properties, [lon, lat] = f.geometry.coordinates;
          const popup = `
            <div style="min-width:210px">
              <div style="font-weight:600;margin-bottom:4px">${p.name || "Tower"}</div>
              <div><strong>Region:</strong> ${p.region || "-"}</div>
              <div><strong>Tech:</strong> ${p.technology || "-"}</div>
              <div><strong>Signal:</strong> ${p.signal || "-"}</div>
              <div><strong>Latency:</strong> ${p.latency ?? "-"} ms</div>
              <div><strong>Download:</strong> ${p.download ?? "-"} Mbps</div>
              <div style="margin-top:6px"><a href="/dashboard/tower/${p.pk}/">View details →</a></div>
            </div>`;
          const marker =
