async function applyManualValues() {
    const title = document.getElementById("manualTitle").value;
    const platform = document.getElementById("manualPlatform").value;
    const region = document.getElementById("manualRegion").value;
    const thumbnail_image = document.getElementById("manualCaseImage").src.value;

    const url = "/manual_update"
    console.log("Stashed Thumbnail image: " + thumbnail_image);

    const updateBody = {
        title: title,
        platform: platform,
        region: region,
        image_data: thumbnail_image
    }

    try {
        const response = await fetch(
            url,
            {
                method: 'POST',
                body: JSON.stringify(updateBody),
                headers: {'Content-Type': "application/json"}
            });
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

async function submitSearch() {
    // Send search to our back-end, which will then pass it off
    // to the ROM site and return parsed details, suitable for
    // submitting to the "/update" endpoint.
    const url = "/search";

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
