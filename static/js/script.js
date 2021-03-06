console.log('canvas saver')

document.addEventListener("DOMContentLoaded", function(event) {
  let elements = document.querySelectorAll('.range_change_event > input');
  console.log(elements)
  for ( elem of elements ) {
    elem.value = "0";
  }
});

function save_screen(form) {

  document.getElementById('excel_btn').style.visibility = 'hidden'

  const range_inputs = document.querySelectorAll('input[type="range"]');
  for (input of range_inputs) {
    input.style.display = "none";
  }

  document.body.scrollTop = 0
  document.body.parentNode.scrollTop = 0

  html2canvas(document.body.firstChild, {
      onrendered: function(canvas) {

          let image = canvas.toDataURL();
          let formData = new FormData(form);

          formData.append("screen", image);

          const name_of_test = document.title.toLowerCase().split(" ").join("_")       

          formData.append( "name_of_test" , name_of_test );

          const request = new XMLHttpRequest();
          request.open("POST", "/screen");

          request.onload = function() {
            form.submit();
          }

          request.send(formData);
      }
  });
}

let elements = document.getElementsByClassName('range_change_event');

for ( elem of elements ) {
  if (elem.classList.contains("to_fixed")) {
    elem.addEventListener("change", (el) => { el.target.parentNode.firstChild.innerHTML = Number(el.target.value).toFixed(1); } )
  } else {
    elem.addEventListener("change", (el) => { el.target.parentNode.firstChild.innerHTML = el.target.value; } )
  }
}

let search = document.getElementById('search')
console.log(search)
if (search !== undefined & search !== null) {
  search.addEventListener('click', (el) => {
    el.preventDefault();
  
    let sname = document.querySelector("#search_form input[name='sname']");
    let fname = document.querySelector("#search_form input[name='fname']");
    let lname = document.querySelector("#search_form input[name='lname']");
    let from_date = document.querySelector("#search_form input[name='from_date']");
    let to_date = document.querySelector("#search_form input[name='to_date']");
  
    (async () => {
      const rawResponse = await fetch( el.target.parentNode.parentNode.parentNode.action , {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({sname: sname.value, fname: fname.value, lname: lname.value, from_date: from_date.value, to_date: to_date.value })
      });
      const visits = await rawResponse.json();
      
      list = document.getElementById('search_results');
      list.innerHTML = '';
  
      for (let [visit,patient,doctor] of visits) {
        
        console.log(visit, patient);

        visit_link = '/visit/' + visit.id; // document.URL
        patient_link = '/patient/' + patient.id

        //console.log(typeof(visit.visit_date), visit.visit_date, Date(visit.visit_date))
  
        let visit_date = new Date(visit.visit_date);
        let birth_date = new Date(patient.birth_date);
  
        //console.log(visit_date)
  
        let test_card = document.createElement('li');
        test_card.classList.add('collection-item', 'row');
        test_card.innerHTML = (`<a href="${ patient_link }" class='col s4'>${ /*visit.id + '. ' +*/ patient.sname + ' ' + patient.fname + ' ' + patient.lname }</a>
                                <span class='col s2 right-align'>${ birth_date.toLocaleDateString('ru-RU') }</span>
                                <!--<a href="${patient_link}" class='col s3'>${ visit.doctor_sname + ' ' + visit.doctor_fname + ' ' + visit.doctor_lname }</a>-->
                                <span class='col s2'>${ visit_date.toLocaleDateString('ru-RU') }</span>
                                  <!--<ul>
                                    <li>Дата рождения: ${ birth_date.toLocaleDateString('ru-RU') }</li>
                                    <li>Пол: ${ patient.sex ? "Мужской" : "Женский" }</li>
                                    <li>ФИО врача: ${ visit.doctor_sname + ' ' + visit.doctor_fname + ' ' + visit.doctor_lname }</li>
                                  </ul>-->
                                <a href="${ visit_link }" class="secondary-content col s4 right-align">Просмотр визита</a>`);
        list.appendChild(test_card);
      }
  
      console.log(visits);
    })();
  });
}


document.addEventListener("DOMContentLoaded", function(event) {

  M.AutoInit();
  
  /*

  let date = new Date();
  let year = ('0000' + date.getFullYear()).slice(-4);
  let month = date.getMonth() + 1
  month = ('0' + month).slice(-2);
  let day = ('0' + date.getDate()).slice(-2);

  console.log(year + '-' + month + '-' + day);
  document.getElementById('visit_date').value = year + '-' + month + '-' + day;

  */
  
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

/*
document.getElementById("screen").addEventListener("click", function(){

  document.body.scrollTop = 0
  document.body.parentNode.scrollTop = 0
  //document.body.scrollIntoView()
  console.log('button clicked')
  html2canvas(document.body, {
      onrendered: function(canvas) {
          var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");  // here is the most important part because if you dont replace you will get a DOM 18 exception.
          var a = document.createElement('a');
          document.body.appendChild(a);
           a.href = image;
           a.download = 'somefilename.png';
           a.click();
      }
  });
});

document.getElementById("test_2").addEventListener("click", function(){
  window.open("{{ url_for('static', 'FSMC') }}", '_blank');
});
*/
