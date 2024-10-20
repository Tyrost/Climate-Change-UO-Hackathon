<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action= "" method="post" id="form-id">
        <label for="lat">Latitude:</label><br>
        <input type="number" id="lat" name="lat"><br>
        <label for="long">Longtitude:</label><br>
        <input type="number" id="long" name="long">

        <label for="start">Start Date</label><br>
        <input type="date" id="start" name="start"><br>
        <label for="lat">End Date</label><br>
        <input type="date" id="end" name="end">

        <label for="services">Choose:</label>
        <select id="services" name="services">
            <option value="" disabled selected>Span</option>
            <option value="day">Day</option>
            <option value="month">Month</option>
            <option value="year">Year</option>
        </select>
        <input type="submit" value="Submit">
      </form>
</body>
</html>