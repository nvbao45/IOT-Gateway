function showUSBDevices(data) {
    const parsedData = JSON.parse(data);
    const usbDevices = parsedData.devices;
    const boards = parsedData.boards;
    const boardsData = document.getElementById("boardsData");
    const usbDevicesTable = document.getElementById('usb-devices-table');
    const usbDevicesBody = usbDevicesTable.querySelector('tbody');
    boardsData.textContent = JSON.stringify(boards);
    usbDevicesBody.innerHTML = ''; // Clear existing rows
    usbDevices.forEach((usb) => {
        const row = document.createElement('tr');

        // Add USB device details
        Object.keys(usb).forEach((key) => {
            const cell = document.createElement('td');
            cell.textContent = usb[key];
            row.appendChild(cell);
        });

        // Add action buttons and template
        const actionCell = document.createElement('td');
        actionCell.innerHTML = `
            <button type="button" onclick="reconfigUSB('${usb.device.replace(/\//g, '_')}')"
                    class="btn btn-icon btn-small-icon btn-border btn-round btn-info"
                    id="reconfig-btn">
                <i class="fas fa-code"></i>
            </button>
            <template id="ota-usb-${usb.device.replace(/\//g, '_')}">
                <swal-html>
                    <div class="col-md-12 form-group form-inline">
                        <label class="col-md-3 col-form-label">Port</label>
                        <div class="col-md-9">${usb.device}</div>
                    </div>
                    <div class="col-md-12 form-group form-inline">
                        <label class="col-md-3 col-form-label">Thiết bị</label>
                        <div class="col-md-9 p-0">
                            <select id="boardtype-select" name="boardtype" onchange="updateModels()" class="form-control input-full">
                                <option value="">Board Type</option>
                                ${Object.keys(boards).map(boardType => `<option value="${boardType}">${boardType}</option>`).join('')}
                            </select>
                        </div>
                    </div>
                    <div class="col-md-12 form-group form-inline">
                        <label class="col-md-3 col-form-label">Thiết bị</label>
                        <div class="col-md-9 p-0">
                            <select id="board-select" name="board" class="form-control input-full">
                                <option value="">Board Model</option>
                                ${boards[Object.keys(boards)[0]].map(board => `<option value="${board[1]}">${board[0]}</option>`).join('')}
                            </select>
                        </div>
                    </div>
                    <div class="col-md-12 form-group form-inline">
                        <label class="col-md-3 col-form-label">Chọn image</label>
                        <div class="col-md-9 p-0">
                            <select class="form-control input-full" id="image-${usb.device.replace(/\//g, '_')}">
                                ${parsedData.images ? parsedData.images.map(image => `
                                    <option value="${image.id}" title="${image.image_description}">
                                        ${image.image_name} - (${image.image_version})
                                    </option>`).join('') : ''}
                            </select>
                        </div>
                    </div>
                </swal-html>
            </template>
        `;
        row.appendChild(actionCell);

        usbDevicesBody.appendChild(row);
    });
}

function showWifiDevices(data) {
    const parsedData = JSON.parse(data);
    const networkDevices = parsedData.devices;
    const networkDevicesTable = document.getElementById('network-devices-table');
    const networkDevicesBody = networkDevicesTable.querySelector('tbody');
    networkDevicesBody.innerHTML = ''; // Clear existing rows

    networkDevices.forEach((network) => {
        const row = document.createElement('tr');

        // Add network device details
        Object.keys(network).forEach((key) => {
            const cell = document.createElement('td');
            cell.textContent = network[key];
            row.appendChild(cell);
        });

        // Add action buttons and template
        const actionCell = document.createElement('td');
        actionCell.innerHTML = `
            <button type="button" onclick="reconfig('${network.ip.replace(/\./g, '-')}')"
                    class="btn btn-icon btn-small-icon btn-border btn-round btn-info"
                    id="reconfig-btn">
                <i class="fas fa-code"></i>
            </button>
            <template id="ota-${network.ip.replace(/\./g, '-')}">
                <swal-html>
                    <ul class="list-group mt-3">
                        <li class="list-group-item list-group-item-light">Host Name: ${network.hostname}</li>
                        <li class="list-group-item list-group-item-light">Địa chỉ IP: ${network.ip}</li>
                        <li class="list-group-item list-group-item-light">Port: ${network.port}</li>
                        <li class="list-group-item list-group-item-light">TCP Check: ${network.tcp_check}</li>
                        <li class="list-group-item list-group-item-light">SSH Upload: ${network.ssh_upload}</li>
                        <li class="list-group-item list-group-item-light">Board: ${network.board}</li>
                        <li class="list-group-item list-group-item-light">Auth Upload: ${network.auth_upload}</li>
                    </ul>
                    <div class="mt-3">
                        <b>Chọn image mới</b>
                        <div class="form-group">
                            <select class="form-control" id="image-${network.ip.replace(/\./g, '-')}">
                                ${parsedData.images ? parsedData.images.map(image => `
                                    <option value="${image.id}">
                                        ${image.image_name} - (${image.image_version})
                                    </option>`).join('') : ''}
                            </select>
                        </div>
                    </div>
                </swal-html>
            </template>
        `;
        row.appendChild(actionCell);

        networkDevicesBody.appendChild(row);
    });
}

(function (){
    let socket;

    var deviceType = "";
    var board = {};

    if (location.pathname.includes("usb")){
        deviceType = "usb";
    } else {
        deviceType = "network";
    }

    if (location.protocol === 'http:') {
        socket = new WebSocket('ws://' + location.host +
                                                `/ota/devices/${deviceType}`);
    } else {
        socket = new WebSocket('wss://' + location.host +
                                                `/ota/devices/${deviceType}`);
    }
    socket.addEventListener('message', ev => {
        if (location.pathname.includes("usb")){
            showUSBDevices(ev.data);
        } else {
            showWifiDevices(ev.data);
        }
    })
})();
