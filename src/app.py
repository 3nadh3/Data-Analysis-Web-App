from flask import Flask, render_template, request, jsonify
import pandas as pd
import io
from io import BytesIO
import json
from analysis import analyze_data
import numpy as np

app = Flask(__name__, static_url_path='/static')

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (pd.Timestamp, pd.Period)):
            return obj.isoformat()
        elif isinstance(obj, pd.Series):
            return obj.tolist()
        elif isinstance(obj, pd.Int64Dtype):
            return int(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        else:
            return super().default(obj)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        try:
            # Read the uploaded file into a Pandas DataFrame
            df = pd.read_csv(BytesIO(file.stream.read()))

            # Call the analysis function
            result = analyze_data(df)

            # Convert the result to JSON using custom encoder
            result_json = json.dumps(result, cls=CustomJSONEncoder)

            # Return the analysis result as JSON
            return jsonify({'data': json.loads(result_json)})
        except Exception as e:
            return jsonify({'error': f'Error processing the file: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

