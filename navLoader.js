document.addEventListener("DOMContentLoaded", function () {
    // Determine the relative path to the root
    let pathPrefix = "";
    let depth = window.location.pathname.split("/").length - 2; // subtracting 2 to exclude domain and file name
    for (let i = 0; i < depth; i++) {
        pathPrefix += "../";
    }

    fetch(pathPrefix + "nav.html")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("nav-placeholder").innerHTML = data;
        })
        .catch(error => {
            console.error("Error loading the navigation:", error);
        });
});

document.addEventListener("DOMContentLoaded", function () {
    let depth = window.location.pathname.split("/").length - 2;
    let prefix = "";
    for (let i = 0; i < depth; i++) {
        prefix += "../";
    }

    fetch(prefix + "nav.html")
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            return response.text();
        })
        .then(data => {
            const tempDiv = document.createElement("div");
            tempDiv.innerHTML = data;

            tempDiv.querySelectorAll("a, img").forEach(el => {
                if (el.hasAttribute("href")) {
                    const href = el.getAttribute("href");
                    if (!href.startsWith("http") && !href.startsWith("#")) {
                        el.setAttribute("href", prefix + href.replace(/^\.\//, ""));
                    }
                }
                if (el.hasAttribute("src")) {
                    const src = el.getAttribute("src");
                    el.setAttribute("src", prefix + src.replace(/^\.\//, ""));
                }
            });

            document.getElementById("nav-placeholder").innerHTML = tempDiv.innerHTML;
        })
        .catch(error => {
            console.error("Error loading the navigation:", error);
        });
});
