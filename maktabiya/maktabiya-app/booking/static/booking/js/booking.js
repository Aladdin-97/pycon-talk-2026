today = new Date();
flatpickr("#datepicker", {
    allowInput: true,
    minDate: today,
    maxDate: today.fp_incr(28),// 28 days from now 
    weekNumbers: true,
    disable: [
        // only monday to friday clickable
        function (date) {
            // return true to disable
            return (date.getDay() === 0 || date.getDay() === 6);

        }
    ],
    locale: {
        "firstDayOfWeek": 1 // start week on Monday
    }
});

modal = new bootstrap.Modal(document.getElementById('confirm-booking'))
// htmx.on("booked", (e) => {
//     console.log(e)
//     successMsg = e.detail.msg;
//     $(".alert").html(successMsg);
//     $("#liveToast").toast("show");
//     location.re
// });
htmx.on('htmx:afterSwap', function (e) {
    if (e.detail.target.id == 'dialog') {
        modal.show()
    }
})

htmx.on("htmx:beforeSwap", (e) => {
    if (e.target.id === "dialog" && !e.detail.xhr.response) {
        modal.hide();
    }
});

htmx.on("htmx:beforeSend", (e) => {
    if (e.target.id == 'book-form') {
        //console.log(e.target)
        $("#book-btn").attr('disabled', true);
        $("#book-btn span").removeClass('d-none')
    }
})

// sqrt((x1-x2)


// My Bookings Custom Calender for filter bookings list without limit 
flatpickr("#filter-datepicker", {
    allowInput: true,
    weekNumbers: true,
    disable: [
        // only monday to friday clickable
        function (date) {
            // return true to disable
            return (date.getDay() === 0 || date.getDay() === 6);

        }
    ],
    locale: {
        "firstDayOfWeek": 1 // start week on Monday
    }
});

function validateForm() {
    const checkboxes = document.querySelectorAll('input[name="booking_ids[]"]');
    let isChecked = false;

    checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            isChecked = true;
            return;
        }
    });

    if (!isChecked) {
        alert("Please select at least one item before deleting.");
        return false;
    }

    return true;
}