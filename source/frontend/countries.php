<!--Credit--> 
<!--https://www.amcharts.com/demos/zooming-to-countries-map/-->

<link rel="stylesheet" href="./components/general.css">
<link rel="stylesheet" href="./components/countries.css">

<!-- Resources -->
<script src="https://cdn.amcharts.com/lib/5/index.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/map.js"></script>
    <!--script src="https://cdn.amcharts.com/lib/5/geodata/worldLow.js"</script-->
    <script src="../backend/js/countrydata.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>
    <script src="//cdn.amcharts.com/lib/5/themes/Dark.js"></script>
    
    <!-- Chart code -->
    <script>
    am5.ready(function() {
    
    // Create root element
    // https://www.amcharts.com/docs/v5/getting-started/#Root_element
    var root = am5.Root.new("chartdiv");
    
    
    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    root.setThemes([
      am5themes_Animated.new(root),
      am5themes_Dark.new(root)
    ]);
    
    
    // Create the map chart
    // https://www.amcharts.com/docs/v5/charts/map-chart/
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
    
    //chart.chartContainer.set("background", am5.Rectangle.new(root, {
    //  fill: am5.color(0xebebeb),
    //  stroke: am5.color(0xd4f1f9),
    //  fillOpacity: 1
    //}));
    // Create main polygon series for countries
    // https://www.amcharts.com/docs/v5/charts/map-chart/map-polygon-series/
    var polygonSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
      //Add any extra information here 
      geoJSON: window.am5geodata_worldLow, //figure put how to put JS file worldLow.js data here
      exclude: ["AQ"]

    }));
    polygonSeries.mapPolygons.template.setAll({
      //information with go next to tooltipText
      tooltipText: "{name}",
      fill: am5.color(0xb92637),
      toggleKey: "active",
      interactive: true
    }
    );
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
polygonSeries.mapPolygons.template.on("active", function (active, target) {
    if (previousPolygon && previousPolygon != target) {
        previousPolygon.set("active", false);
      }
      if (target.get("active")) {
        countryName = target.dataItem.dataContext.name; // Access the name directly
        
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ country: countryName })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Optional: Log the response from PHP
        })
        .catch((error) => {
            console.error('Error:', error);
        });

        polygonSeries.zoomToDataItem(target.dataItem);
        //console.log("Clicked on", target.get("tooltipText"));
      }
      else {
        //chart.goHome();
      }
      previousPolygon = target;
    });

//polygonSeries.mapPolygons.template.events.on("click", function(ev) {
 // console.log("Clicked on", ev.target.dataItem.get("name"));
//});
    
    
    // Add zoom control
    // https://www.amcharts.com/docs/v5/charts/map-chart/map-pan-zoom/#Zoom_control
    var zoomControl = chart.set("zoomControl", am5map.ZoomControl.new(root, {}));
    //zoomControl.homeButton.set("visible", True);
    
    // Set clicking on "water" to zoom out
    chart.chartContainer.get("background").events.on("click", function () {
      //chart.goHome();
    })
    
    
    // Make stuff animate on load
    chart.appear(1000, 100);
    
    }); // end am5.ready()
</script>

<?php

if (isset($_POST['country'])) {

  $country_name = $_POST['country'];
  $command = escapeshellcmd("python3 ../backend/Python/country_data.py" . escapeshellarg($country_name));
  $output = shell_exec($command);
  $data = json_decode($data, true);

  $country = $data['Country'];
  $capital = $data['Capital'];
  $population = $data['Population'];
  $region = $data['Region'];
  $currency = $data['Currency'];

} else {

  $country = '-----';
  $capital = '-----';
  $population = '-----';
  $region = '-----';
  $currency = '-----';

}

?>


<div id="wrapper">
    <div id="chartdiv"></div>
</div>

<div class="data-container">
  <?php
    if (!isset($_POST['country'])) {
      echo '
      <table>
        <tr>
            <td>Country:</td>
            <td><h4 id="country-placeholder">---</h4></td>
        </tr>
        <tr>
            <td>Capital:</td>
            <td><h4 id="capital-placeholder">---</h4></td>
        </tr>
        <tr>
            <td>Population:</td>
            <td><h4 id="population-placeholder">---</h4></td>
        </tr>
        <tr>
            <td>Region:</td>
            <td><h4 id="region-placeholder">---</h4></td>
        </tr>
        <tr>
            <td>Currency:</td>
            <td><h4 id="currency-placeholder">---</h4></td>
        </tr>
      </table>
      '; 
    } else {
      


    }
  ?>
    
</div>

