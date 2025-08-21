// tickerLoader.js
document.addEventListener("DOMContentLoaded", function () {
    let depth = window.location.pathname.split("/").length - 2;
    let prefix = "";
    for (let i = 0; i < depth; i++) {
        prefix += "../";
    }

    fetch(prefix + "ticker.html")
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

            document.getElementById("ticker-placeholder").innerHTML = tempDiv.innerHTML;
        })
        .catch(error => {
            console.error("Error loading the ticker:", error);
        });
});
