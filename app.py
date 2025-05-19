from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "ExifTool API is running."

@app.route("/extract", methods=["POST"])
def extract_metadata():
    try:
        # Сохраняем весь входящий поток в temp файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(request.get_data())
            temp_path = temp_file.name

        # Вызываем exiftool
        result = subprocess.run(
            ["exiftool", "-j", temp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        metadata = result.stdout.decode("utf-8")

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "ExifTool failed",
            "details": e.stderr.decode("utf-8")
        }), 500

    except Exception as e:
        return jsonify({
            "error": "Unexpected error",
            "details": str(e)
        }), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return metadata, 200
