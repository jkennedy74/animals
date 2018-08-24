// Tree loss from 2000-2012
var lossUrl = "http://gis-treecover.wri.org/arcgis/rest/services/ForestCover_lossyear_density/ImageServer/";
// Tree gain from 2000-2012
var gainUrl = "http://ec2-50-18-182-188.us-west-1.compute.amazonaws.com:6080/arcgis/rest/services/ForestGain_2000_2012/ImageServer/"
// Tree coverage in 2000
var coverUrl = "http://ec2-50-18-182-188.us-west-1.compute.amazonaws.com:6080/arcgis/rest/services/TreeCover2000/ImageServer/"

// Topographic base layer
var base = L.esri.basemapLayer("Topographic");

// Tree loss overlay
var lossLayer = L.esri.imageMapLayer({
  url: lossUrl,
  opacity : 0.8,
});

// Tree gain overlay
var gainLayer = L.esri.imageMapLayer({
  url: gainUrl,
  opacity : 0.9,
});

// Tree coverage overlay
var coverLayer = L.esri.imageMapLayer({
  url: coverUrl,
  opacity : 0.5,
});

// Create map object and set default layers
var map = L.map("map-id", {
    center: [28.0339, 1.6596],
    zoom: 2,
    layers: [base, coverLayer]
  });

// base layer group
var baseLayers = {
    "Topographic": base,
    "Gray": L.esri.basemapLayer("Gray")
};

// overlay group
var overlays = {
  "Tree cover (2000)": coverLayer,
  "Tree Loss (00-12)": lossLayer,
  "Tree gain (00-12)": gainLayer  
};

// layer control for the map
L.control.layers(baseLayers, overlays).addTo(map);

// cirlces overlay for class density
function buildClassGeo(s_class) {

  var url = `/geojsonC/${s_class}`

  console.log("---- buildClassGeo initiated ----")

  // Use `d3.json` to fetch the metadata for a animal class
  d3.json(url).then(function(data) {
    console.log(`features: ${data.features.length}`)

     // Use d3 to select the panel with id of `#info`
     var meta_data = d3.select("#info");

     // Use `.html("") to clear any existing metadata
     meta_data.html("");

     meta_data.append("h6").text("Now Viewing...");
    //  meta_data.append("br")
     meta_data.append("h6").text(`Class: ${data.features[0].properties.s_class}`);
    
    // code for the leaflet timeline plugin

    // time interval
    var getInterval = function(animal) {
      return {
        start: animal.properties.date,
        end:   animal.properties.end
      };
    };
    
    // timeline slider
    var timelineControl = L.timelineSliderControl({
      steps: 100,
      formatOutput: function(date) {
        return moment(date * 1000).format('YYYY-MM-DD');
      }
    });

    // timeline markers
    var timeline = L.timeline(data, {
      getInterval: getInterval,
      pointToLayer: function(data, latlng){
        return L.circleMarker(latlng, {
          radius: 20,
          color: "black",
          weight: 1,
          fillColor: "blue",
          fillOpacity: 0.05
        })
      }
    });

    // add the timeline to the map
    timelineControl.addTo(map);
    timelineControl.addTimelines(timeline);
    timeline.addTo(map);

  });
}

// cirlces overlay for species density
function buildSpeciesGeo(species) {

  var url = `/geojsonS/${species}`

  console.log("---- buildSpeciesGeo initiated ----")

  // Use `d3.json` to fetch the metadata for a animal species
  d3.json(url).then(function(data) {
    console.log(`features: ${data.features.length}`)

     // Use d3 to select the panel with id of `#info`
     var meta_data = d3.select("#info");

     // Use `.html("") to clear any existing metadata
     meta_data.html("");

     meta_data.append("h6").text("Now Viewing...");
    //  meta_data.append("br")
     meta_data.append("h6").text(`Species: ${data.features[0].properties.species}`);
     meta_data.append("h6").text(`Scientific Name: ${data.features[0].properties.scientific_name}`);
     meta_data.append("h6").text(`Class: ${data.features[0].properties.s_class}`);
     meta_data.append("h6").text(`Taxonkey: ${data.features[0].properties.taxonkey}`);
    
    // code for the leaflet timeline plugin
    
    // time interval
    var getInterval = function(animal) {
      return {
        start: animal.properties.date,
        end:   animal.properties.end
      };
    };
    
    // timeline slider
    var timelineControl = L.timelineSliderControl({
      steps: 100,
      formatOutput: function(date) {
        return moment(date * 1000).format('YYYY-MM-DD');
      }
    });

    // timeline markers
    var timeline = L.timeline(data, {
      getInterval: getInterval,
      pointToLayer: function(data, latlng){
        return L.circleMarker(latlng, {
          radius: 20,
          color: "black",
          weight: 1,
          fillColor: "blue",
          fillOpacity: 0.05
        })
      }
    });

    // add the timeline to the map
    timelineControl.addTo(map);
    timelineControl.addTimelines(timeline);
    timeline.addTo(map);

  });
}

function init() {
  // Grab a reference to the dropdown select element
  var classSelector = d3.select("#classSelect");
  var speciesSelector = d3.select("#speciesSelect");

  // Use the list of classes to populate the select options
  d3.json("/classes").then((response1) => {
    response1.forEach((item1) => {
      classSelector
        .append("option")
        .text(item1)
        .property("value", item1);
    });

    // Use the first class from the list to build the initial chart
    const firstClass = response1[0];
    buildClassGeo(firstClass);
  });
  // Use the list of species to populate the select options
  d3.json("/species").then((response2) => {
    response2.forEach((item2) => {
      speciesSelector
        .append("option")
        .text(item2)
        .property("value", item2);
    });
  });
}

function optionClassChanged(newClass) {
  // Fetch new data each time a new Class is selected
  d3.selectAll(".leaflet-interactive").remove();
  d3.select(".leaflet-bottom").html("");
  buildClassGeo(newClass);
}

function optionSpeciesChanged(newSpecies) {
  // Fetch new data each time a new Species is selected
  d3.selectAll(".leaflet-interactive").remove();
  d3.select(".leaflet-bottom").html("");
  buildSpeciesGeo(newSpecies);
}

// Initialize the dashboard
init();