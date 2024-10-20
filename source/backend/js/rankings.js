async function fetchCSV() {
    try {
        const response = await fetch('../backend/carbon_emmisions.csv');
        const data = await response.text();
        const json = csvToJson(data);
        Table(json);
    } catch (error) {
        console.error('Error fetching the CSV file:', error);
    }
}
// Select the tbody element of the table
const tableBody = document.querySelector('#dataTable tbody'); 
function csvToJson(csv) {
    const lines = csv.split('\n');
    const result = [];

    for (let i = 1; i < lines.length; i++) {
        const obj = {};
        const currentLine = lines[i].split(',');
        //console.log(currentLine);
        result[i] = currentLine;
    }
    //console.log(result[20][0])
    return result;
}

function Table(data){
// Use a for loop to generate table rows
for (let i = 1; i < 52; i++) {
    // with open($path, 'r') as f
    //data[i]['coy']
    //console.log(data)
    const row = document.createElement('tr');
    
    
    const cellNumber = document.createElement('th');
    cellNumber.textContent = i;

    const cellName = document.createElement('td');
    cellName.textContent = `${data[i][0]}`; // Item name

    const cellEmmision = document.createElement('td');
    const formattedNumber = new Intl.NumberFormat('en-US').format(Math.floor(data[i][1]*1000));
    cellEmmision.textContent = `${formattedNumber}`; // Item name

    const cellPopulation = document.createElement('td');

    const formattedPop = new Intl.NumberFormat('en-US').format(Math.floor(data[i][2]*100000));
    cellPopulation.textContent = `${formattedPop}`;

    const cellAverage = document.createElement('td');
    const num = (data[i][1]*1000)/(data[i][2]*100000);
    let num_cap = num.toFixed(7);
    cellAverage.textContent = `${num_cap}`; // Item name


    // Append cells to the row
    row.appendChild(cellNumber);
    row.appendChild(cellName);
    row.appendChild(cellEmmision);
    row.appendChild(cellPopulation);
    row.appendChild(cellAverage);



    // Append the row to the tbody
    tableBody.appendChild(row);
}
}
fetchCSV()