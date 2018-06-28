document.addEventListener("DOMContentLoaded", function(event) {

  let date = new Date();
  let year = ('0000' + date.getFullYear()).slice(-4);
  let month = date.getMonth() + 1
  month = ('0' + month).slice(-2);
  let day = ('0' + date.getDate()).slice(-2);

  console.log(year + '-' + month + '-' + day);
  document.getElementById('visit_date').value = year + '-' + month + '-' + day;

  
  const spec_input = document.querySelectorAll("input[name^='spec_'], input[name='clinic']");
  for (input of spec_input) {
    console.log(input)
    const value = localStorage.getItem(input.name);
    if (value) {
      input.value = value;
      input.previousElementSibling.classList.add("active");
    }

    input.addEventListener("change", (event) => {
      localStorage.setItem(event.target.name, event.target.value);
    });
  }

});


