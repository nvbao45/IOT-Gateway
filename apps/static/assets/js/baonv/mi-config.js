$(function() {
   prettyPrint();
});

saveConfig = () => {
    let formData = new FormData();
    formData.append('port', $('#port').val());
    formData.append('baudrate', $('#baudrate').val());
    formData.append('timeout', $('#timeout').val());
    formData.append('apn', $('#apn').val());
    formData.append('user', $('#user').val());
    formData.append('pwd', $('#pwd').val());

    const requestOptions = {
        method: 'POST',
        body: formData
    };
    fetch('/mobile-internet/config', requestOptions)
        .then(response => response.json())
        .then(data => {
            if (data.success){
                window.location.reload();
                Swal.fire({
                    title: 'Success',
                    text: data.message,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(function(){

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
            console.log(error)
        });
}

ussd = () => {
    let formData = new FormData();
    formData.append('ussd', $('#ussd').val());

    const requestOptions = {
        method: 'POST',
        body: formData
    };
    fetch('/mobile-internet/ussd', requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch(error => {
            console.log(error)
        });
}

call = () => {
    let formData = new FormData();
    formData.append('number', $('#phone_number').val());
    const requestOptions = {
        method: 'POST',
        body: formData
    };
    Swal.fire({
        title: 'Đang gọi...',
        didOpen: () => {
            Swal.showLoading()
            fetch('/mobile-internet/call', requestOptions)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                })
                .catch(error => {
                    console.log(error)
                });
        },
        didClose() {
            formData.append('hangup', "true");
            fetch('/mobile-internet/call',{method:'POST', body: formData})
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                })
                .catch(error => {
                    console.log(error)
                });
        }
    })
}

prettyPrint = () => {
    try {
        document.getElementById('error').innerText = '';
        let ugly = document.getElementById('post_body').value;
        let obj = JSON.parse(ugly);
        let pretty = JSON.stringify(obj, undefined, 4);
        document.getElementById('post_body').value = pretty;
    } catch (e) {
        document.getElementById('error').innerText = 'Invalid JSON';
    }
}

httpGet = () => {
    let formData = new FormData();
    formData.append('url', $('#get_url').val());
    const requestOptions = {
        method: 'POST',
        body: formData
    };
    Swal.fire({
        title: 'Đang lấy dữ liệu...',
        didOpen: () => {
            Swal.showLoading()
            fetch('/mobile-internet/get', requestOptions)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    Swal.close()
                    Swal.fire({
                        title: 'Success',
                        text: data.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then(function(){
                        let httpResponse = data[4];
                        let results = ''
                        httpResponse.result.forEach(result => {
                            results += result
                        })
                        results.substr(results.indexOf('{'))
                        document.getElementById("get_result").innerHTML = results;
                    })
                })
                .catch(error => {
                    console.log(error)
                    Swal.close()
                    Swal.fire({
                        title: 'Error',
                        text: error.message,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    })
                });
        }
    })
}

httpPost = () => {
    let api_url = 'https://smartcity.uit.edu.vn/api/';
    let post_body = $('#post_body').val();
    let post_url = api_url + $('#post_url').val();
    let formData = new FormData();
    formData.append('body', post_body);
    formData.append('url', post_url);
    const requestOptions = {
        method: 'POST',
        body: formData
    };
    Swal.fire({
        title: 'Đang gửi dữ liệu...',
        didOpen: () => {
            Swal.showLoading()
            fetch('/mobile-internet/post', requestOptions)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    Swal.close()
                    Swal.fire({
                        title: 'Success',
                        text: data.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then(function(){
                        let httpResponse = data[8];
                        let results = ''
                        httpResponse.result.forEach(result => {
                            results += result
                        })
                        results.substr(results.indexOf('{'))
                        document.getElementById("post_result").innerHTML = results;
                    })
                })
                .catch(error => {
                    console.log(error)
                    Swal.close()
                    Swal.fire({
                        title: 'Error',
                        text: error.message,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    })
                });
        }
    })
}

