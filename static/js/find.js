document.getElementById('choicecat').addEventListener('change', function() {
    if (this.value == 'custom') {
        document.getElementById("inpbox").style.display = "inline-block";
    } else {
        document.getElementById("inpbox").style.display = "none";
    }
    if (this.value == 'state') {
        document.getElementById("sts").style.display = "inline-block";
    } else {
        document.getElementById("sts").style.display = "none";
    }
    if (this.value == 'city') {
        document.getElementById("sts").style.display = "inline-block";
        document.getElementById("state").style.display = "inline-block";
    } else {
        document.getElementById("state").style.display = "none";
    }
    if (this.value == 'Help Type') {
        document.getElementById("choicecat1").style.display = "inline-block";
    } else {
        document.getElementById("choicecat1").style.display = "none";
    }
    if (this.value == 'All Filters') {
        document.getElementById("sts").style.display = "inline-block";
        document.getElementById("state").style.display = "inline-block";
        document.getElementById("inpbox").style.display = "inline-block";
        document.getElementById("choicecat1").style.display = "inline-block";
    }
})

document.getElementById('sctnr').addEventListener('click', function() {
    if (document.getElementById('formcat').style.display == 'block') {
        document.getElementById('formcat').style.display = 'none';
        document.getElementById('sctnr').innerText = "Show Filters";
    } else {
        document.getElementById('formcat').style.display = 'block';
        document.getElementById('sctnr').innerText = "Hide Filters";
    }
});

document.getElementById("movebtn").addEventListener("click", function() {
    location.href = "/find";
})