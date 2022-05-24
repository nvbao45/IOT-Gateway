function reconfigAction(deviceID) {
    console.log(deviceID)
    let image = document.getElementById('image-'+deviceID).value;
    let formData = new FormData();
    formData.append('image', image);
    formData.append('deviceID', deviceID);
    const requestOptions = {
        method: 'POST',
        body: formData
    };
    fetch('/ota/reconfig', requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.success === true){
                Swal.fire({
                    title: '<strong>Thành công</strong>',
                    text: data.message,
                    icon: 'success',
                    type: 'success',
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonText: 'Ok',
                });
            } else {
                Swal.fire({
                    title: '<strong>Thất bại</strong>',
                    text: data.message,
                    icon: 'error',
                    type: 'error',
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonText: 'Ok',
                });
            }
        })
}

function reconfig(deviceID){
    Swal.fire({
        title: '<strong>Cấu hình thiết bị</strong>',
        template: '#ota-'+deviceID,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel',
    }).then((result) => {
        if (result.isConfirmed){
            reconfigAction(deviceID);
            Swal.fire({
                title: 'Đang xử lý',
                didOpen: () => {
                    Swal.showLoading()
                },
            })

        }
    })
}