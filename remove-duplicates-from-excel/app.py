from flask import Flask, request, render_template, send_file, flash, redirect
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Process the file
            df = pd.read_excel(filepath)

            # Check if 'Id' column exists
            if 'Id' not in df.columns:
                flash('ID column not found in the uploaded file.')
                return redirect(request.url)

            # Remove duplicates based on 'Id' column
            df_cleaned = df.drop_duplicates(subset='Id', keep='first')
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'cleaned_' + file.filename)
            df_cleaned.to_excel(output_filepath, index=False)

            return send_file(output_filepath, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
