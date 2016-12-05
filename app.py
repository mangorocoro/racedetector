import os, time, subprocess, re, Image
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

            # grab the raw file and save it (can be any extension)
            untouched_filename = secure_filename(file.filename)    
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], untouched_filename)
            file.save(filepath)
            

            # get image file's extension (png, gif, tiff, etc)
            im = Image.open(filepath)
            im_extension = "."+im.format
            im_extension = im_extension.lower()

            

            if im_extension != '.jpg':
                # create jpg name of file
                jpg_filename = re.split(im_extension, untouched_filename).pop(0) + ".jpg"
                # save the jpg filename into folder
                jpg_filepath = 'uploads/'+jpg_filename
                Image.open(filepath).save(jpg_filepath)
                # once jpg file is saved, remove the other file
                os.remove(filepath)
                filepath = jpg_filepath

            print "filepath after {}".format(filepath)

            # *process the inputted image with tensorflow classifier
            # *pull the probabilities for each of the labels (put in hash)
            # *grab the highest probability label -- that will be your image's classification
            ethnicity_string = classify(filepath.lower())
            
            # after processing is done, display results page
            return render_template('answer.html', ethnicity_string = ethnicity_string, filepath = filepath)
            

    return render_template('index.html')



def classify(filepath):
    
    tensor_output_raw = subprocess.check_output("python2 tf_files/label_image_asian4.py "+filepath, shell=True).rstrip()
    tensor_output = tensor_output_raw.split('\n')

    print tensor_output
    
    dicto = {}
    for output in tensor_output:
        parsed = re.split(r'[() ]', output) #['chinese', '', 'score', '=', '0.43429', '']
        label = parsed.pop(0)
        prob = float(parsed.pop(-2))
        dicto[label] = prob

    max = None
    label = None
    for key in dicto:
        if dicto[key] > max:
            max = dicto[key]
            label = key

    return label


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)



if __name__ == "__main__":
    app.secret_key = 'asdfasdf'

    app.run()

