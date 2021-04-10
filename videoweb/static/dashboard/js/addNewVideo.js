document.onclick = function (e) {
    e = e || event;
    e.stopPropagation();
    let form = document.getElementById("add-video");
    let btn = document.getElementById("add-video-btn");
    let input = document.getElementById("url")
    let target = e.target || e.srcElement;
    if (target!=btn && target!=form && target!=input) {
        form.style.display = "none";
    } else {
        form.style.display = "flex";
    }
}

