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

$(function () {
    $('#start-bg-job').click(start_long_task);
});

function update_progress(status_url, nanobar, status_div) {
    // send GET request to status URL
    $.getJSON(status_url, function (data) {
        // update UI
        //use this to update global vars for current and total
        percent = parseFloat(data['current'] * 100 / data['total']);
        addData(chart, parseFloat(data['current']), parseFloat(data['status']))
        update_boot(percent);
        nanobar.go(percent);
        $(status_div.childNodes[1]).text(percent + '%');
        //use status to extract loss value and update global loss value
        $(status_div.childNodes[2]).text(data['status']);
        $('#boot_status').html("Loss Status: " + data['status']);
        // (closing the tab will continue training, but graph progress will not be saved)
        if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
            if ('result' in data) {
                // show result
                //or update chart.js here, as the values are already updating content asynchronously here
                //perhaps init chart before this code, then call update method in here
                $(status_div.childNodes[3]).text('Result: ' + data['result']);
            }
            else {
                // something unexpected happened
                $(status_div.childNodes[3]).text('Result: ' + data['state']);
            }
        }
        else {
            // rerun in 2 seconds
            setTimeout(function () {
                update_progress(status_url, nanobar, status_div);
            }, 2000);
        }
    });
}

function start_long_task() {
    // add task status elements


    div = $('<div class="progress"><div></div><div>0%</div><div>...</div><div>&nbsp;</div></div>');
    $('#progress').append(div);

    // create a progress bar
    var nanobar = new Nanobar({
        bg: '#B551CA',
        target: div[0].childNodes[0]
    });

    // send ajax POST request to start background job
    $.ajax({
        type: 'POST',
        url: '/longtask',
        success: function (data, status, request) {
            status_url = request.getResponseHeader('Location');
            //console.log(status_url);
            task_id = status_url;
            update_progress(status_url, nanobar, div[0]);
        },
        error: function () {
            alert('Unexpected error');
        }
    });
}