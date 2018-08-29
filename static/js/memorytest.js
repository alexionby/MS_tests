document.addEventListener("DOMContentLoaded", function(event) {

  let test_table = document.getElementById('test_part')
  let test_arr = [ 1,5,2,1,3,6,2,4,1,6,2,1,6,1,2,4,6,1,2,5,6,3,4,1,2,6,9,4,3,8,4,3,7,8,1,3,7,4,8,5,2,9,
     3,4,7,2,4,5,1,6,4,1,5,6,7,9,8,3,6,4,2,5,8,3,6,7,4,5,2,3,7,2,9,8,1,6,9,7,2,3,6,
     4,9,1,7,2,5,6,8,4,2,8,7,9,3,7,8,5,1,9,2,1,4,3,6,5,2,1,6,4,2,1,6,9,7,3,5,4,8,9]

  for (let i = 0; i < 8; i+=1) {
    console.log(i)

    let row1 = test_table.insertRow(2*i);
    let row2 = test_table.insertRow(2*i + 1);

    for (let j = 0; j < 15; j+=1) {
      element_index = i * 15 + j

      let cell1 = row1.insertCell(j);
      let cell2 = row2.insertCell(j);
      cell1.innerHTML = "<img src='static/img/symb" + test_arr[element_index] + ".png' />";
      cell2.innerHTML = test_arr[element_index];

      if (element_index === 9) {
        console.log(cell1, cell2);
        cell1.classList.add("right-border");
        cell2.classList.add("right-border");
      }

    }
  }

});


document.addEventListener("DOMContentLoaded", function(event) {

  const input_all = document.querySelector('input[name="memtest_all"]');
  const input_correct =  document.querySelector('input[name="memtest_correct"]');
  const input_wrong = document.querySelector('input[name="memtest_wrong"]');

    /*
    input_all.addEventListener('change', function(event) {
      if (Number(input_correct.value) > 0) {
        input_wrong.value = Number(input_all.value) - Number(input_correct.value);
      } 
      else if (Number(input_wrong.value) > 0) {
        input_correct.value = Number(input_all.value) - Number(input_wrong.value);
      }
    })
    */

    input_wrong.addEventListener('change', function(event) {
      if (Number(input_correct.value) > 0) {
        input_all.value = Number(input_wrong.value) + Number(input_correct.value);
      } 
      else if (Number(input_all.value) > 0) {
        input_correct.value = Number(input_all.value) - Number(input_wrong.value);
      }
    })

});