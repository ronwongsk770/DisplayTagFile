from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import io
import pyperclip

app = Flask(__name__)

# In-memory storage
filtered_data = []

@app.route('/')
def index():
    return render_template('index.html', data=[])

@app.route('/filter', methods=['POST'])
def filter_text():
    global filtered_data
    text = request.form.get('input_text', '').strip()

    if not text:
        return jsonify({"error": "Please enter some text."}), 400

    # Split based on 'F10'
    parts = text.split("F10")
    filtered_data = ["F10" + part.strip() for part in parts if part.strip()]
    return jsonify({"data": filtered_data, "count": len(filtered_data)})

@app.route('/copy', methods=['POST'])
def copy_data():
    global filtered_data
    if not filtered_data:
        return jsonify({"error": "No data to copy."}), 400
    pyperclip.copy("\n".join(filtered_data))
    return jsonify({"message": "Data copied to clipboard!"})

@app.route('/download_csv')
def download_csv():
    global filtered_data
    if not filtered_data:
        return jsonify({"error": "No data to download."}), 400
    df = pd.DataFrame(filtered_data, columns=["F10 Data"])
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="f10_data.csv", mimetype='text/csv')

@app.route('/search', methods=['POST'])
def search():
    global filtered_data
    query = request.form.get('query', '').lower().strip()
    if not query:
        return jsonify({"data": filtered_data})
    results = [d for d in filtered_data if query in d.lower()]
    return jsonify({"data": results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, debug=True)

