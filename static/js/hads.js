elements = document.getElementsByTagName('select')

var dict = {};

for (element of elements) {

  element.addEventListener('change', function(element) {

    for (element of document.getElementsByTagName('select')) {

      if (element.selectedIndex === undefined) {
        return
      }

      dict[element.name] = parseInt(element.options[element.selectedIndex].value)

      let sum = 0;
      for (let value of [2,3,6,7,10,11,14]) {
        sum += dict['q' + value];
      }
      document.getElementById('hads_dep').value = sum;

      sum = 0;
      for (let value of [1,4,5,8,9,12,13]) {
        sum += dict['q' + value];
      }
      document.getElementById('hads_anx').value = sum;
    }
  });
}

submit_btn = document.getElementById("submit_btn");
submit_btn.addEventListener("click", () => {

  const form = document.querySelector("form");
  if (form.checkValidity()) {
    submit_btn.classList.add("hidden");
    document.querySelector("div.hidden").classList.remove("hidden");
  }
  document.getElementById("excel_btn").click();
});