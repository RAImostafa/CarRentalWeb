async function bookCar(plateNumber) {
    try {
        const response = await fetch('/book_car', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ plate_number: plateNumber }) // Use plate_number instead of car_model
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

