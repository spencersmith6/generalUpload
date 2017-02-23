from flask import Flask, request
import time
import os
import tinys3

app = Flask(__name__)

def dump_files(clinic_name, files, notes):
    ts = time.time()
    stamp = '%s_%s'  % (clinic_name, str(int(round(ts))))
    folder = "files/%s/" % stamp
    os.makedirs(folder)
    f = open('%snotes' %folder, 'w')
    f.write(notes)

    # ##### For uploading to S3
    # conn = tinys3.Connection('S3_ACCESS_KEY', 'S3_SECRET_KEY', tls=True)
    # conn.upload(''.join([folder, f.filename]), f, 'my_bucket')
    # for f in files:
    #     conn.upload(''.join([folder, f.filename]), f, 'my_bucket')  # my_bucket is a bucket set up on aws
    #     #######

    f.close()
    for f in files:
        f.save(''.join([folder, f.filename]))


@app.route("/generalUpload", methods=["POST", "GET"])
def generalUpload():
    return app.send_static_file('uploadPage.html')

@app.route("/process", methods=["POST"])
def process():
    if request.method == "POST":
        if request.files['data'].filename == '':
            return app.send_static_file('Missing_File_Error_Page.html')
        if request.form['clinic'] == '':
            return app.send_static_file('Missing_File_Error_Page.html')
        clinic_name = request.form['clinic']
        uploaded_files = request.files.getlist("data")
        notes = request.form['notes']
        dump_files(clinic_name, uploaded_files, notes)
    return "Data has been recieved. Thank you for participating."

app.run()