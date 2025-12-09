document.addEventListener("DOMContentLoaded", function () {
    fetch("footer.html")                 // mengambil file navbar.html
        .then(response => response.text())
        .then(data => {
            document.getElementById("footer").innerHTML = data;

            // Load CSS navbar
            let link = document.createElement("link");
            link.rel = "stylesheet";
            link.href = "footer.css";
            document.head.appendChild(link);
        });
});
