document.addEventListener("DOMContentLoaded", function(event) {

    document.getElementById('VS_mark').addEventListener("change", function(e) {

        if ( e.target.value < 1 || e.target.value > 6 ) {
            alert("Значение должно быть от 1 до 6!");
            e.target.value = "";
            e.target.parentElement.nextElementSibling.firstChild.value = "";
        } else {
            const arr = [1,2,2,3,3,4];
            e.target.parentElement.nextElementSibling.firstChild.value = arr[e.target.value - 1];
        }
    });

    document.getElementById('FS_mark').addEventListener("change", function(e) {

        if ( e.target.value < 1 || e.target.value > 6 ) {
            alert("Значение должно быть от 1 до 6!");
            e.target.value = "";
            e.target.parentElement.nextElementSibling.firstChild.value = "";
        } else {
            const arr = [1,2,3,3,4,5];
            e.target.parentElement.nextElementSibling.firstChild.value = arr[e.target.value - 1];
        }
    });

    document.getElementsByName("edss_step")[0].addEventListener("change", function(e) {

        if (e.target.value < 0 || e.target.value > 10 || isNaN(e.target.value)) {
            e.target.value = "";
        } else {
            const inv = 1.0 / 0.5;
            e.target.value = Math.round(e.target.value * inv) / inv;
        }
    
    });

    for (let elem of document.querySelectorAll("input[type='range']")) {
        elem.addEventListener('focus', function(e) {
            e.target.parentElement.style.background = 'aquamarine';
        });

        elem.addEventListener('blur', function(e) {
            e.target.parentElement.style.background = '';
        });
    }

    
    let elements = document.getElementsByClassName('edss_change_event');

    for ( elem of elements ) {
        elem.addEventListener("change", (el) => { el.target.parentNode.nextElementSibling.innerHTML = Number(el.target.value).toFixed(1); } )
    }


});