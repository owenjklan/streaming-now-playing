

async function submitSearch() {
    const url = "http://localhost:22222/search";

    const searchForm = document.getElementById('search-form');
    const searchData = new URLSearchParams();

    for (const pair of new FormData(searchForm)) {
        searchData.append(pair[0], pair[1]);
    }

    try {
        const response = await fetch(url, {method: 'POST', body: searchData});
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        // const formBody = parser.parseFromString(await response.text(), "text/html");
        const formBody = await response.text();
        document.getElementById("resultsTable").innerHTML = formBody;
    } catch (error) {
        console.error(error.message);
        alert("Failed loading search form!");
    }
}
