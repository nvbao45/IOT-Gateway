
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

function addDevice(){
    const formData = new FormData();
    const queryString = $('#add-device-form').serializeArray();

    queryString.forEach(function(item) {
        formData.append(item.name, item.value);
    });

    addRequest('/devices/add', formData);
}

$('#btn-add-device').on('click', function(){
    (async () => {
        Swal.fire({
        template: '#add-device-template',
        showCancelButton: true,
        showCloseButton: true
    }).then((result) => {
        if (result.isConfirmed){
            addDevice();
            Swal.fire({
                title: 'Đang xử lý',
                didOpen: () => {
                    Swal.showLoading()
                },
            })
        }
    })
    })();
})