var scanModal, html5QrCode;
optionsModalScan = {
    placement: 'center-center',
    backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-50',
    onHide: () => {
        console.log('modal is hidden');
    },
    onShow: () => {
        console.log('modal is shown');
    },
    onToggle: () => {
        console.log('modal has been toggled');
    }
};

async function openScanModal(){
    await fetch("/index_content/scan")
    .then(function(response){
        return response.text();
    }).then(function(html){
        $(html).insertAfter("#mainNavBar");
        scanModal = new Modal(document.getElementById("scanModal"), openScanModal);
        scanModal.show();
    });
    Html5Qrcode.getCameras().then(devices => {
        if (devices && devices.length) {
            var cameraId = devices[0].id;
            // .. use this to start scanning.
            html5QrCode = new Html5Qrcode("scanQR");
            html5QrCode.start(
            cameraId, 
            {
                fps: 10   // Optional, frame per seconds for qr code scanning
                // qrbox: { width: 250, height: 250 }  // Optional, if you want bounded box UI
            },
            (decodedText, decodedResult) => {
                // do something when code is read
                console.log(decodedText);
            },
            (errorMessage) => {
                // parse error, ignore it.
            }).then(() => {
                $("#scanQR video").addClass("rounded-lg");
            });
        }
    })
    .catch((err) => {
        $("#scanQR").append("<p>permission denined</p>");
    });
}

function closeScanModal(){
    scanModal.hide();
    html5QrCode.stop();
    
    $("#scanModal").remove();
}