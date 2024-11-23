const socket = io();

socket.on("connect", () => {
    console.log("connected");
});

socket.on("disconnect", () => {
    console.log("disconnected");
});

// function emit_example() {
//     //Event sent by Client
//     socket.emit("my_event", function() {
//     });
// }


socket.on("server", function(msg) {
    serverMessage = msg;

    document.getElementById("gameTitle").innerHTML = serverMessage.game_title;

    if ('game_region' in serverMessage && serverMessage.game_region !== null) {
        document.getElementById("gameRegion").innerHTML = serverMessage.game_region;
    } else {
        document.getElementById("gameRegion").innerHTML = "Unknown";
    }

    if ('game_platform' in serverMessage && serverMessage.game_platform !== null) {
        document.getElementById("gamePlatform").innerHTML = serverMessage.game_platform;
    } else {
        document.getElementById("gamePlatform").innerHTML = "Unknown";
    }

    console.log("Image data: " + serverMessage.image_data);

    document.getElementById("gameCaseImage").src = serverMessage.image_data;
});