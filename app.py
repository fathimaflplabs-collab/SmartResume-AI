from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from docx import Document
from analyzer import analyze_resume
import os


app = Flask(__name__)


# ==========================
# CONFIGURATION
# ==========================

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================
# CHECK FILE TYPE
# ==========================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================
# EXTRACT PDF TEXT
# ==========================

def extract_pdf_text(filepath):

    text = ""

    reader = PdfReader(filepath)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# ==========================
# EXTRACT DOCX TEXT
# ==========================

def extract_docx_text(filepath):

    document = Document(filepath)

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"

    return text


# ==========================
# HOME
# ==========================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================
# ANALYZE PAGE
# ==========================

@app.route("/analyze")
def analyze():

    return render_template("analyze.html")


# ==========================
# PROCESS RESUME
# ==========================

@app.route("/process-resume", methods=["POST"])
def process_resume():

    # Check file

    if "resume" not in request.files:

        return "No resume file uploaded."


    file = request.files["resume"]


    # Check filename

    if file.filename == "":

        return "No file selected."


    # Check extension

    if not allowed_file(file.filename):

        return "Only PDF and DOCX files are allowed."


    # Get target job

    target_job = request.form.get(
        "target_job",
        "Not specified"
    )


    # Secure filename

    filename = secure_filename(
        file.filename
    )


    # Save file

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)


    # ==========================
    # EXTRACT TEXT
    # ==========================

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()


    try:

        if extension == "pdf":

            resume_text = extract_pdf_text(
                filepath
            )

        elif extension == "docx":

            resume_text = extract_docx_text(
                filepath
            )

        else:

            resume_text = ""


    except Exception as error:

        return f"Could not read the resume: {error}"


    # ==========================
    # ANALYZE RESUME
    # ==========================

    analysis = analyze_resume(
        resume_text,
        target_job
    )


    # ==========================
    # SHOW RESULTS
    # ==========================

    return render_template(
        "results.html",
        filename=filename,
        target_job=target_job,
        resume_text=resume_text,
        analysis=analysis
    )


# ==========================
# RUN APPLICATION
# ==========================

if __name__ == "__main__":

    app.run(debug=True)