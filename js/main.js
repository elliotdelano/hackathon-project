let xhttp = new XMLHttpRequest()
xhttp.onreadystatechange = function () {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
        var arrayWithValues = xhttp.responseText.trim().split('\t');
        console.log(arrayWithValues);
    };
};
xhttp.open("GET", "/../Static/CollegeAdmissionData.tsv", true);
xhttp.send();