//input
const tableBody = document.querySelector('#input tbody'); 
var input_database = [];
var j = 0;
function inputTable(data) {
    input_database[j] = data; // Store the current data
    j++; // Increment the counter

    // Clear existing rows in the table body
    if (j > 5)
    {
        tableBody.innerHTML = '';
        input_database = [];
        return;
    }

    // Get all unique dates from the stored data
    const allDates = [];
    input_database.forEach(entry => {
        allDates.push(...Object.keys(entry)); // Add all dates to the array
    });
    
    // Get unique dates and limit to 5
    const uniqueDates = [...new Set(allDates)];
    // Limit to 5 unique dates

    // Create a header row for the dates
    const headerRow = document.createElement('tr');
    uniqueDates.forEach(date => {
        const cellDay = document.createElement('th');
        cellDay.textContent = moment(date).format('MMMM DD YYYY');
        headerRow.appendChild(cellDay);
    });
    tableBody.appendChild(headerRow); // Append the header row

    const dataTypes = ['tempmin', 'tempmean', 'tempmax', 'vpdmin', 'vpdmax'];
    
    // Create rows for each data type
    dataTypes.forEach(dataType => {
        const dataRow = document.createElement('tr');

        uniqueDates.forEach(date => {
            const cellData = document.createElement('td'); // Use <td> for data cells
            // Find the relevant data for the date
            const relevantData = input_database.find(entry => entry[date]); // Get the data for the specific date
            cellData.textContent = relevantData ? relevantData[date][dataType] : ''; // Safely access the data
            dataRow.appendChild(cellData); // Append the cell to the data row
        });

        tableBody.appendChild(dataRow); // Append the data row to the tbody
    });
}


//output
var output_database = [];
var k = 0;
const prog_tableBody = document.querySelector('#prog tbody'); 
function progTable(data){
    output_database[k] = data; // Store the current data
    k++; // Increment the counter

    // Clear existing rows in the table body
    if (k > 5)
    {
        prog_tableBody.innerHTML = '';
        output_database = [];
        return;    
    }   

    // Get all unique dates from the stored data
    const allDates = [];
    output_database.forEach(entry => {
        allDates.push(...Object.keys(entry)); // Add all dates to the array
    });
    
    // Get unique dates and limit to 5
    const uniqueDates = [...new Set(allDates)];
    // Limit to 5 unique dates

    // Create a header row for the dates
    const headerRow = document.createElement('tr');
    uniqueDates.forEach(date => {
        const cellDay = document.createElement('th');
        cellDay.textContent = moment(date).format('MMMM DD YYYY');
        headerRow.appendChild(cellDay);
    });
    prog_tableBody.appendChild(headerRow); // Append the header row

    const dataTypes = ['tempmin', 'tempmean', 'tempmax', 'vpdmin', 'vpdmax'];
    
    // Create rows for each data type
    dataTypes.forEach(dataType => {
        const dataRow = document.createElement('tr');

        uniqueDates.forEach(date => {
            const cellData = document.createElement('td'); // Use <td> for data cells
            // Find the relevant data for the date
            const relevantData = output_database.find(entry => entry[date]); // Get the data for the specific date
            cellData.textContent = relevantData ? relevantData[date][dataType] : ''; // Safely access the data
            dataRow.appendChild(cellData); // Append the cell to the data row
        });

        prog_tableBody.appendChild(dataRow); // Append the data row to the tbody
    });
}

/*var data = {'2021-03-17': {'Name': 'Homestead',
  'tempmin': 67.6,
  'tempmean': 75.1,
  'tempmax': 82.0,
  'tdmean': 61.8,
  'vpdmin': 3.61,
  'vpdmax': 17.09}}
inputTable(data);

data = {
 '2021-03-18': {'Name': 'Homestead',
  'tempmin': 69.6,
  'tempmean': 77.0,
  'tempmax': 83.7,
  'tdmean': 64.7,
  'vpdmin': 3.21,
  'vpdmax': 18.22}}

inputTable(data);
data = {
 '2021-03-19': {'Name': 'Homestead',
  'tempmin': 70.0,
  'tempmean': 77.8,
  'tempmax': 85.1,
  'tdmean': 65.2,
  'vpdmin': 2.1,
  'vpdmax': 18.56}
}
inputTable(data);*/