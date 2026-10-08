const uploadArea = document.getElementById("uploadArea");

const resumeFile = document.getElementById("resumeFile");

const selectedFile = document.getElementById("selectedFile");

const fileName = document.getElementById("fileName");

const fileSize = document.getElementById("fileSize");

const removeFile = document.getElementById("removeFile");

const jobCards = document.querySelectorAll(".job-card");

const selectedJob = document.getElementById("selectedJob");

const customJob = document.getElementById("customJob");

const analyzeButton = document.getElementById("analyzeButton");


let currentFile = null;
let currentJob = "";


// ==========================
// FILE SELECTION
// ==========================

resumeFile.addEventListener("change", function () {

    if (this.files.length > 0) {

        handleFile(this.files[0]);

    }

});


function handleFile(file) {

    const allowedTypes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ];

    if (!allowedTypes.includes(file.type)) {

        alert("Please upload a PDF or DOCX file.");

        return;
    }


    if (file.size > 10 * 1024 * 1024) {

        alert("File size must be less than 10 MB.");

        return;
    }


    currentFile = file;


    fileName.textContent = file.name;


    const sizeInKB = (file.size / 1024).toFixed(1);

    fileSize.textContent = sizeInKB + " KB";


    selectedFile.style.display = "flex";


    uploadArea.style.borderColor = "#5b5ce2";
}


// ==========================
// REMOVE FILE
// ==========================

removeFile.addEventListener("click", function () {

    currentFile = null;

    resumeFile.value = "";

    selectedFile.style.display = "none";

    uploadArea.style.borderColor = "#cfd4e4";

});


// ==========================
// DRAG & DROP
// ==========================

uploadArea.addEventListener("dragover", function (event) {

    event.preventDefault();

    uploadArea.classList.add("dragover");

});


uploadArea.addEventListener("dragleave", function () {

    uploadArea.classList.remove("dragover");

});


uploadArea.addEventListener("drop", function (event) {

    event.preventDefault();

    uploadArea.classList.remove("dragover");


    const files = event.dataTransfer.files;


    if (files.length > 0) {

        handleFile(files[0]);

    }

});


// ==========================
// JOB SELECTION
// ==========================

jobCards.forEach(function (card) {

    card.addEventListener("click", function () {

        jobCards.forEach(function (item) {

            item.classList.remove("selected");

        });


        this.classList.add("selected");


        currentJob = this.dataset.job;


        selectedJob.textContent = currentJob;


        customJob.value = "";

    });

});


// ==========================
// CUSTOM JOB
// ==========================

customJob.addEventListener("input", function () {

    const value = this.value.trim();


    if (value !== "") {

        jobCards.forEach(function (card) {

            card.classList.remove("selected");

        });


        currentJob = value;


        selectedJob.textContent = currentJob;

    }

});


// ==========================
// ANALYZE BUTTON
// ==========================

analyzeButton.addEventListener("click", function () {

    if (!currentFile) {

        alert("Please upload your resume first.");

        return;
    }


    if (!currentJob) {

        alert("Please select a target job.");

        return;
    }


    const formData = new FormData();


    formData.append(
        "resume",
        currentFile
    );


    formData.append(
        "target_job",
        currentJob
    );


    analyzeButton.disabled = true;

    analyzeButton.innerHTML =
        "Analyzing Resume...";


    fetch("/process-resume", {

        method: "POST",

        body: formData

    })

    .then(function(response) {

        return response.text();

    })

    .then(function(data) {

        document.open();

        document.write(data);

        document.close();

    })

    .catch(function(error) {

        console.error(error);

        alert(
            "Something went wrong while uploading the resume."
        );


        analyzeButton.disabled = false;

        analyzeButton.innerHTML =
            "Analyze My Resume →";

    });

});