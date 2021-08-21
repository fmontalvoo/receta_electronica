const formReceta = document.getElementById('formReceta');
formReceta.addEventListener('submit', submit);


async function submit(evt) {
    const path = (location.pathname + location.search).substr(1);

    evt.preventDefault();
    let seleccionados = document.querySelectorAll('input');

    const medicamentos = [];
    for (const medicamento of seleccionados) {
        if (medicamento.checked)
            medicamentos.push(medicamento.id);
    }
    const response = await fetch(`/${path}`,
        {
            method: 'POST',
            body: JSON.stringify({
                medicamentos
            }),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }
    );
    const data = await response.json();
    console.log(data['status'])
    if (data['status'] == 201)
        location.href = '/lista_pacientes'


}