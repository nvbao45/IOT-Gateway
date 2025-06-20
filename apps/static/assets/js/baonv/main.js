function deleteRequest(endpoint, id, removeId) {
    const url = endpoint + id;
    const data = {
        _method: 'delete'
    };
    Swal.fire({
        title: "Bạn có chắc chắn muốn xóa?",
        showDenyButton: true,
        icon: 'warning',
        confirmButtonText: 'Xóa',
        denyButtonText: 'Hủy',
    }).then((result) => {
        if (result.isConfirmed){
            $.ajax({
                url: url,
                type: 'DELETE',
                data: data,
                success: function(data) {
                    if (data.success){
                        $(`#${removeId}-` + id).remove();
                        Swal.fire({
                            title: 'Success',
                            text: data.message,
                            icon: 'success',
                            confirmButtonText: 'OK'
                        })
                    } else {
                        Swal.fire({
                            title: 'Error',
                            text: data.message,
                            icon: 'error',
                            confirmButtonText: 'OK'
                        })
                    }
                }
            });
        }
    })
}

function addRequest(endpoint, formData) {
    const requestOptions = {
        method: 'POST',
        body: formData
    };
    fetch(endpoint, requestOptions)
        .then(response => response.json())
        .then(data => {
            Swal.hideLoading()
            Swal.close()
            if (data.success){
                Swal.fire({
                    title: 'Success',
                    text: data.message,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(function(){
                    window.location.reload();
                })
            } else {
                Swal.fire({
                    title: 'Error',
                    text: data.message,
                    icon: 'error',
                    confirmButtonText: 'OK'
                })
            }
        })
        .catch(error => {
            Swal.hideLoading()
            Swal.close()
            Swal.fire({
                title: 'Failed',
                text: error,
                icon: 'error',
                showConfirmButton: false,
                timer: 5000
            })
        });
}