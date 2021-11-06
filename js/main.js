let nameGlobal = []
let satScoresGlobal = []

let xhttp = new XMLHttpRequest()
xhttp.onreadystatechange = function () {
    nameGlobal = []
    satScoresGlobal = []
    if (xhttp.readyState == 4 && xhttp.status == 200) {
        var arrayWithValues = xhttp.responseText.trim().split('\n');
        for (let arrayThing of arrayWithValues) {
            let parts = arrayThing.split('\t')
            nameGlobal.push(parts[0])
            satScoresGlobal.push(parts[1].split('\r')[0])
        }
        console.log(nameGlobal, satScoresGlobal);
    };

    for (let name of nameGlobal) {
        let a = document.createElement("a")
        let node = document.createTextNode(name)
        a.appendChild(node)

        document.getElementById("collegeDropdown").appendChild(a)
    }
};
xhttp.open("GET", "/../Static/CollegeAdmissionData.tsv", true);
xhttp.send();

function myFunction() {
    document.getElementById("collegeDropdown").classList.toggle("show");
}

function filterFunction() {
    var input, filter, a, i;
    input = document.getElementById("collegeInputField");
    filter = input.value.toUpperCase();
    div = document.getElementById("collegeDropdown");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}