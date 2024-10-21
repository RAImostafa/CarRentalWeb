async function bookCar(carModel) {
    try {
        const response = await fetch('/book_car', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ car_model: carModel })
        });

        const data = await response.json();
        if (response.ok) {
            // Show success or already booked message based on the response
            if (data.message === 'Car booked successfully') {
                alert("Car booked successfully!");
            } else if (data.message === 'Car is already booked') {
                alert("Car is already booked.");
            }
            
            // Redirect to the homepage after the alert
            window.location.href = "/home";
        } else {
            // Show error message if something went wrong
            alert(data.message || "An error occurred while booking the car.");
        }
    } catch (error) {
        alert("An error occurred. Please try again.");
    }
}


/* home icon*/
document.addEventListener('DOMContentLoaded', function() {
    const homeIcon = document.getElementById('home-icon');
    const homeUrl = homeIcon.getAttribute('data-home-url');
    
    homeIcon.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent the default behavior
        window.location.href = homeUrl; // Use the correct URL route name
    });
});