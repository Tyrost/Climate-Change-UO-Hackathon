<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UO Hackathon</title>

    <!-- <link rel="stylesheet" href="/source/frontend/components/index.css"> -->
    <link rel="stylesheet" href="./frontend/components/general.css">
    <link rel="stylesheet" href="./frontend/components/index.css">

</head>
<body>
    
    <div class="main-background-container"></div>

    <div class="menu-bar">
            <div class="button-container">
                <button class="home-button" onclick="location.href='./index.php'">Home</button>
                <button class="countries-button" onclick="location.href='./frontend/countries.php'">Countries</button>
                <button class="rankings-button" onclick="location.href='./frontend/rankings.html'">Rankings</button>
                <button class="Prognostication-button" onclick="location.href='./frontend/prognostication.php'">Prognostication</button>
                <button class="newsletter-button" onclick="location.href='./frontend/newsletter.html'">Newsletter</button>
            </div>
    </div>

    <div class="main-title-container">
        <h2 class="main-name" id="main-big-letters">Fire Starter</h2>
        <h4 class="main-name" id="main-smaller-letters">The Future of our World</h4>
        <h5 class="main-name" id="main-description-letters">Explore the world around us. Help us protect mother earth and its environment.</h5>
    </div>

    <img class="main-image" src="./frontend/components/images/wildfire-image.jpg">
    </div>
    <div style="width: 10px; height:200vh; color:white; position:absolute;"></div>

    <div class="lower-image-container" id="lowerImageContainer">
        <div class="panel-content">
            <h2 style='font-size: 25px; font-family: Roobert, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;'>Climate Impact</h2>
            <p style='line-height: 1.6; font-family: Roobert, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;top:40vh;'>
                Learn how our environment is changing. Stay informed about the impact of global warming
                on ecosystems and communities around the world.
            </p>
        </div>
    </div>

    <div class="info-container">
        <h2 class="info-title" style='color: white; text-align:center; top:5vh; font-size:50px; font-family: Roobert, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;'>Climate Change</h2>
        <h2 class="info-title" style='color: white; text-align:center; font-size:18px; font-family: Roobert, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;'>The recurrent issue of the century</h2>
        <div class="info-description-container">
        <p style='line-height: 1.6; font-family: Roobert, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;; position: absolute; color:white; text-align: center; top:40vh; left: 30%;'>
                Wildfires affect:<br>
                    - Federal and State Budgets.<br>
                    - Public Health.<br>
                    - Natural environment.<br>
                    <br>
                    Increased emissions were linked to a rise in fire-favorable weather,<br>
                    such as the hot, dry conditions seen during heat waves and droughts,<br>
                    as well as increased rates of forest growth,<br>
                    creating more vegetation fuels.<br>
                    Both trends are aided by rapid warming in the high northern latitudes,<br>
                    where it is happening twice as fast as the global average.<br>
                    Boreal forests in Eurasia and North America,<br>
                    saw emissions from fires nearly triple between 2001 and 2023.<br>

            </p>
        </div>

    </div>

    <div class="side-shape" id="shape-one"></div>
    <div class="side-shape" id="shape-two"></div>

<script>

let lastScrollTop = 0;

window.addEventListener('scroll', function() {
  const panelSection = document.querySelector('.lower-image-container');
  const scrollPosition = window.pageYOffset || document.documentElement.scrollTop;

  if (scrollPosition > 100 && scrollPosition > lastScrollTop) {
    panelSection.classList.add('active');
  }
 
  else if (scrollPosition < 1000) {
    panelSection.classList.remove('active');
  }

  lastScrollTop = scrollPosition;
});

</script>

</body>
</html>