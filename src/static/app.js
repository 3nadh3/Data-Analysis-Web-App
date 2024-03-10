// app.js

function uploadDataset() {
    var form = document.getElementById('uploadForm');
    var formData = new FormData(form);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            displayError(result.error);
        } else {
            displayResult(result);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayError('An unexpected error occurred.');
    });
}

function displayResult(result) {
    var resultContainer = document.getElementById('resultContainer');
    resultContainer.innerHTML = '<h2>Analysis Result</h2>';
    
    // Create a table and append it to the resultContainer
    var table = document.createElement('table');
    resultContainer.appendChild(table);

    // Create table header
    var thead = table.createTHead();
    var headerRow = thead.insertRow();
    for (var key in result.data[0]) {
        var th = document.createElement('th');
        th.appendChild(document.createTextNode(key));
        headerRow.appendChild(th);
    }

    // Create table body
    var tbody = table.createTBody();
    result.data.forEach(function (rowData) {
        var row = tbody.insertRow();
        for (var key in rowData) {
            var cell = row.insertCell();
            cell.appendChild(document.createTextNode(rowData[key]));
        }
    });
}

function displayError(errorMessage) {
    var resultContainer = document.getElementById('resultContainer');
    resultContainer.innerHTML = '<h2>Error</h2><p>' + errorMessage + '</p>';
}
