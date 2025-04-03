# Dynamic Data Visualization Dashboard

This web application allows you to create interactive visualizations from your data files. It supports loading data from pickle (.pkl) files and provides an intuitive interface for exploring your data.

## Features

- Interactive visualizations with Plotly
- Multiple chart types: line charts, bar charts, scatter plots, and box plots
- Dynamic data filtering and visualization options
- Data preview table
- Responsive design for different screen sizes

## Installation

1. Install the required dependencies:

```bash
pip install flask pandas plotly
```

2. Clone or download this repository to your local machine.

## Usage

### Step 1: Prepare your data

You can convert your existing data files (CSV, Excel, JSON, etc.) to a pickle file using the included `data_loader.py` script:

```bash
python data_loader.py your_data.csv
```

This will create a `data.pkl` file in the current directory.

If you already have a pickle file, make sure it contains a pandas DataFrame or a data structure that can be converted to a DataFrame.

### Step 2: Run the application

```bash
python app.py
```

This will start the Flask server on http://localhost:5000.

### Step 3: Access the dashboard

Open your web browser and navigate to http://localhost:5000 to view and interact with your data.

## File Structure

```
├── app.py                  # Main Flask application
├── data_loader.py          # Utility to convert data files to pickle
├── data.pkl                # Your data (generated or provided by you)
├── static/
│   ├── css/
│   │   └── styles.css      # CSS styles for the dashboard
│   └── js/
│       └── dashboard.js    # JavaScript code for interactive features
└── templates/
    └── index.html          # HTML template for the dashboard
```

## Customization

### Adding new chart types

To add new chart types, modify the `get_plot` function in `app.py` and add the corresponding option in the `index.html` template.

### Styling

The dashboard styles can be customized by editing the `static/css/styles.css` file.

## Troubleshooting

- **Data not loading**: Make sure your pickle file is in the correct format and contains valid data.
- **No plots appearing**: Check that your data contains the columns you're trying to visualize.
- **Server errors**: Look at the Flask server console output for error messages.

## License

This project is open-source and available for personal and commercial use.