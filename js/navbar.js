document.addEventListener("DOMContentLoaded", function () {
    fetch("navbar.html")                 // mengambil file navbar.html
        .then(response => response.text())
        .then(data => {
            document.getElementById("navbar").innerHTML = data;

            // Load CSS navbar
            let link = document.createElement("link");
            link.rel = "stylesheet";
            link.href = "navbar.css";
            document.head.appendChild(link);
        });
});
