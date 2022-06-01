let socket;

if (location.protocol === 'http:') {
    socket = new WebSocket('ws://' + location.host + '/ws/system-info');
} else {
    socket = new WebSocket('wss://' + location.host + '/ws/system-info');
}

socket.addEventListener('message', ev => {
    const data = JSON.parse(ev.data);

    $('#system-cpu-temp').text(data['cpu_temp'] + '°C');
    $('#system-cpu').text(data['cpu'] + '%');
    $('#system-ram').text(data['ram_free'] + 'MB');
    $('#system-disk').text(data['disk_free'] + 'GB');
})