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
    fetch('/dispense')
        .then(res => res.json())
        .then(data => {
            document.getElementById('status').innerText = data.status;
            setTimeout(() => { document.getElementById('status').innerText = ''; }, 3000);
        });
}

setInterval(updateResult, 1000);
