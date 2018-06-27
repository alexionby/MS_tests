async function toExcel(endpoint, type) {

  let li = [...document.querySelectorAll("li[data-visit]")];
  console.log(li);
  //li = Array.from(li);
  //console.log(li);
  li = li.map((elem) => { return Number(elem.dataset.visit) }); 
  //console.log(li);

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({"type": type, "visits": li})
  });
  
  if (!res.ok) {
    console.log("No response");
    throw new Error(res.status); // 404
  }

  const data = await res.json();
  return data;
}

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM fully loaded and parsed");

    const buttons = document.getElementsByTagName("button");
    console.log(buttons);

    for (let button of buttons) {
      button.addEventListener("click", (event) => {
        console.log(event.target);
        //event.target.value
        toExcel("/to_excel", event.target.value ).then(data => {

          console.log(data);
          
          const a = document.createElement("a");
          a.href = window.location.origin + '/' + data['path'];
          //a.textContent = "Download";
          a.download = data['type'];
          a.classList.add("hide");
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        }) 
      });
    }
});