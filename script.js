const map = L.map('stateMap').setView([37.8000, -79.3000], 8);
const homeButton = L.control({ position: 'topleft' });
const coordsDisplay = L.control({ position: 'topright' });

fetch('onlyVAcounties.json')
  .then(response => response.json())
  .then(data => {
    L.geoJSON(data, {
      style: {
        color: 'black',
        weight: 1.5,
        fillColor: 'lightblue',
        fillOpacity: 0.5
      }
    }).addTo(map);
  })
  .catch(error => console.error('Ruh ro raggy:', error));



homeButton.onAdd = function(map) {
  const button = L.DomUtil.create('button', 'home-button');
  button.innerHTML = 'Reset view';
  button.onclick = function() {
    map.setView([37.8000, -79.2000], 8);
  };
  return button;
};

coordsDisplay.onAdd = function(map) {
  const div = L.DomUtil.create('div', 'coords-display');
  div.innerHTML = 'Coords: ';
  map.on('mousemove', function(e) {
    div.innerHTML = `Coords: ${e.latlng.lat.toFixed(4)}, ${e.latlng.lng.toFixed(4)}`;
  });
  return div;
};

homeButton.addTo(map);
coordsDisplay.addTo(map);

let activeMarkers = [];

function loadMarkers() {
  fetch('markers.json')
    .then(response => response.json())
    .then(data => {
      
      activeMarkers.forEach(marker => map.removeLayer(marker));
      activeMarkers = [];

      data.forEach(({ latitude, longitude, count, reasons }) => {
        const marker = L.marker([latitude, longitude]).addTo(map);
        activeMarkers.push(marker);

        const countLabel = L.divIcon({
          className: 'marker-label',
          html: `<div class="count-label">${count}</div>`,
          iconSize: [0, 0], 
          iconAnchor: [2, -10] 
        });

        const labelMarker = L.marker([latitude, longitude], { icon: countLabel }).addTo(map);
        activeMarkers.push(labelMarker);
        marker.bindPopup(`Accidents: ${count}<br>Reasons: ${reasons.join(", ")}`);
      });
    })
    .catch(error => console.error('Error:', error));
}


loadMarkers();
map.setMinZoom(7);
