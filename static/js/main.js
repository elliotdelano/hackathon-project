let nameGlobal = []
let satScoresGlobal = []
let schoolGlobal = undefined

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

async function update_progress(status_url, fast) {
    let results = []
    for (let url of status_url) {
        await $.getJSON(url, function (data) {
            if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
                if ('result' in data) {
                    results.push(data.result || 0)
                }
            }
        });
    }
    if (results.length == status_url.length) {
        let data = {
            sents: results,
            sat_rating: fast.sat_rating,
            gpa_rating: fast.gpa_rating,
            ecs_bonus: fast.ec_bonus,
            acceptance_rate: fast.acceptance_rate,
            goat_rating: fast.goat_rating
        }
        $.ajax({
            type: 'POST',
            url: '/compute',
            datatype: 'json',
            data: JSON.stringify(data),
            success: function (info) {
                window.location.href = "/results";

            },
            contentType: 'application/json'
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
    let datas = {
        sat: $('#sat').val(),
        gpa: $('#gpa').val(),
        ec_0: $('#ec_0').val(),
        hr_0: $('#hr_0').val(),
        ec_1: $('#ec_1').val(),
        hr_1: $('#hr_1').val(),
        ec_2: $('#ec_2').val(),
        hr_2: $('#hr_2').val(),
        ec_3: $('#ec_3').val(),
        hr_3: $('#hr_3').val(),
        ec_4: $('#ec_4').val(),
        hr_4: $('#hr_4').val(),
        ec_5: $('#ec_5').val(),
        hr_5: $('#hr_5').val(),
        ec_6: $('#ec_6').val(),
        hr_6: $('#hr_6').val(),
        ec_7: $('#ec_7').val(),
        hr_7: $('#hr_7').val(),
        ec_8: $('#ec_8').val(),
        hr_8: $('#hr_8').val(),
        ec_9: $('#ec_9').val(),
        hr_9: $('#hr_9').val(),
        school: $('#school').val(),
    }

    schoolGlobal = datas.school

    $.ajax({
        type: 'POST',
        url: '/chanceme',
        datatype: 'json',
        data: JSON.stringify(datas),
        success: function (sfgsd) {
            let status_url = sfgsd.ids
            update_progress(status_url, sfgsd)
        },
        contentType: 'application/json'
    });
    // $.post('/chanceme', JSON.stringify(datas), function (sfgsd) {
    //     let status_url = sfgsd.ids
    //     update_progress(status_url, sfgsd)
    // })
}