document.addEventListener("DOMContentLoaded", function(event) {

  document.querySelector("input[name='pasat_correct']").addEventListener("input", function(e) {

    const procent = document.querySelector("input[name='pasat_procent']")
    procent.value = Math.round(Number(e.target.value) / 60 * 100) / 100

  })

});
