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

function deleteCar(plateNumber) {
    fetch('/delete_car', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ plate_number: plateNumber })  // Use plate_number instead of model
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload(); // Refresh the page
        } else {
            alert(data.message);
        }
    })
    .catch(() => {
        alert('An error occurred while deleting the car.');
    });
}


