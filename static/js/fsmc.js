elements = document.getElementsByTagName('input')

var dict = {};

for (element of elements) {

  element.addEventListener('click', function() {

    let i;
    for (i=1; i<21; i++) {

      checkboxes = document.getElementsByName('q' + i)
      let sum = 0;
      for (checkbox of checkboxes) {
        if ( checkbox.checked == true ) {
          sum += 1;
          dict['q' + i] = parseInt(checkbox.value);
        }
      }
      if ( sum == 0 ) {
        console.log(i)
        return
      }
    }

    console.log('all selected');
    console.log(dict);

    let sum = 0;
    for (let value of [1,4,7,8,11,13,15,17,18,20]) {
      sum += dict['q' + value];
    }
    document.getElementById('fsmc_kog').value = sum;

    sum = 0;
    for (let value of [2,3,5,6,9,10,12,14,16,19]) {
      sum += dict['q' + value];
    }
    document.getElementById('fsmc_mot').value = sum;

    document.getElementById('fsmc_total').value = parseInt(document.getElementById('fsmc_kog').value) + parseInt(document.getElementById('fsmc_mot').value);

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