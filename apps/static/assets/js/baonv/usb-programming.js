function updateModels() {
    let boardType = document.getElementById("boardtype-select").value;
    let modelSelect = document.getElementById("board-select");
    modelSelect.innerHTML = ""; // Clear existing options

    // Get models from the dataset
    let models = JSON.parse(document.getElementById("boardsData").textContent)[boardType] || [];

    // Populate models in the second dropdown
    models.forEach(model => {
        let option = document.createElement("option");
        option.value = model[1];
        option.textContent = model[0];
        modelSelect.appendChild(option);
    });
}

/**
 * @deprecated This function is deprecated and may be removed in future versions.
 * Use `reconfigUSB` instead for improved functionality and error handling.
 */
function reconfigAction(deviceID) {
    let image = document.getElementById('image-'+deviceID).value;
    let board = document.getElementById('board-select').value;

    let formData = new FormData();
    formData.append('image', image);
    formData.append('board', board);
    formData.append('port', deviceID.replaceAll('_', '/'));

    const requestOptions = {
        method: 'POST',
        body: formData
    };
    fetch('/ota/usbprogramming', requestOptions)
        .then(response => response.json())
        .then(data => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            function read() {
                reader.read().then(({ done, value }) => {
                    if (done) {
                        log.textContent += "\n--- Stream finished ---\n";
                        return;
                    }

                    const chunk = decoder.decode(value, { stream: true });
                    // Parse each SSE line
                    chunk.split("\n\n").forEach(event => {
                        if (event.startsWith("data:")) {
                            const message = event.replace("data: ", "").trim();
                            log.textContent += message + "\n";
                            log.scrollTop = log.scrollHeight;
                        }
                    });

                    read();
                });
            }

            read();

        }).catch(error => {
            Swal.fire({
                title: '<strong>Thất bại</strong>',
                text: 'Có lỗi xảy ra trong quá trình cấu hình thiết bị',
                icon: 'error',
                type: 'error',
                showCancelButton: false,
                focusConfirm: false,
                confirmButtonText: 'Ok',
            });
        });
}

function reconfigUSB(deviceID){
    Swal.fire({
        title: '<strong>Cấu hình thiết bị</strong>',
        template: '#ota-usb-'+deviceID,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel',
    }).then((result) => {
        if (result.isConfirmed){
            let image = document.getElementById('image-'+deviceID).value;
            let board = document.getElementById('board-select').value;
        
            let formData = new FormData();
            formData.append('image', image);
            formData.append('board', board);
            formData.append('port', deviceID.replaceAll('_', '/'));

            const swalInstance = Swal.fire({
                title: 'Uploading...',
                html: '<pre id="swal-log" style="text-align:left; height:300px; overflow:auto; background:#000; color:#0f0; padding:10px; font-family:monospace;"></pre>',
                showConfirmButton: false,
                allowOutsideClick: false, // Disable closing by clicking outside
            });
        
            const logElement = document.getElementById('swal-log');
            let hasError = false;
        
            // Start fetch request to upload
            fetch('/ota/usbprogramming', {
                method: 'POST',
                body: formData
            }).then(response => {
                if (!response.ok) {
                    throw new Error("Server returned " + response.status);
                }
        
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
        
                function read() {
                    reader.read().then(({ done, value }) => {
                        if (done) {
                            logElement.textContent += "\n--- Upload finished ---\n";
                            logElement.scrollTop = logElement.scrollHeight;
                            
                            Swal.update({
                                title: hasError ? 'Upload Failed' : 'Upload Complete',
                                html: logElement.outerHTML,
                                showConfirmButton: true,
                            });
                            return;
                        }
        
                        const chunk = decoder.decode(value, { stream: true });
        
                        chunk.split("\n\n").forEach(event => {
                            if (event.startsWith("data:")) {
                                const message = event.replace("data: ", "").trim();
                                logElement.textContent += message + "\n";
                                logElement.scrollTop = logElement.scrollHeight;
        
                                // Check for error in the message
                                if (/error|failed|exception|not found/i.test(message)) {
                                    hasError = true;
                                }
                            }
                        });
        
                        read();  // Continue reading
                    }).catch(err => {
                        Swal.update({
                            title:'Upload Failed',
                            html: logElement.outerHTML,
                            showConfirmButton: true,
                        });
                    });
                }
        
                read();  // Start reading the response
            }).catch(err => {
                Swal.update({
                    title:'Upload Failed',
                    html: logElement.outerHTML,
                    showConfirmButton: true,
                });
            });
        }
    })
}