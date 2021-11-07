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
        let li = document.createElement("li")
        let node = document.createTextNode(name)
        a.appendChild(node)
        li.appendChild(a)
        a.classList.add("dropdown-item", "h6")
        a.onclick = function () { document.getElementById("school").value = name }
        document.getElementById("collegeDropdown").appendChild(li)
    }
};
xhttp.open("GET", "/static/CollegeAdmissionData.tsv", true);
xhttp.send();

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

// $(function () {
//     $('#getResults').click(start_long_task);
// });

function update_progress(status_url, fast) {
    let results = []
    for (let url of status_url) {
        $.getJSON(url, function (data) {
            if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
                if ('result' in data) {
                    results.push(data.result)
                }
            }
        });
    }
    if (results.length == status_url.length) {
        let data = {
            sents: results,
            sat_rating: fast.sat_rating,
            gpa_rating: fast.gpa_rating,
            ec_bonus: fast.ec_bonus,
            acceptance_rate: fast.acceptance_rate,
            goat_rating: fast.goat_rating
        }
        $.ajax({
            type: 'POST',
            url: '/results',
            datatype: 'json',
            data: data
        });
    } else {
        setTimeout(function () {
            update_progress(status_url, fast);
        }, 2000);
    }

}

// function $(str) {
//     return document.getElementById(str)
// }

function start_long_task() {
    // let datas = {
    //     sat: $('#sat').value,
    //     gpa: $('#gpa').value,
    //     ec_0: $('#ec_0').value,
    //     hr_0: $('#hr_0').value,
    //     ec_1: $('#ec_1').value,
    //     hr_1: $('#hr_1').value,
    //     ec_2: $('#ec_2').value,
    //     hr_2: $('#hr_2').value,
    //     ec_3: $('#ec_3').value,
    //     hr_3: $('#hr_3').value,
    //     ec_4: $('#ec_4').value,
    //     hr_4: $('#hr_4').value,
    //     ec_5: $('#ec_5').value,
    //     hr_5: $('#hr_5').value,
    //     ec_6: $('#ec_6').value,
    //     hr_6: $('#hr_6').value,
    //     ec_7: $('#ec_7').value,
    //     hr_7: $('#hr_7').value,
    //     ec_8: $('#ec_8').value,
    //     hr_8: $('#hr_8').value,
    //     ec_9: $('#ec_9').value,
    //     hr_9: $('#hr_9').value,
    //     school: $('#school').value,
    // }

    let datas = {
        sat: 5,
        gpa: 5,
        ec_0: 5,
        hr_0: 5,
        ec_1: 5,
        hr_1: 5,
        ec_2: 5,
        hr_2: 5,
        ec_3: 5,
        hr_3: 5,
        ec_4: 5,
        hr_4: 5,
        ec_5: 5,
        hr_5: 5,
        ec_6: 5,
        hr_6: 5,
        ec_7: 5,
        hr_7: 5,
        ec_8: 5,
        hr_8: 5,
        ec_9: 5,
        hr_9: 5,
        school: 5,
    }

    console.log(datas)

    $.ajax({
        type: 'POST',
        url: '/chanceme',
        datatype: 'json',
        success: function (sfgsd) {
            let status_url = sfgsd.ids
            update_progress(status_url, sfgsd)
        },
        data: datas
    });
}