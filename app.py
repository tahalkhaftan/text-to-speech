from pathlib import Path
import asyncio

from flask import Flask, jsonify, request, send_file, send_from_directory
from voice import create_voice

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "voice.mp3"


@app.route("/")
def index():
    # index.html is in the SAME folder as app.py
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    text = str(data.get("text", "")).strip()
    language = str(data.get("language", "fa"))
    gender = str(data.get("gender", "male"))

    if not text:
        return jsonify({"error": "لطفاً یک متن وارد کنید."}), 400

    if language not in {"fa", "en"}:
        return jsonify({"error": "زبان انتخاب‌شده معتبر نیست."}), 400

    if gender not in {"male", "female"}:
        return jsonify({"error": "نوع صدا معتبر نیست."}), 400

    try:
        asyncio.run(
            create_voice(
                text=text,
                language=language,
                gender=gender,
                output_path=OUTPUT_FILE
            )
        )
    except Exception as exc:
        return jsonify({
            "error": "ساخت صدا انجام نشد.",
            "details": str(exc)
        }), 500

    return jsonify({
        "success": True,
        "audio_url": "/audio",
        "download_url": "/download"
    })


@app.route("/audio")
def audio():
    if not OUTPUT_FILE.exists():
        return "voice.mp3 هنوز ساخته نشده است.", 404

    return send_file(
        OUTPUT_FILE,
        mimetype="audio/mpeg",
        conditional=True
    )


@app.route("/download")
def download():
    if not OUTPUT_FILE.exists():
        return "voice.mp3 هنوز ساخته نشده است.", 404

    return send_file(
        OUTPUT_FILE,
        mimetype="audio/mpeg",
        as_attachment=True,
        download_name="voice.mp3"
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
