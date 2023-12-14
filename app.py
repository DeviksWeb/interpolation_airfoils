from flask import Flask, render_template, request, send_file, redirect, session, url_for
import aerosandbox as asb
from datetime import datetime
from waitress import serve

app = Flask(__name__)

@app.route("/")
def running():
    return render_template('index.html')

@app.route("/", methods=["POST"])
def get_values():
    model = request.form['model']
    quality = int(request.form['quality'])
    af = asb.Airfoil(model)
    af = af.repanel(n_points_per_side=(int(quality)))
    now = datetime.now()
    date_time = now.strftime("%d%m%Y%H%M%S")
    file_name = model + "_" + str(int(quality)) + str(date_time) + ".dat"
    af.write_dat(filepath=file_name)
    return redirect(url_for(".download", file_name=file_name))

@app.route("/download")
def download():
    file_name = request.args["file_name"]
    return send_file(file_name, as_attachment=True)

serve(app, host="0.0.0.0", port=8080)
