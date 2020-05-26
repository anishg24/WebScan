/*
 * Copyright (c) 2020. Anish Govind
 * https://github.com/anishg24
 */

const buttonCapture = document.getElementById("capture");

buttonCapture.onclick = function () {
    // XMLHttpRequest
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // alert(xhr.responseText);
            const image = document.getElementById("image");
            image.src = "/image_viewer?" + new Date().getTime();
        }
    };
    xhr.open("POST", "/capture_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({status: "true"}));
};