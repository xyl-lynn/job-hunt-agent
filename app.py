from flask import Flask, request, jsonify, render_template
import os
import tempfile
from PyPDF2 import PdfReader
from tools.jd_parser import parse_jd
from tools.resume import get_resume_summary
from tools.interview import generate_interview_prep
from memory.store import save_application, check_followups, list_all, update_status, delete_application, edit_application

app = Flask(__name__)


def extract_pdf_text(file) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        reader = PdfReader(tmp.name)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    os.unlink(tmp.name)
    return text.strip()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze/jd", methods=["POST"])
def analyze_jd():
    try:
        resume_file = request.files.get("resume")
        jd_text = request.form.get("jd_text", "").strip()
        if not resume_file or not jd_text:
            return jsonify({"error": "请上传简历并填写职位描述"}), 400
        resume_text = extract_pdf_text(resume_file)
        jd_info = parse_jd(jd_text)
        return jsonify({"jd_info": jd_info, "resume_text": resume_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analyze/advice", methods=["POST"])
def analyze_advice():
    try:
        data = request.json
        advice = get_resume_summary(data["resume_text"], data["jd_info"])
        return jsonify({"advice": advice})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analyze/interview", methods=["POST"])
def analyze_interview():
    try:
        data = request.json
        interview = generate_interview_prep(data["resume_text"], data["jd_info"])
        return jsonify({"interview": interview})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/applications", methods=["GET"])
def applications():
    return jsonify(list_all())


@app.route("/applications", methods=["POST"])
def add_application():
    try:
        data = request.json
        record = save_application(
            company=data.get("company", "未知"),
            position=data.get("position", "未知"),
            jd_summary=data.get("jd_summary", ""),
            remind_days=data.get("remind_days", 7)
        )
        return jsonify(record)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/applications/<int:record_id>", methods=["PATCH"])
def patch_application(record_id):
    try:
        data = request.json
        record = update_status(record_id, data.get("status"), data.get("notes", ""))
        if not record:
            return jsonify({"error": "记录不存在"}), 404
        return jsonify(record)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/applications/<int:record_id>", methods=["DELETE"])
def remove_application(record_id):
    try:
        delete_application(record_id)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/applications/<int:record_id>/edit", methods=["PATCH"])
def edit_app(record_id):
    try:
        data = request.json
        record = edit_application(record_id, data.get("company"), data.get("position"))
        if not record:
            return jsonify({"error": "记录不存在"}), 404
        return jsonify(record)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/followups")
def followups():
    return jsonify(check_followups())


if __name__ == "__main__":
    app.run(debug=True, port=5001)