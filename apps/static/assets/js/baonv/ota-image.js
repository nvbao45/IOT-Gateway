function deleteImage(image) {
    deleteRequest('/ota/image/delete/', image, 'image');
}

function upload(){
    const formData = new FormData();
    const queryString = $('#image-upload-form').serializeArray();
    const file = document.getElementById('file').files[0];

    formData.append('file', file);
    queryString.forEach(function(item) {
        formData.append(item.name, item.value);
    });
    addRequest('/ota/image/upload', formData);
}

$('#btn-upload').on('click', function(){
    (async () => {
        Swal.fire({
        template: '#image-upload',
        showCancelButton: true,
        showCloseButton: true
    }).then((result) => {
        if (result.isConfirmed){
            upload(); 
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