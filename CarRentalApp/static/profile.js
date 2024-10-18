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
    .catch(error => console.error('Error:', error));
}

function deleteBooking(carModel) {
    fetch('/delete_booking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ car_model: carModel })
    }).then(response => response.json())
      .then(data => {
          alert(data.message);
          location.reload(); // Refresh the page to update the bookings
      })
      .catch(error => console.error('Error:', error));
}
