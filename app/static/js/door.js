// set the modal menu element
var edit, add, editModal, addModal, addModal2;

// options with default values
optionsModalDoor = {
  placement: 'bottom-right',
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

async function toggleEditItem(){
    // Inject Modal
    if (!$('#editProductModal').length){
        await fetch('/dashboard_content/editProductModal')
        .then(function(response){
            return response.text();
        }).then(function(html){
            $(html).insertAfter("#productPage");
            edit = document.getElementById('editProductModal');
            editModal = new Modal(edit, optionsModalDoor);
        });
    }
    editModal.toggle();
}
async function openAddItem(){
    // Inject Modal
    if (!$('#addProductModal').length){
        await fetch('/dashboard_content/addProductModal')
        .then(function(response){
            return response.text();
        }).then(function(html){
            $(html).insertAfter("#productPage");
            add = document.getElementById('addProductModal');
            addModal = new Modal(add, optionsModalDoor);
        });
    }
    addModal.show();
}
function closeAddItem(){
    addModal.hide();
    $("#addProductModal").remove();
}