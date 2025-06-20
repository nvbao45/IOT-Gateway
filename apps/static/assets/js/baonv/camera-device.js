function addDevice(entrypoint){
    const formData = new FormData();
    const queryString = $('#add-camera-form').serializeArray();

    queryString.forEach(function(item) {
        console.log(item);
        formData.append(item.name, item.value);
    });

    addRequest(entrypoint, formData);
}

function formInputChanged(){
    const addressInput = document.getElementById('ip_address');
    const protocolInput = document.getElementById('protocol');
    const portInput = document.getElementById('port');
    const streamPathInput = document.getElementById('stream_path');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const streamUriSpan = document.getElementById('stream_uri');
    const streamUriAlert = document.getElementById('stream_uri_alert');
    const streamUriInput = document.getElementById('uri');

    function updateStreamUri() {
        const protocol = protocolInput.value || '';
        const address = addressInput.value || '';
        const port = portInput.value || '';
        const streamPath = streamPathInput.value || '';
        const username = usernameInput?.value || '';
        const password = passwordInput?.value || '';

        let auth = '';
        if (username && password) {
            auth = `${encodeURIComponent(username)}:${encodeURIComponent(password)}@`;
        }

        let uri = '';
        if (protocol && address) {
            uri = `${protocol}://${auth}${address}`;
            if (port) {
                uri += `:${port}`;
            }
            if (streamPath) {
                uri += streamPath.startsWith('/') ? streamPath : `/${streamPath}`;
            }
        } 

        if (uri === '') {
            streamUriAlert.classList.add('hidden');
        }
        else {
            streamUriAlert.classList.remove('hidden');
        }

        streamUriSpan.textContent = uri;
        streamUriInput.value = uri;
    }

    // Attach listeners AFTER Swal opens
    [addressInput, protocolInput, portInput, streamPathInput, usernameInput, passwordInput].forEach(input => {
        if (input) {
            input.addEventListener('input', updateStreamUri);
        }
    });
}

function editCamera(id){
    fetch('/devices/camera/' + id, {
        method: 'GET',
    })
        .then(data => data.json())
        .then(data =>
        {
            Swal.fire({
                template: '#add-camera-template',
                showCancelButton: true,
                title: "Sửa camera",
                didOpen: formInputChanged,
                showCloseButton: true
            }).then((result) => {
                if (result.isConfirmed){
                    addDevice(`/devices/camera/edit/${id}`);
                    Swal.fire({
                        title: 'Waiting',
                        didOpen: () => {
                            Swal.showLoading()
                        },
                    })
                }
            });

            const form = document.getElementById('add-camera-form');
            let hasAuth = false;
            form.querySelectorAll('input, select, textarea').forEach(function(item){
                if (item.name in data){
                    item.value = data[item.name];
                    console.log(item.name, data[item.name]);
                    if ((item.name == "username" || item.name == "password") && data[item.name] != ""){
                        hasAuth = true;
                        item.parentElement.parentElement.classList.remove('hidden');
                    }
                }
            });
            if (hasAuth){
                form.querySelector('input[name="auth"]').checked = true;
            };
        })
}

function deleteCamera(id){
    deleteRequest(`/devices/camera/delete/`, id, 'camera');
}

function showCamera(id){
    console.log(id);
}


showAuthForm = function(checkbox){
    const authForms = document.querySelectorAll(".auth-form");
    if (checkbox.checked){
        authForms.forEach(function(item){
            item.classList.remove('hidden');
        });
    } else {
        authForms.forEach(function(item){
            item.classList.add('hidden');
        });
    }
}

$('#btn-add-camera').on('click', function(){
    (async () => {
        Swal.fire({
            template: '#add-camera-template',
            showCancelButton: true, 
            showCloseButton: true,
            didOpen: formInputChanged
        }).then((result) => {
            if (result.isConfirmed){
                addDevice('/devices/camera/add');
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
