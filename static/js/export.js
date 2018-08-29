function toExcel(endpoint, type) {
  
  let li = [...document.querySelectorAll("li[data-visit]")];
  li = li.map((elem) => { return Number(elem.dataset.visit) }); 
  
  const form = document.createElement("form"),
        node_type = document.createElement("input"),
        node_id = document.createElement("input"),
        node_patient = document.createElement("input");
        
  form.action = endpoint;
  form.method = "post";

  node_type.value = type;
  node_type.name = "type";
  form.appendChild(node_type.cloneNode());

  node_id.value = li.toString();
  node_id.name = "visits";
  form.appendChild(node_id.cloneNode());

  node_patient.value = document.getElementById("patient_name").textContent + '_' + document.getElementById("patient_birth_date").textContent;
  node_patient.name = "fname";
  form.appendChild(node_patient.cloneNode());

  form.style.display = "none";
  // To be sent, the form needs to be attached to the main document.
  document.body.appendChild(form);

  form.submit();

  // Once the form is sent, remove it.
  document.body.removeChild(form);
}

document.addEventListener("DOMContentLoaded", (event) => {

  const select = document.getElementsByTagName('select')[0]
  select.addEventListener("change", (event) => {
    if (event.target.value !== "") {
      const button = document.querySelector(".export-btn");
      button.classList.remove("disabled");
    } 
  });

});

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM fully loaded and parsed");
    const buttons = document.getElementsByTagName("button");
    for (let button of buttons) {
      button.addEventListener("click", (event) => {
        const select = document.getElementsByTagName('select')[0]
        console.log(select.value);
        toExcel("/to_excel", select.value);
    })

  }
});