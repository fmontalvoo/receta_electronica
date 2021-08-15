const btnDelete= document.querySelectorAll('#btn-delete');
if(btnDelete) {
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if(!confirm('¿Esta seguro de elimiar el  medicamento?')){
        e.preventDefault();
      }
    });
  })
}