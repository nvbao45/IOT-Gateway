import { io } from "/static/assets/js/baonv/socket.io.esm.min.js";

$(function(){
    const socket = io();
    socket.on("connect", function(){
        console.log("connected");
        socket.emit("get", {
            "type": "sensordata",
            "content": {
                "sensor": "temperature"
            }
        })
    });

    socket.on("data", function(data){
        console.log(data);
    });

    socket.on("get", function(data){
        console.log(data);
    });
})

/*import { io } from "/static/assets/js/baonv/socket.io.esm.min.js";

let data = [];
let sim_data = [];

let activity = document.getElementById("activity-feed");
let sim_activity = document.getElementById("sim-activity-feed");
const socket = io.connect();

$(function(){
    if (localStorage.activity){
        data = JSON.parse(localStorage.activity);
    }
    if (localStorage.simactivity){
        sim_data = JSON.parse(localStorage.simactivity);
    }
    show_activity(data);
    show_sim_activity(sim_data);
})

function show_activity(data){
    localStorage.setItem("activity", JSON.stringify(data));
    let itemColor = ['primary', 'success', 'danger', 'warning', 'info', 'primary', 'success', 'danger', 'warning', 'info'];
    activity.innerHTML = "";
    for (let i = 0; i < data.length; i++){
        activity.innerHTML += `
            <li class="feed-item feed-item-${itemColor[i]}">
                <time class="date" datetime="9-25"><span class="text-warning">${data[i].timestamp}</span></time>
                <span class="text">
                    Node <span class="text-primary">${data[i].node_name}</span>
                    gửi dữ liệu cảm biến <span class="text-danger">${data[i].sensor}</span>
                    với giá trị <span class="text-info">${data[i].value}</span>
                </span>
            </li>
        `
    }
}

function show_sim_activity(data){
    localStorage.setItem("simactivity", JSON.stringify(data));
    let itemColor = ['primary', 'success', 'danger', 'warning', 'info'];
    sim_activity.innerHTML = "";
    for (let i = 0; i < data.length; i++){
        sim_activity.innerHTML += `
            <li class="feed-item feed-item-${itemColor[i]}">
                <time class="date" datetime="9-25"><span class="text-warning"></span></time>
                <span class="text">
                    ${data[i]}
                </span>
            </li>
        `
    }
}

socket.on("message", (dt) => {
    if (data.length < 10) {
        data.unshift(dt);
    } else {
        data.pop();
        data.unshift(dt);
    }
    show_activity(data);
});

socket.on("sim_message", (dt) => {
    console.log(dt)
    if (sim_data.length < 5) {
        sim_data.unshift(dt);
    } else {
        sim_data.pop();
        sim_data.unshift(dt);
    }
    show_sim_activity(sim_data);
});

socket.on("error", (error) => {
    console.error(error);
});
socket.on("reconnect", (attempt) => {
    console.log(`Reconnecting to server. Attempt: ${attempt}`);
});
socket.on("reconnect_attempt", (attempt) => {
    console.log(`Attempting to reconnect to server. Attempt: ${attempt}`);
});
socket.on("reconnect_failed", (attempt) => {
    console.log(`Reconnecting to server. Attempt: ${attempt}`);
});
socket.on("connect", () => {
    console.log("Connected to server");
});
socket.on("disconnect", () => {
    console.log("Disconnected to server");
});

*/
