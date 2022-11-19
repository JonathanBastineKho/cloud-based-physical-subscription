var scanModal, html5QrCode;

const isValidUrl = urlString=> {
    try { 
        return Boolean(new URL(urlString)); 
    }
    catch(e){ 
        return false; 
    }
}

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
            {fps: 5},
            (decodedText, decodedResult) => {
                html5QrCode.stop();
                var formData = new FormData();
                formData.append("serial_number", decodedText);
                formData.append("csrf_token", document.getElementById("csrf_tok").value)
                submitData(formData);
                return "";
            },
            (errorMessage) => {
                // parse error, ignore it.
            }).then(() => {
                $("#scanQR video").addClass("rounded-lg");
            });
        }
    })
    .catch((err) => {
        $("#scanQR").append("<p class='dark:text-white'>permission denined</p>");
    });
}

function closeScanModal(){
    scanModal.hide();
    html5QrCode.stop();
    $("#scanModal").remove();
}

async function submitData(formData){
    await fetch("/access", {
        method : 'POST',
        body : formData
    }).then(function(res){
        return res.json();
    }).then(function(data){
        if (!data.success){
            fetch("/index_content/scanFail")
            .then(function(res){
                return res.text()
            }).then(function(html){
                $("#scanModalContent").empty();
                $("#scanModalContent").append(html);
                $("#scanMessage").text(`${data.message}`);
            });
        } else {
            fetch("/index_content/scanSuccess")
            .then(function(res){
                return res.text()
            }).then(function(html){
                $("#scanModalContent").empty();
                $("#scanModalContent").append(html);
                $("#scanMessage").text(`${data.message}`);
            });
        }
    });
}
function accessBtn(event){
    event.preventDefault();
    var formData2 = new FormData(event.target);
    submitData(formData2);
}