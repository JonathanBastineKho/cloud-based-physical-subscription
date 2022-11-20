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
            var cameraId = devices[devices.length - 1].id;
            // .. use this to start scanning.
            html5QrCode = new Html5Qrcode("scanQR");
            html5QrCode.start(
            cameraId, 
            {fps: 5},
            (decodedText, decodedResult) => {
                html5QrCode.stop();
                var formData = new FormData();
                formData.append("serial_number", decodedText);
                formData.append("csrf_token", document.getElementById("csrf_tok").value);
                loading();
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
    loading();
    submitData(formData2);
}

function loading(){
    $("#scanForm").empty();
    $("#scanForm").append(`
    <div class="grid grid-cols-1 content-center">
        <div role="status" class="place-self-center">
            <svg aria-hidden="true" class="mr-2 w-32 h-32 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
            </svg>
            <span class="sr-only">Loading...</span>
        </div>
        <div class="grid grid-cols-1 content-center mt-4">
            <h3 class="mb-5 text-lg font-normal place-self-center text-gray-500 dark:text-gray-400 w-fit">Please wait for a moment...</h3>
        </div>
    </div>
    `);
}