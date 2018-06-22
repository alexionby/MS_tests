document.addEventListener("DOMContentLoaded", function(event) {

  let date = new Date();
  let year = ('0000' + date.getFullYear()).slice(-4);
  let month = date.getMonth() + 1
  month = ('0' + month).slice(-2);
  let day = ('0' + date.getDate()).slice(-2);

  console.log(year + '-' + month + '-' + day);
  document.getElementById('visit_date').value = year + '-' + month + '-' + day;

  //M.AutoInit();
});


