// looks for a #venue-map div with a data-markers attribute (json array of
// {lat, lng, title, href}), draws pins for each one, does nothing if the
// page has no map or Leaflet failed to load off the CDN
function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value == null ? "" : value;
  return div.innerHTML;
}

document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("venue-map");
  if (!el || typeof L === "undefined") {
    return;
  }

  const markers = JSON.parse(el.dataset.markers || "[]");
  if (!markers.length) {
    return;
  }

  const gmapsLabel = el.dataset.gmapsLabel || "Google Maps";
  const amapsLabel = el.dataset.amapsLabel || "Apple Maps";

  const map = L.map(el).setView([markers[0].lat, markers[0].lng], markers.length > 1 ? 12 : 14);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 19,
  }).addTo(map);

  const bounds = [];
  markers.forEach((marker) => {
    const pin = L.marker([marker.lat, marker.lng]).addTo(map);

    const titleHtml = marker.title
      ? (marker.href ? `<a href="${marker.href}">${escapeHtml(marker.title)}</a>` : escapeHtml(marker.title))
      : "";
    const gmapsUrl = `https://www.google.com/maps/search/?api=1&query=${marker.lat},${marker.lng}`;
    const amapsUrl = `https://maps.apple.com/?ll=${marker.lat},${marker.lng}&q=${encodeURIComponent(marker.title || "")}`;

    pin.bindPopup(`
      <div class="map-popup">
        ${titleHtml ? `<div class="map-popup__title">${titleHtml}</div>` : ""}
        <div class="map-popup__links">
          <a href="${gmapsUrl}" target="_blank" rel="noopener">${escapeHtml(gmapsLabel)}</a>
          <a href="${amapsUrl}" target="_blank" rel="noopener">${escapeHtml(amapsLabel)}</a>
        </div>
      </div>
    `);

    bounds.push([marker.lat, marker.lng]);
  });

  if (bounds.length > 1) {
    map.fitBounds(bounds, { padding: [24, 24] });
  }
});
