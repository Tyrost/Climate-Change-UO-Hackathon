<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Countries Page</title>

  <!--Credit--> 
  <!--https://www.amcharts.com/demos/zooming-to-countries-map/-->

  <link rel="stylesheet" href="./components/general.css">
  <link rel="stylesheet" href="./components/countries.css">

</head>
<body>


<!-- Resources -->
<script src="https://cdn.amcharts.com/lib/5/index.js"></script>
<script src="https://cdn.amcharts.com/lib/5/map.js"></script>
<script src="../backend/js/countrydata.js"></script>
<script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>
<script src="//cdn.amcharts.com/lib/5/themes/Dark.js"></script>

<!-- Chart code -->
<script>
am5.ready(function() {

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
polygonSeries.mapPolygons.template.on("active", function (active, target) {
    if (previousPolygon && previousPolygon != target) {
        previousPolygon.set("active", false);
    }
    if (target.get("active")) {
        countryName = target.dataItem.dataContext.name;
        
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ country: countryName })
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

}); 
</script>

<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (isset($input['country'])) {
        $country_name = $input['country'];
        $command = escapeshellcmd("python3 ../backend/Python/country_data.py " . escapeshellarg($country_name));
        $output = shell_exec($command);
        $data = json_decode($output, true);

        header('Content-Type: application/json');
        echo json_encode($data);
        exit;
    }
}

$country = '-----';
$capital = '-----';
$population = '-----';
$region = '-----';
$currency = '-----';
?>

<div class="menu-bar">
  <div class="button-container">
      <button class="home-button" onclick="location.href='../index.php'">Home</button>
      <button class="countries-button" onclick="location.href='./countries.php'">Countries</button>
      <button class="rankings-button" onclick="location.href='./rankings.html'">Rankings</button>
      <button class="prognostication-button" onclick="location.href='./prognostication.php'">Prognostication</button>
      <button class="newsletter-button" onclick="location.href='./newsletter.html'">Newsletter</button>
  </div>
</div>

<div id="wrapper">
    <div id="chartdiv"></div>
</div>

<div class="data-container">
    <table>
        <tr>
            <td>Country:</td>
            <td><h4 id='country-placeholder'><?php echo $country; ?></h4></td>
        </tr>
        <tr>
            <td>Capital:</td>
            <td><h4 id='capital-placeholder'><?php echo $capital; ?></h4></td>
        </tr>
        <tr>
            <td>Population:</td>
            <td><h4 id='population-placeholder'><?php echo $population; ?></h4></td>
        </tr>
        <tr>
            <td>Region:</td>
            <td><h4 id='region-placeholder'><?php echo $region; ?></h4></td>
        </tr>
        <tr>
            <td>Currency:</td>
            <td><h4 id='currency-placeholder'><?php echo $currency; ?></h4></td>
        </tr>
    </table>
</div>

<!-- <div class="large-sqr" style="color: white;height:5vh; z-index:100;"></div> -->

<div class="bottom-panel-section" style="justify-content: center; justify-content: center; padding-top:50vh;">
      <div class="panel-content">
        <p>
          The World is a big place. Which is why we are committed on providing you <br>
          with the best possible model of information from around the globe. Explore the<br> 
          various perspectives, details and colors of the world with out 3D model.<br>
        </p>
        <h3 style="color:darksalmon; font-family:Arial, Helvetica, sans-serif;">History Lesson</h3>
        <p style="font-size: 15px; color:darksalmon;">
        The Earth is an ancient traveler, wandering through the vastness of space for<br>
        4.5 billion years, quietly spinning on its tilted axis and dancing around the<br>
        Sun. Along the way, it nurtured life from the simplest single-celled organisms<br>
        into vibrant ecosystems teeming with diversity. Through ice ages and fiery<br>
        volcanic eruptions, Earth adapted, evolving into the delicate, life-supporting<br>
        sphere we now call home.<br>
        <br>
        But today, this old traveler is facing a challenge unlike any it has seen<br>
        before—climate change. Like a caretaker burdened with too much, Earth's systems<br>
        are starting to falter under the weight of carbon emissions, deforestation, and<br>
        pollution. The oceans warm, glaciers melt, and the air thickens with invisible<br>
        threats.<br>
        <br>
        Yet, we still have a chance to be part of the story where we become its<br>
        protectors, reducing harm and restoring balance. This isn't just about<br>
        preserving landscapes or saving wildlife—it's about securing a future where<br>
        Earth can continue its journey, carrying life safely through the stars.<br>
        <br>
        If we listen to its silent call and act with care, we ensure that Earth, with<br>
        all its beauty and fragility, can keep nurturing us for generations to come.<br>
        </p>
      
      <div class="earth-img-container">
        <img class="earth-image" src="./components/images/red-earth.jpg" style="width: 30%; height:55%; position:absolute; bottom:180px; right:100px;">
      </div>

      </div>
</div>


<!-- -------------------------------------------------------------------------------------- -->
<script>

let lastScrollTop = 0;

window.addEventListener('scroll', function() {
  const panelSection = document.querySelector('.bottom-panel-section');
  const scrollPosition = window.pageYOffset || document.documentElement.scrollTop;

  if (scrollPosition > 10 && scrollPosition > lastScrollTop) {
    panelSection.classList.add('active');
  }
 
  else if (scrollPosition < 10) {
    panelSection.classList.remove('active');
  }

  lastScrollTop = scrollPosition;
});

</script>

</body>
</html>