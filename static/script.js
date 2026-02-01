let scanInterval = null;

function startScan() {
    const cam = document.getElementById("cameraFeed");
    const placeholder = document.getElementById("cameraPlaceholder");

    placeholder.style.display = "none";
    cam.src = "/video";
    cam.style.display = "block";

    if (!scanInterval) {
        scanInterval = setInterval(updateResult, 1000);
    }
}


function stopScan() {
    const cam = document.getElementById("cameraFeed");
    const placeholder = document.getElementById("cameraPlaceholder");

    cam.src = "";
    cam.style.display = "none";
    placeholder.style.display = "flex";

    if (scanInterval) {
        clearInterval(scanInterval);
        scanInterval = null;
    }

    document.getElementById("skin").innerText = "Stopped";
    document.getElementById("skin_type").innerText = "-";
    document.getElementById("rec").innerText = "-";
    document.getElementById("brand").innerText = "-";
}


function updateResult() {
    fetch('/result')
        .then(res => res.json())
        .then(data => {
            document.getElementById('skin').innerText = data.skin_tone;
            document.getElementById('skin_type').innerText = data.skin_type;
            document.getElementById('rec').innerText = data.recommendation;
            document.getElementById('brand').innerText = data.brand;
        });
}


function dispense() {
    const status = document.getElementById("status");

    // Step 1: show dispensing
    status.innerText = "🧴 Dispensing...";
    status.style.color = "green";

    // Step 2: after 2 seconds, show dispensed
    setTimeout(() => {
        status.innerText = "✅ Dispensed";
    }, 2000);

    // Step 3: after 4 seconds, clear message
    setTimeout(() => {
        status.innerText = "";
    }, 4000);
}





