// Global variables
let allData = [];
let columnInfo = {};
let currentPlot = null;

// Initialize the dashboard
$(document).ready(function() {
    // Load column information
    loadColumns();
    
    // Load data summary
    loadSummary();
    
    // Set up event handlers
    $('#update-plot').click(updatePlot);
    $('#plot-type').change(handlePlotTypeChange);
    
    // Load sample data
    loadData();
});

// Load column information from the API
function loadColumns() {
    $.getJSON('/api/columns', function(data) {
        columnInfo = data;
        
        // Populate dropdowns
        populateDropdown('#x-axis', [...data.numeric, ...data.categorical]);
        populateDropdown('#y-axis', data.numeric);
        populateDropdown('#color-by', [''].concat([...data.categorical]), true);
        
        // Set initial selection
        if (data.numeric.length > 0) {
            if (data.numeric.length > 1) {
                $('#x-axis').val(data.numeric[0]);
                $('#y-axis').val(data.numeric[1]);
            } else {
                $('#x-axis').val(data.index[0]);
                $('#y-axis').val(data.numeric[0]);
            }
        }
        
        // Create initial plot
        updatePlot();
    }).fail(function() {
        alert('Failed to load column information. Please check if the data file exists.');
    });
}

// Load data summary information
function loadSummary() {
    $.getJSON('/api/summary', function(data) {
        $('#data-summary').text(`Dataset: ${data.rows} rows, ${data.columns} columns`);
    });
}

// Load data for the table preview
function loadData() {
    $.getJSON('/api/data', function(data) {
        allData = data;
        
        // Display first 10 rows in the table
        const previewData = data.slice(0, 10);
        
        if (previewData.length > 0) {
            // Create table header
            const headerRow = $('#table-header');
            headerRow.empty();
            
            const columns = Object.keys(previewData[0]);
            columns.forEach(col => {
                headerRow.append(`<th>${col}</th>`);
            });
            
            // Create table body
            const tableBody = $('#table-body');
            tableBody.empty();
            
            previewData.forEach(row => {
                const tr = $('<tr>');
                columns.forEach(col => {
                    tr.append(`<td>${row[col]}</td>`);
                });
                tableBody.append(tr);
            });
        }
    });
}

// Populate a dropdown with options
function populateDropdown(selector, options, includeEmpty = false) {
    const dropdown = $(selector);
    dropdown.empty();
    
    if (includeEmpty) {
        dropdown.append($('<option>', {
            value: '',
            text: 'None'
        }));
    }
    
    options.forEach(option => {
        dropdown.append($('<option>', {
            value: option,
            text: option
        }));
    });
}

// Update the plot based on current selections
function updatePlot() {
    const plotType = $('#plot-type').val();
    const xAxis = $('#x-axis').val();
    const yAxis = $('#y-axis').val();
    const colorBy = $('#color-by').val();
    
    // Show loading state
    $('#plot-container').addClass('loading');
    
    // Get plot data from API
    $.getJSON('/api/plot', {
        type: plotType,
        x: xAxis,
        y: yAxis,
        color: colorBy
    }, function(plotData) {
        // Create or update the plot
        Plotly.react('plot-container', plotData.data, plotData.layout);
        
        // Remove loading state
        $('#plot-container').removeClass('loading');
    }).fail(function() {
        alert('Failed to create plot. Please check your selections.');
        $('#plot-container').removeClass('loading');
    });
}

// Handle plot type changes
function handlePlotTypeChange() {
    const plotType = $('#plot-type').val();
    
    // Adjust available options based on plot type
    if (plotType === 'box') {
        // For box plots, categorical x-axis often makes more sense
        if (columnInfo.categorical && columnInfo.categorical.length > 0) {
            $('#x-axis').val(columnInfo.categorical[0]);
        }
    }
}

// Error handling for missing data
window.addEventListener('error', function(e) {
    if (e.target.tagName === 'SCRIPT') {
        console.error('Error loading script:', e.target.src);
    }
});