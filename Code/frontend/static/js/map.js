// looks for a #venue-map div with a data-markers attribute (json array of
// {lat, lng, title, href}), draws pins for each one, does nothing if the
// page has no map or Leaflet failed to load off the CDN
document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("venue-map");
  if (!el || typeof L === "undefined") {
    return;
  }

  const markers = JSON.parse(el.dataset.markers || "[]");
  if (!markers.length) {
    return;
  }

  const map = L.map(el).setView([markers[0].lat, markers[0].lng], markers.length > 1 ? 12 : 14);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 19,
  }).addTo(map);

  const bounds = [];
  markers.forEach((marker) => {
    const pin = L.marker([marker.lat, marker.lng]).addTo(map);
    if (marker.title) {
      const label = marker.href ? `<a href="${marker.href}">${marker.title}</a>` : marker.title;
      pin.bindPopup(label);
    }
    bounds.push([marker.lat, marker.lng]);
  });

  if (bounds.length > 1) {
    map.fitBounds(bounds, { padding: [24, 24] });
  }
});
