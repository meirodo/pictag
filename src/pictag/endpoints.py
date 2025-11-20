from . import app
import os
from flask import render_template, redirect, request
from werkzeug.utils import secure_filename
from .ml import get_image_tags, model, preprocess

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/upload")
def upload():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        try:
            file.save(filepath)
            tags = get_image_tags(filepath, model, preprocess)
            return render_template("index.html", tags=tags)
        except Exception as e:
            print(f"処理中にエラーが発生しました: {e}")
            return render_template("index.html", error_message="処理中にエラーが発生しました。")
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
