// set the modal menu element
const edit = document.getElementById('editProductModal');
const add = document.getElementById('addProductModal');

// options with default values
const optionsModal = {
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

const editModal = new Modal(edit, optionsModal);
const addModal = new Modal(add, optionsModal);

function toggleEditItem(){
    editModal.toggle();
}
function toggleAddItem(){
    addModal.toggle();
}