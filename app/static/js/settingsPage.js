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
    }).then(function(res){
        if (res.ok){
            console.log("ok");
        } else{
            console.log("false");
        }
    });
    modals[modal]();
}