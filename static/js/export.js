function toExcel(endpoint, type) {
  let li = [...document.querySelectorAll("li[data-visit]")];
  li = li.map((elem) => { return Number(elem.dataset.visit) }); 
  
  const form = document.createElement("form"),
        node_type = document.createElement("input");
        node_id = document.createElement("input");
  
  form.action = endpoint;
  form.method = "post";

  node_type.value = type;
  node_type.name = "type";
  form.appendChild(node_type.cloneNode());

  node_id.value = li.toString();
  node_id.name = "visits";
  form.appendChild(node_id.cloneNode());

  form.style.display = "none";
  // To be sent, the form needs to be attached to the main document.
  document.body.appendChild(form);

  form.submit();

  // Once the form is sent, remove it.
  document.body.removeChild(form);
}

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM fully loaded and parsed");
    const buttons = document.getElementsByTagName("button");
    for (let button of buttons) {
      button.addEventListener("click", (event) => {
        toExcel("/to_excel", event.target.value);
    })
  }
});