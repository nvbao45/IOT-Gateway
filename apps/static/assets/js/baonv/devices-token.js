
function deleteDevice(deviceId) {
    deleteRequest('/devices/delete/', deviceId, "device");
}

function showToken(obj){
    const token = obj.dataset.token;
    const id = obj.dataset.id;
    if (obj.dataset.show === "false") {
        $('#token-input-' + id).val(token);
        const icon = obj.querySelector('i');
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        $('#token-input-' + id).val("***********");
        const icon = obj.querySelector('i');
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
    obj.dataset.show = obj.dataset.show == "true" ? "false" : "true";
}

function addDevice(entrypoint){
    const formData = new FormData();
    const queryString = $('#add-device-form').serializeArray();

    queryString.forEach(function(item) {
        formData.append(item.name, item.value);
    });

    addRequest(entrypoint, formData);
}

function editDevice(id){

    fetch('/devices/' + id, {
        method: 'GET',
    })
        .then(data => data.json())
        .then(data =>
        {
            Swal.fire({
                template: '#add-device-template',
                showCancelButton: true,
                showCloseButton: true
            }).then((result) => {
                if (result.isConfirmed){
                    addDevice(`/devices/${id}/edit`);
                    Swal.fire({
                        title: 'Waiting',
                        didOpen: () => {
                            Swal.showLoading()
                        },
                    })
                }
            })
            let hidden_control = document.querySelectorAll('#add-device-form .hidden');
            hidden_control.forEach(function(item){
                item.classList.remove('hidden');
            });

            document.getElementById("name").value = data['device_name'];
            document.getElementById("description").value = data['device_description'];
            document.getElementById("token").value = data['device_token'];
        })
}

$('#btn-add-device').on('click', function(){
    (async () => {
        Swal.fire({
        template: '#add-device-template',
        showCancelButton: true,
        showCloseButton: true
    }).then((result) => {
        if (result.isConfirmed){
            addDevice('/devices/add');
            Swal.fire({
                title: 'Waiting',
                didOpen: () => {
                    Swal.showLoading()
                },
            })
        }
    })
    })();
})