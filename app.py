from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from predict import predict as _predict

ALLOWED_EXTENSIONS = {"jpg", "jpeg"}

app = Flask(__name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def upload():
    return render_template("upload.html")


@app.route("/predict/", methods=["POST"])
def predict():
    # handle binary data
    if request.mimetype != "multipart/form-data":
        response = make_response(_predict(request.stream), 200)
        response.mimetype = "text/plain"
        return response
    # check if the post request has the file part
    if "captcha" not in request.files:
        flash("No file part")
        return redirect(url_for("upload"))
    file = request.files["captcha"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("upload"))
    if file and allowed_file(file.filename):
        response = make_response(_predict(file.stream), 200)
        response.mimetype = "text/plain"
        return response
    return ("", 400)


if __name__ == "__main__":
    app.run(debug=True)