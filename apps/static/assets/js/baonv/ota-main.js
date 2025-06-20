function reconfigAction(deviceID) {
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
                    title: '<strong>Success</strong>',
                    text: data.message,
                    icon: 'success',
                    type: 'success',
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonText: 'Ok',
                });
            } else {
                Swal.fire({
                    title: '<strong>Failed</strong>',
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
        title: '<strong>Firmware Upload</strong>',
        template: '#ota-'+deviceID,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel',
    }).then((result) => {
        if (result.isConfirmed){
            let image = document.getElementById('image-'+deviceID).value;
            let formData = new FormData();
            formData.append('image', image);
            formData.append('deviceID', deviceID);

            const swalInstance = Swal.fire({
                title: 'Uploading...',
                html: '<pre id="swal-log" style="text-align:left; height:300px; overflow:auto; background:#000; color:#0f0; padding:10px; font-family:monospace;"></pre>',
                showConfirmButton: false,
                allowOutsideClick: false, // Disable closing by clicking outside
            });
        
            const logElement = document.getElementById('swal-log');
            let hasError = false;
        
            // Start fetch request to upload
            fetch('/ota/reconfig', {
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
