#Third Party Dep
from flask import Flask, jsonify, render_template, request, send_from_directory
import os
from uuid import uuid4


#Internal Dependencies
from users import users


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/', methods = ['GET'])
def ping():
    return render_template('upload.html')


@app.route('/users', methods = ['GET'])
def userhandle():
    return jsonify({'user' : users})

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static", filename)

@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)

