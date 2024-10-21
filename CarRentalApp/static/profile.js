/* home icon*/
document.addEventListener('DOMContentLoaded', function() {
    const homeIcon = document.getElementById('home-icon');
    const homeUrl = homeIcon.getAttribute('data-home-url');
    
    homeIcon.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent the default behavior
        window.location.href = homeUrl; // Use the correct URL route name
    });
});

function signOut() {
    fetch('/sign_out', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            alert('Sign out failed.');
        }
    })
    .catch(() => {
        alert('An error occurred while signing out.');
    });
}

function deleteBooking(carModel) {
    fetch('/delete_booking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ car_model: carModel })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload(); // Refresh the page to update the bookings
    })
    .catch(() => {
        alert('An error occurred while deleting the booking.');
    });
}

