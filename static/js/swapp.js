function exportReport(exportUrl) {
    let win = window.open(exportUrl);
    win.print();
    setTimeout(function() {win.close()}, 10);
}

function openItemView(item_id) {
    const itemModal = new bootstrap.Modal(document.getElementById('view-item-' + item_id));
    itemModal.toggle()
}

function getTimerStatus(startTimestamp, endTimestamp) {
    let now = new Date();
    let endTime = new Date(endTimestamp);
    let startTime = new Date(startTimestamp);
    let totalDuration = endTime - startTime;
    let currentDuration = now - startTime;
    let remainingDuration = endTime - now;
    let progressPercent = currentDuration * 100 / totalDuration;

    if (remainingDuration < 0) remainingDuration = 0;
    if (progressPercent > 100) progressPercent = 100;

    return {
        "progressPercent": progressPercent,
        "remainingDays": Math.floor(remainingDuration / (1000 * 60 * 60 * 24)), // remaining time / ms in day
        "remainingHours": Math.floor((remainingDuration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)), // remaining time % ms in day / ms in hour
        "remainingMinutes": Math.floor((remainingDuration % (1000 * 60 * 60)) / (1000 * 60)), // remaining time % ms in hour / ms in minute
        "remainingSeconds": Math.floor((remainingDuration % (1000 * 60)) / 1000), // remaining time % ms in minute / ms in sec
    };
}

function refreshEventTimer(event_start_timestamp, event_end_timestamp) {
    let status = getTimerStatus(event_start_timestamp, event_end_timestamp)

    let time_counter = document.getElementById('remaining-time-counter');
    let time_progress = document.getElementById('remaining-time-progress');
    time_counter.innerHTML = "Remaining time until end of event: " + status.remainingDays + " days " + status.remainingHours + "h " + status.remainingMinutes + 'm ' + status.remainingSeconds + "s";
    time_counter.setAttribute('aria-valuenow', status.progressPercent.toString())
    time_progress.style.width = status.progressPercent + "%";

}

function refreshRegTimer(reg_start_timestamp, reg_end_timestamp) {
    let status = getTimerStatus(reg_start_timestamp, reg_end_timestamp)

    let time_counter = document.getElementById('remaining-reg-time-counter');
    let time_progress = document.getElementById('remaining-reg-time-progress');
    time_counter.innerHTML = "Remaining registration time: " + status.remainingDays + " days " + status.remainingHours + "h " + status.remainingMinutes + 'm ' + status.remainingSeconds + "s";
    time_counter.setAttribute('aria-valuenow', status.progressPercent.toString())
    time_progress.style.width = status.progressPercent + "%";
}

function refreshItemsAndRegs(refreshUrl) {
    let items_counter = document.getElementById('sold-items-counter');
    let items_progress = document.getElementById('sold-items-progress');

    let reg_counter = document.getElementById('reg-counter');
    let reg_progress = document.getElementById('reg-progress');

    let newStatus = new XMLHttpRequest();
    newStatus.onreadystatechange = function () {
        if (newStatus.readyState === 4 && newStatus.status === 200) {
            let status = JSON.parse(newStatus.response);
            items_counter.innerHTML = "Sold " + status.sold_items_count + "/" + status.approved_items_count + " items so far, for a total of £" + status.money_collected + " (£" + status.money_earned + " for you)";
            items_progress.style.width = status.items_progress_percent + "%";
            items_progress.setAttribute('aria-valuenow', status.items_progress_percent.toString())

            reg_counter.innerHTML = "Registered sellers: " + status.reg_count + "/" + status.reg_cap;
            reg_progress.style.width = status.reg_progress_percent + '%';
            reg_progress.setAttribute('aria-valuenow', status.reg_progress_percent);
        }
    }
    newStatus.open("GET", refreshUrl, true);
    newStatus.send();
}

// The getCookie function was provided in the official django documentation on CSRF tokens
// (https://docs.djangoproject.com/en/2.2/ref/csrf/)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function deleteItem(item_id) {
    if (confirm('You are about to permanently remove this item. Are you sure?')) {
        document.getElementById("delete-item-"+item_id).submit()
    } else {
        console.log("delete aborted!");
    }
}

function confirmCancel(message) {
    if (!confirm(message)) {
        console.log("delete aborted!");
        return false;
    }
}


function checkInItem(item_id, checkInUrl) {
    let checked_in_indicator = document.getElementById('checked-in-indicator-'+item_id);
    let checked_in_indicator_modal = document.getElementById('checked-in-indicator-modal-'+item_id);
    let checked_in_button = document.getElementById('check-in-button-'+item_id);
    let delete_item_button = document.getElementById('delete-item-btn-'+item_id);
    let edit_item_button = document.getElementById('edit-item-btn-'+item_id);

    let checkIn = new XMLHttpRequest();
    checkIn.onreadystatechange = function () {
        if (checkIn.readyState === 4 && checkIn.status === 200) {
            let response = JSON.parse(checkIn.response);
            if (response.checked_in) {
                checked_in_indicator.innerHTML = "Checked-in: YES";
                checked_in_indicator_modal.innerHTML = "Checked-in: YES";
                checked_in_button.classList.remove('btn-outline-warning');
                checked_in_button.classList.add('btn-warning');
                delete_item_button.classList.add('disabled')
                edit_item_button.classList.add('disabled')
            } else {
                checked_in_indicator.innerHTML = "Checked-in: NO";
                checked_in_indicator_modal.innerHTML = "Checked-in: NO";
                checked_in_button.classList.add('btn-outline-warning');
                checked_in_button.classList.remove('btn-warning');
                delete_item_button.classList.remove('disabled')
                edit_item_button.classList.remove('disabled')
            }
        }
     }
    let csrftoken = getCookie('csrftoken');
    checkIn.open("POST", checkInUrl , true);
    checkIn.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    checkIn.setRequestHeader("X-CSRFToken", csrftoken);
    checkIn.send("item_id="+item_id);
}