// set the modal menu element
const edit = document.getElementById('editProductModal');
const add = document.getElementById('addProductModal');

// options with default values
const options = {
  placement: 'bottom-right',
  backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40',
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

const editModal = new Modal(edit, options);
const addModal = new Modal(add, options);

function toggleEditItem(){
    editModal.toggle();
}
function toggleAddItem(){
    addModal.toggle();
}