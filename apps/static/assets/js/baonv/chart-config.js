function deviceSelectChange(){
    $("#devices-select").on("change", function(){
        fetch(`/devices/${$(this).val()}/sensors`)
            .then(res => res.json())
            .then(data => {
                $('#sensors-select').empty();
                data.forEach(item => {
                    $('#sensors-select').append(`<option value="${item.sensor}">${item.sensor}</option>`);
                });
            })
    });
}

function deleteChart(id) {
    deleteRequest('/chart/config/delete/', id, 'chart');
}

function addChart(){
    const formData = new FormData();
    const queryString = $('#char-form').serializeArray();

    queryString.forEach(function(item) {
        formData.append(item.name, item.value);
    });
    addRequest('/chart/config/add', formData);
}

function updateChart(id){
    fetch(`/chart/${id}`)
        .then(response => response.json())
        .then(data => {
            Swal.fire({
                template: '#add-chart',
                showCancelButton: true,
                showCloseButton: true
            }).then((result) => {
                if (result.isConfirmed){
                    const formData = new FormData();
                    const queryString = $('#char-form').serializeArray();

                    queryString.forEach(function(item) {
                        formData.append(item.name, item.value);
                    });

                    addRequest(`/chart/config/edit/${id}`, formData);
                    Swal.fire({
                        title: 'Đang xử lý',
                        didOpen: () => {
                            Swal.showLoading()
                        },
                    })
                }
            })

            $('#name').val(data.name);
            $('#devices-select').val(`${data['device_id']}`);
            fetch(`/devices/${data['device_id']}/sensors`)
                .then(res => res.json())
                .then(dt => {
                    $('#sensors-select').empty();
                    dt.forEach(item => {
                        if (data['sensor'] == item['sensor']) {
                            $('#sensors-select').append(`<option value="${item['sensor']}" selected>${item['sensor']}</option>`);
                        } else {
                            $('#sensors-select').append(`<option value="${item['sensor']}">${item['sensor']}</option>`);
                        }
                    });
                });
            $('#samples').val(data['samples']);
            $('#size-select').val(data['size']);
            $('#type-select').val(data['type']);
            $('#color').val(data['color']);
            $('#enable').attr('checked', data['enable']);
        });
}

$('#btn-addchart').on('click', function(){
    Swal.fire({
        template: '#add-chart',
        showCancelButton: true,
        showCloseButton: true
    }).then((result) => {
        if (result.isConfirmed){
            addChart();
            Swal.fire({
                title: 'Đang xử lý',
                didOpen: () => {
                    Swal.showLoading()
                },
            })
        }
    })
    deviceSelectChange();
});

