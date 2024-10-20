am5.ready(function() {
  // Get the country from URL if present
  const urlParams = new URLSearchParams(window.location.search);
  const countryParam = urlParams.get('country');

  var root = am5.Root.new("chartdiv");
  
  root.setThemes([
    am5themes_Animated.new(root),
    am5themes_Dark.new(root)
  ]);
  
  var chart = root.container.children.push(
    am5map.MapChart.new(root, {
      rotationX: 60,
      rotationY: -20,
      panX: "rotateX",
      panY: "rotateY",
      wheelY: "rotateY",
      wheelX: "rotateX",
      wheelSensitivity: 8.0,
      projection: am5map.geoOrthographic()
  }));
  
  var polygonSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
    geoJSON: window.am5geodata_worldLow,
    exclude: ["AQ"]
  }));
  
  polygonSeries.mapPolygons.template.setAll({
    tooltipText: "{name}",
    fill: am5.color(0xb92637),
    toggleKey: "active",
    interactive: true
  });
  
  polygonSeries.mapPolygons.template.states.create("hover", {
    fill: am5.color(0xd44b06)
  });
  
  polygonSeries.mapPolygons.template.states.create("active", {
    fill: am5.color(0xFF8C42)
  });
  
  var backgroundSeries = chart.series.unshift(
    am5map.MapPolygonSeries.new(root, {})
  );
  
  backgroundSeries.mapPolygons.template.setAll({
    fill: am5.color(0xd4f1f9),
    stroke: am5.color(0xd4f1f9),
  });
  
  backgroundSeries.data.push({
    geometry: am5map.getGeoRectangle(90, 180, -90, -180)
  }); 
  
  var previousPolygon;
  var countryName; 

  function updateCountryInfo(countryName) {
      fetch(`../../frontend/countries.php?country=${encodeURIComponent(countryName)}`, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json'
          }
      })
      .then(response => response.json())
      .then(data => {
          document.getElementById('country-placeholder').textContent = data.Country;
          document.getElementById('capital-placeholder').textContent = data.Capital;
          document.getElementById('population-placeholder').textContent = data.Population;
          document.getElementById('region-placeholder').textContent = data.Region;
          document.getElementById('currency-placeholder').textContent = data.Currency;
      })
      .catch((error) => {
          console.error('Error:', error);
      });
  }

  polygonSeries.mapPolygons.template.on("active", function (active, target) {
      if (previousPolygon && previousPolygon != target) {
          previousPolygon.set("active", false);
      }
      if (target.get("active")) {
          countryName = target.dataItem.dataContext.name;
          
          // Update the URL with the selected country
          const url = new URL(window.location);
          url.searchParams.set('country', encodeURIComponent(countryName));
          window.history.pushState({}, '', url);

          updateCountryInfo(countryName);
          polygonSeries.zoomToDataItem(target.dataItem);
      }
      previousPolygon = target;
  });
  
  // Add zoom control
  var zoomControl = chart.set("zoomControl", am5map.ZoomControl.new(root, {}));
  
  // Set clicking on "water" to zoom out
  chart.chartContainer.get("background").events.on("click", function () {
    //chart.goHome();
  })
  
  chart.appear(1000, 100);

  // Handle country from URL parameter
  if (countryParam) {
      polygonSeries.mapPolygons.each(function(polygon) {
          if (polygon.dataItem.dataContext.name === decodeURIComponent(countryParam)) {
              polygon.setState("active", true);
              polygonSeries.zoomToDataItem(polygon.dataItem);
              updateCountryInfo(decodeURIComponent(countryParam));
          }
      });
  }
});