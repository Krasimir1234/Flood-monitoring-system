let reports = [];  // Array -> hold submitted reports

// Function -> change profile pic
function changeProfilePic() {
    document.getElementById("fileInput").click();
}

// Function -> upload a new profile picture
function uploadPicture() {
    const fileInput = document.getElementById("fileInput");
    const profilePic = document.getElementById("profilePic");

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            profilePic.src = e.target.result;
        };
        reader.readAsDataURL(fileInput.files[0]);
    }
}

// Function -> enable profile editing
function editProfile() {
    document.getElementById("nameDisplay").style.display = "none";
    document.getElementById("nameInput").style.display = "inline";
    document.getElementById("emailDisplay").style.display = "none";
    document.getElementById("emailInput").style.display = "inline";
    document.getElementById("usernameDisplay").style.display = "none";
    document.getElementById("usernameInput").style.display = "inline";

    document.getElementById("editBtn").style.display = "none";
    document.getElementById("saveBtn").style.display = "inline";
}

// Function -> save profile changes
function saveProfile() {
    document.getElementById("nameDisplay").textContent = document.getElementById("nameInput").value;
    document.getElementById("emailDisplay").textContent = document.getElementById("emailInput").value;
    document.getElementById("usernameDisplay").textContent = document.getElementById("usernameInput").value;

    document.getElementById("nameDisplay").style.display = "inline";
    document.getElementById("nameInput").style.display = "none";
    document.getElementById("emailDisplay").style.display = "inline";
    document.getElementById("emailInput").style.display = "none";
    document.getElementById("usernameDisplay").style.display = "inline";
    document.getElementById("usernameInput").style.display = "none";

    document.getElementById("editBtn").style.display = "inline";
    document.getElementById("saveBtn").style.display = "none";
}

// Function -> submit a report
function submitReport() {
    const reportStatus = "Unverified";  // Default status
    const reportDescription = document.getElementById("reportDescription").value;
    const reportImage = document.getElementById("reportImage").files[0];
    const reportVideo = document.getElementById("reportVideo").files[0];
    const reportLocation = document.getElementById("reportLocation").value;
    const maxVideoSize = 15 * 1024 * 1024;  // 15 MB max
    const maxImageSize = 5 * 1024 * 1024;   // 5 MB max

    if (!reportDescription) {
        alert("Please enter a description for the report.");
        return;
    }

    if (!reportLocation) {
        alert("Please enter a location to submit the report.");
        return;
    }

    if (reportImage && reportImage.size > maxImageSize) {
        alert("The image file is too large. Please upload an image that is 5 MB or smaller.");
        return;
    }

    if (reportVideo && reportVideo.size > maxVideoSize) {
        alert("The video file is too large. Please upload a video that is 15 MB or smaller.");
        return;
    }

    const newReport = {
        id: reports.length + 1,
        status: reportStatus,
        description: reportDescription,
        location: reportLocation,
        image: reportImage ? reportImage.name : "No image uploaded",
        video: reportVideo ? reportVideo.name : "No video uploaded",
        timestamp: new Date().toLocaleString(), // Submission time
    };

    reports.push(newReport);  // Save report in array
    alert("Report submitted successfully and sent to the government as 'Unverified'.");

    document.getElementById("reportForm").reset();

    displayReports();
}

// Function -> display reports
function displayReports() {
    const reportList = document.getElementById("reportList");
    reportList.innerHTML = "";  // Clear previous list

    reports.forEach(report => {
        const reportDiv = document.createElement("div");
        reportDiv.classList.add("report");

        reportDiv.innerHTML = `
            <p><strong>Report ID:</strong> ${report.id}</p>
            <p><strong>Description:</strong> ${report.description}</p>
            <p><strong>Location:</strong> ${report.location}</p>
            <p><strong>Image:</strong> ${report.image}</p>
            <p><strong>Video:</strong> ${report.video}</p>
            <p><strong>Status:</strong> ${report.status}</p>
            <p><strong>Submitted:</strong> ${report.timestamp}</p>
            <hr>
        `;

        reportList.appendChild(reportDiv);
    });
}

// Simulate government login to view reports
function simulateGovernmentLogin() {
    document.getElementById("verificationSection").style.display = "block";
    displayReports();
}

simulateGovernmentLogin();  // Display reports for the government view
