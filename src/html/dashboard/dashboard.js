// We need to dynamically load the search.js, otherwise
// it's functions aren't present to the dynamically loaded
// script form's embedded JS (ie: onclick() handlers).
function loadScript(url) {
    const head = document.getElementsByTagName('head')[0];
    const script = document.createElement('script');
    script.type = "text/javascript";

    script.onload = function () {
        console.log("Search script loaded");
    };

    script.src = url;
    head.appendChild(script);
}

// Load the HTML for our search form
async function loadSearchForm() {
    const url = "/search";

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        document.getElementById("searchForm").innerHTML = await response.text();
    } catch (error) {
        console.error(error.message);
        alert("Failed loading search form!");
    }
}

loadScript("/html/search/search.js");

// Load the HTML for the search form
await loadSearchForm();
