
async function updateGame(encodedVars) {
    console.log("Will update with: " + encodedVars);
}

// We need to dynamically load the search.js, otherwise
// it's functions aren't present to the dynamically loaded
// script form's embedded JS (ie: onclick() handlers).
function loadScript(url) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = "text/javascript";

    script.onload = function () {
        console.log("Search script loaded");
    };

    script.src = url;
    head.appendChild(script);
}

// Load the HTML for our search form
async function loadSearchForm() {
    const url = "http://localhost:22222/search";

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const formBody = await response.text();
        document.getElementById("searchForm").innerHTML = formBody;
    } catch (error) {
        console.error(error.message);
        alert("Failed loading search form!");
    }
}

loadScript("http://localhost:22222/html/search/search.js");
await loadSearchForm();
