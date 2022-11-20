optionsModalSettings = {
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

editPW = document.getElementById('PhonepassPW-modal');
editID = document.getElementById('PhonepassID-modal')
editPWModal = new Modal(editPW, optionsModalSettings);
editIDModal = new Modal(editID, optionsModalSettings);

function togglePW(){
    editPWModal.toggle();
}
function toggleID(){
    editIDModal.toggle();
}

modals = {
    "PhonepassID-modal" : toggleID,
    "PhonepassPW-modal" : togglePW
}

async function postEditSettings(event){
    event.preventDefault();
    var formData = new FormData(event.target);
    var url = $(`#${event.target.id}`).attr("action");
    var modal = $(`#${event.target.id}`).attr("modal");
    await fetch(url, {
        method: 'POST',
        body: formData
    }).then(async function(res){
        modals[modal]();
        if (res.ok){
            console.log("ok");
            $("#toast-success").fadeIn(1000);
            $("#toast-success").css('display', 'flex');
            await sleep(5000);
            $("#toast-success").fadeOut(1000);
        } else{
            console.log("false");
        }
    });
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function closeToast(){
    $("#toast-success").fadeOut(1000);
}