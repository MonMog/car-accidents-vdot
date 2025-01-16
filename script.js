const map = L.map('stateMap').setView([37.8000, -79.3000], 7);
const permaMap = L.map('permaMap').setView([37.8000, -79.3000], 7);


function loadCounties(map) {
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
}

loadCounties(map);
loadCounties(permaMap);





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

function loadPermaMarkers() {
  fetch('permaMarkers.json')
    .then(response => response.json())
    .then(data => {
      data.forEach(({ latitude, longitude, count, reasons }) => {
        const marker = L.marker([latitude, longitude]).addTo(permaMap);

        const countLabel = L.divIcon({
          className: 'marker-label',
          html: `<div class="count-label">${count}</div>`,
          iconSize: [0, 0],
          iconAnchor: [2, -10]
        });

        const labelMarker = L.marker([latitude, longitude], { icon: countLabel }).addTo(permaMap);
        marker.bindPopup(`Accidents: ${count}<br>Reasons: ${reasons.join(", ")}`);
      });
    })
    .catch(error => console.error('Error:', error));
}

loadMarkers();
loadPermaMarkers();


map.setMinZoom(7);
permaMap.setMinZoom(7);
