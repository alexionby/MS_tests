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

/*
document.getElementById("screen").addEventListener("click", function(){

  document.body.scrollTop = 0
  document.body.parentNode.scrollTop = 0
  html2canvas(document.body, {
      onrendered: function(canvas) {

          var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
          var a = document.createElement('a');
          document.body.appendChild(a);
           a.href = image;
           let filename = document.getElementsByName('fname')[0].value + '_' + document.getElementsByName('visit_date')[0].value + '.png';
           a.download = filename;
           a.click();


          let image = canvas.toDataURL();
          let filledForm = document.forms.mainForm;
          let formData = new FormData(filledForm);
          formData.append("screen", image);
          formData.append("screen_name", "test_name.png")

          var request = new XMLHttpRequest();
          request.open("POST", "/screen");
          request.send(formData);
      }
  });
});*/
