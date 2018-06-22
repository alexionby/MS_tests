document.addEventListener("DOMContentLoaded", function(event) {

  let time_try1
  let time_try2

  timer_function("#try1")
  timer_function("#try2")

});

function timer_function(id) {

  document.querySelector(id + " button[name='end']").disabled = true;

  document.querySelector(id + " button[name='end']").addEventListener('click', function() {
    document.querySelector(id + " input").value = ((new Date() - time_try1) / 1000)
    document.querySelector(id + " button[name='end']").disabled = true;
    document.querySelector(id + " button[name='start']").disabled = false;
  })

  document.querySelector(id + " button[name='start']").addEventListener('click', function() {
    time_try1 = new Date()
    document.querySelector(id + " button[name='start']").disabled = true;
    document.querySelector(id + " button[name='end']").disabled = false;
  })
}
