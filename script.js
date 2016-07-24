var map;
var allNeighborhoods;
var neighborhoodLayer;

// Execute on page load
(function(){
  map = L.map('map');
  var osmUrl='http://{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png';
  var osmAttrib='Credit: <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a>, <a href="http://www.thunderforest.com/transport/">Andy Allan</a>';
  var osm = new L.TileLayer(osmUrl, {minZoom: 10, maxZoom: 18, attribution: osmAttrib});
  map.addLayer(osm);
  map.setView([41.907477, -87.685913], 10);

  var legend = L.control({position: 'bottomleft'});
  legend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML += "<b>Neighborhood:</b> <span id='neighbName'>Select a Neighborhood</span><br>" +
                  "<b>Overlap:</b> <span id='overlapPct'>%</span><br>" +
                  "<b>Responses:</b> <span id='respCount'></span><br>" +
                  "<small>Source: <a href='https://www.dnainfo.com/chicago/20150928/loop/this-is-where-chicagoans-say-borders-of-their-neighborhoods-are'>DNAInfo</a></small>";
    return div;
  };
  legend.addTo(map);

  neighborhoodLayer = L.geoJson().addTo(map);

  var xhr = new XMLHttpRequest();
  xhr.addEventListener("load", loadNeighborhoodData);
  xhr.open("GET", siteBase + "/neighborhood_data.geojson");
  xhr.send();
})();

function displayNeighborhood(neighborhood) {
  map.removeLayer(neighborhoodLayer);
  neighborhoodLayer = L.geoJson(allNeighborhoods, {
    filter: function(feature, layer) {
      return feature.properties.neighb === neighborhood;
    },
    style: {
      "color": "#B0171F",
      "weight": 0,
      "opacity": 0.65
    }
  }).addTo(map);
  map.fitBounds(neighborhoodLayer.getBounds());

  var neighbLegend = document.getElementById("neighbName");
  var overlapLegend = document.getElementById("overlapPct");
  var countLegend = document.getElementById("respCount");

  for (var i = 0; i < neighbData.length; ++i) {
    if (neighbData[i].neighborhood === neighborhood) {
      neighbLegend.innerText = neighbData[i].clean_neighborhood;
      overlapLegend.innerText = (neighbData[i].overlap * 100).toFixed(2).toString() + "%";
      countLegend.innerText = neighbData[i].count;
      break;
    }
  }
}

function loadNeighborhoodData() {
  allNeighborhoods = JSON.parse(this.responseText);

  var tableRef = document.getElementsByTagName('tbody')[0];
  for (var n = 0; n < neighbData.length; ++n) {
    var newRow = tableRef.insertRow(tableRef.rows.length);
    var neighborhoodCell  = newRow.insertCell(0);
    var overlapCell = newRow.insertCell(1);
    var responseCell = newRow.insertCell(2);

    var neighbItem = neighbData[n];
    var neighborhoodText = document.createTextNode(neighbItem.clean_neighborhood);
    var overlapText = document.createTextNode((neighbItem.overlap * 100).toFixed(2).toString() + "%");
    var responseText = document.createTextNode(neighbItem.count);

    neighborhoodCell.appendChild(neighborhoodText);
    overlapCell.appendChild(overlapText);
    responseCell.appendChild(responseText);

    var tableRow = tableRef.rows[tableRef.rows.length - 1];
    tableRow.setAttribute("onclick", "displayNeighborhood('" + neighbItem.neighborhood + "')");
  }
}
