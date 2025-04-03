# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import pickle
import json
import plotly
import plotly.express as px
import os

app = Flask(__name__)

# Load the data from pickle file
def load_data():
    try:
        with open('data.pkl', 'rb') as file:
            data = pickle.load(file)
        return pd.DataFrame(data) if not isinstance(data, pd.DataFrame) else data
    except Exception as e:
        print(f"Error loading data: {e}")
        # Return empty DataFrame if file not found or other error
        return pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/columns')
def get_columns():
    df = load_data()
    numeric_columns = list(df.select_dtypes(include='number').columns)
    categorical_columns = list(df.select_dtypes(include=['object', 'category']).columns)
    
    return jsonify({
        'numeric': numeric_columns,
        'categorical': categorical_columns,
        'index': list(df.index.astype(str))
    })

@app.route('/api/data')
def get_data():
    df = load_data()
    return df.to_json(orient='records')

@app.route('/api/plot')
def get_plot():
    plot_type = request.args.get('type', 'line')
    x_column = request.args.get('x')
    y_column = request.args.get('y')
    color_by = request.args.get('color')
    
    df = load_data()
    
    if y_column not in df.columns:
        return jsonify({'error': 'Y column not found'})
    
    # Create plot based on type
    if plot_type == 'line':
        fig = px.line(df, x=x_column, y=y_column, color=color_by)
    elif plot_type == 'bar':
        fig = px.bar(df, x=x_column, y=y_column, color=color_by)
    elif plot_type == 'scatter':
        fig = px.scatter(df, x=x_column, y=y_column, color=color_by)
    elif plot_type == 'box':
        fig = px.box(df, x=x_column, y=y_column, color=color_by)
    else:
        # Default to line
        fig = px.line(df, x=x_column, y=y_column, color=color_by)
    
    # Update layout for better appearance
    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    
    # Convert the figure to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/api/summary')
def get_summary():
    df = load_data()
    summary = {
        'rows': len(df),
        'columns': len(df.columns),
        'column_types': df.dtypes.astype(str).to_dict(),
        'numeric_summary': df.describe().to_dict()
    }
    return jsonify(summary)

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)