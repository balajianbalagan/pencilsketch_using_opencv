from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import flash
import os
import cv2

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'balaji'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/after', methods=['GET', 'POST'])
def after():
    img = request.files['file']
    img.save("static/process/file.jpg")
    image = cv2.imread("static/process/file.jpg")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = 255 - gray_image
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    inverted_blurred = 255 - blurred
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)

    cv2.imwrite("static/process/filep.jpg", pencil_sketch)

    return render_template('after.html')


@app.route('/save')
def save():
    image = cv2.imread("static/process/filep.jpg")
    imagelist = os.listdir('static/saved')
    str1 = "static/saved/" + str(len(imagelist)) + ".jpg"
    try:
        cv2.imwrite(str1, image)

    except:
        flash("image save not successful", "error")
    flash("image saved successfully!", "success")
    return redirect(url_for('index'))


@app.route('/mysketches')
def mysketches():
    imagelist = os.listdir('static/saved')
    imagelist = ['saved/' + image for image in imagelist]
    return render_template("mysketches.html", imagelist=imagelist)


@app.route('/mysketches/delete/<path:filepath>')
def delete(filepath):
    os.remove(filepath)
    return redirect(url_for('mysketches'))


app.run(debug=True)
