import pandas as pd
import pickle
import argparse
import os

def convert_file_to_pickle(input_file, output_file='data.pkl'):
    """
    Convert various file formats to pickle file for the dashboard.
    
    Supported formats:
    - CSV
    - Excel
    - JSON
    - Parquet
    - Python file with DataFrame variable
    
    Args:
        input_file (str): Path to the input file
        output_file (str): Path to save the pickle file
    """
    file_extension = os.path.splitext(input_file)[1].lower()
    
    try:
        # Handle different file types
        if file_extension == '.csv':
            df = pd.read_csv(input_file,encoding='ISO-8859-1')
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(input_file)
        elif file_extension == '.json':
            df = pd.read_json(input_file)
        elif file_extension == '.parquet':
            df = pd.read_parquet(input_file)
        elif file_extension == '.py':
            # This is a bit risky but can be useful for quick testing
            # The Python file should contain a DataFrame named 'data'
            namespace = {}
            with open(input_file, 'r') as f:
                exec(f.read(), namespace)
            if 'data' in namespace:
                df = namespace['data']
            else:
                raise ValueError("Python file must contain a DataFrame named 'data'")
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Save to pickle
        with open(output_file, 'wb') as f:
            pickle.dump(df, f)
        
        print(f"Successfully converted {input_file} to {output_file}")
        print(f"Data shape: {df.shape}")
        print(f"Columns: {', '.join(df.columns)}")
        
    except Exception as e:
        print(f"Error converting file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert data file to pickle for dashboard")
    parser.add_argument("input_file", help="Path to input data file")
    parser.add_argument("--output", "-o", default="data.pkl", help="Path for output pickle file")
    
    args = parser.parse_args()
    convert_file_to_pickle(args.input_file, args.output)