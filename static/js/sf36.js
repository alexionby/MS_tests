document.addEventListener("DOMContentLoaded", function(event) {

  function decoder(name, arr = []) {

    let value = document.querySelector('select[name="' + name + '"').value;
    value = parseInt(value);
    
    if (arr.length > 0) {
      return arr[ value - 1];
    } else {
      return value;
    }
  }

  document.getElementById('resultBtn').addEventListener("click", function() {

    console.log( document.querySelectorAll('ol li') );

    let PF = document.querySelectorAll('select[name^="q3"]')
    let PFsum = 0;

    for (elem of PF) {
      PFsum += parseInt( elem.value );
      console.log(PFsum);
    }
    PF = ((PFsum - 10)/20 * 100);

    console.log(PFsum, PF);

    let RP = document.querySelectorAll('select[name^="q4"]');
    let RPsum = 0;

    for (elem of RP) {
      RPsum += parseInt( elem.value );
      console.log(RPsum);
    }

    RP = ((RPsum - 4)/4 * 100);

    let GH1 = decoder("q1", [5, 4.4, 3.4, 2, 1]);
    let GH11a = decoder("q11a");
    let GH11b = decoder("q11b", [5,4,3,2,1]);
    let GH11c = decoder("q11c");
    let GH11d = decoder("q11d", [5,4.4,3.4,2,1]);

    let GHsum = GH1 + GH11a + GH11b + GH11c + GH11d;
    let GH = ((GHsum - 5)/20) * 100;

    let VT9a = decoder("q9a", [6,5,4,3,2,1]);
    let VT9e = decoder("q9e", [6,5,4,3,2,1]);
    let VT9g = decoder("q9g");
    let VT9i = decoder("q9i");

    let VTsum = VT9a + VT9e + VT9g + VT9i;
    let VT = ((VTsum - 4)/20) * 100;

    let SF6 = decoder("q6", [5,4,3,2,1]);
    let SF10 = decoder("q10");

    let SFsum = SF6 + SF10
    let SF = ((SFsum - 2)/8) * 100

    let REsum = 0
    let RE = document.querySelectorAll('select[name^="q5"]');

    for (elem of RE) {
      REsum += parseInt(elem.value);
    }
    RE = ((REsum-3)/3) * 100;

    let MH9d = decoder("q9d", [6,5,4,3,2,1]);
    let MH9h = decoder("q9h", [6,5,4,3,2,1]);
    let MH9b = decoder("q9b");
    let MH9c = decoder("q9c");
    let MH9g = decoder("q9g");

    let MHsum = MH9b + MH9c + MH9d + MH9d + MH9g + MH9h;
    let MH = ((MHsum - 5)/ 25) * 100;

    console.log("MH");
    console.log(MH);

    let BP7 = decoder("q7", [6, 5.4, 4.2, 3.1, 2.2, 1]);
    let BP8 = decoder("q8",  [6, 5, 4, 3, 2, 1]);

    let BP = (((BP7 + BP8) - 2) /10) * 100;

    console.log(PF, RP, BP, GH, VT, SF, RE, MH)

    const PF_Z = (PF - 84.52404)/ 22.89490
    const RP_Z = (RP - 81.19907)/ 33.797290
    const BP_Z = (BP - 75.49196)/ 23.558790
    const GH_Z = (GH - 72.21316)/ 20.16964
    const VT_Z = (VT - 61.05453)/ 20.86942
    const SF_Z = (SF - 83.59753)/ 22.37642
    const RE_Z = (RE - 81.29467)/ 33.02717
    const MH_Z = (MH - 74.84212)/ 18.01189

    document.getElementById("PF").textContent = PF_Z.toFixed(3);
    document.getElementById("RP").textContent = RP_Z.toFixed(3);
    document.getElementById("BP").textContent = BP_Z.toFixed(3);
    document.getElementById("GH").textContent = GH_Z.toFixed(3);
    document.getElementById("VT").textContent = VT_Z.toFixed(3);
    document.getElementById("SF").textContent = SF_Z.toFixed(3);
    document.getElementById("RE").textContent = RE_Z.toFixed(3);
    document.getElementById("MH").textContent = MH_Z.toFixed(3);

    const PHCsum = (PF_Z * 0.42402) + (RP_Z * 0.35119) + (BP_Z * 0.31754) + (SF_Z * - 0.00753) + (MH_Z * -0.22069) + (RE_Z * -0.19206) + (VT_Z * 0.02877) + (GH_Z * 0.24954)
    const PHC = (PHCsum * 10) + 50

    const MHCsum = (PF_Z * -0.22999) + (RP_Z * -0.12329) + (BP_Z * -0.09731) + (SF * 0.26876) + (MH_Z * 0.48581) + (RE_Z * 0.43407) + (VT_Z * 0.23534) + (GH_Z * -0.01571)
    const MHC = (MHCsum * 10) + 50

    document.querySelector("input[name='PHC']").value = PHC.toFixed(3);
    document.querySelector("input[name='MHC']").value = MHC.toFixed(3);

    const form = document.querySelector("form");
    if (form.checkValidity()) {
      document.getElementById('resultBtn').classList.add("hidden");
      document.querySelector("div.hidden").classList.remove("hidden");
    }
    document.getElementById("excel_btn").click();
  })

});
