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
    // const requestOptions = {
    //     method: 'POST',
    //     body: formData
    // };
    // fetch('/ota/image/upload', requestOptions)
    //     .then(response => response.json())
    //     .then(data => {
    //         Swal.hideLoading()
    //         Swal.close()
    //         if (data.success){
    //             Swal.fire({
    //                 title: 'Success',
    //                 text: data.message,
    //                 icon: 'success',
    //                 confirmButtonText: 'OK'
    //             }).then(function(){
    //                 window.location.reload();
    //             })
    //         } else {
    //             Swal.fire({
    //                 title: 'Error',
    //                 text: data.message,
    //                 icon: 'error',
    //                 confirmButtonText: 'OK'
    //             })
    //         }
    //     })
    //     .catch(error => {
    //         Swal.hideLoading()
    //         Swal.close()
    //         Swal.fire({
    //             title: 'Thất bại',
    //             text: error,
    //             icon: 'error',
    //             showConfirmButton: false,
    //             timer: 5000
    //         })
    //     });
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
                title: 'Đang xử lý',
                didOpen: () => {
                    Swal.showLoading()
                },
            })
        }
    })
    })();
})