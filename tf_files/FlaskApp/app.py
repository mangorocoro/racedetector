import os, time
from flask import Flask, request, redirect, url_for, send_from_directory, flash, render_template
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
                        
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # save inputted image into uploads folder
            file.save(filepath)


            # *process the inputted image with tensorflow classifier
            # *pull the probabilities for each of the labels (put in hash)
            # *grab the highest probability label -- that will be your image's classification

            #ethnicity_string = run_classifier(filename)

            # assign highest probability labels to variable to display custom 
            # large text banner

            # processing function will block until done
            ethnicity_string = 'korean'

            # after processing is done, display results page
            return render_template('answer.html', ethnicity_string = ethnicity_string, filepath = filepath)

            #return redirect(url_for('uploaded_file', filename=filename))

    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)




if __name__ == "__main__":
    app.secret_key = 'asdfasdf'

    app.run()

