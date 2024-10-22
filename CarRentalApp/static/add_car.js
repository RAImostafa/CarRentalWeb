// Function to validate the form before submission

function validateForm() {
    event.preventDefault(); // Prevent the default form submission
    const imagePath = document.getElementById('image_path').value;
    const model = document.getElementById('model').value;
    const carType = document.getElementById('car_type').value;
    const seats = document.getElementById('seats').value;
    const doors = document.getElementById('doors').value;
    const bags = document.getElementById('bags').value;
    const transmission = document.getElementById('transmission').value;
    const location = document.getElementById('location').value;
    const price = document.getElementById('price').value;
    const duration = document.getElementById('duration').value;
    const renterName = document.getElementById('renter_name').value;
    const renterPhone = document.getElementById('renter_phone').value;
    const plateNumber = document.getElementById('plate_number').value;

    // Basic validation checks
    if (!imagePath || !model || !carType || !seats || !doors || !bags || 
        !transmission || !location || !price || 
        !duration || !renterName || !renterPhone || !plateNumber) {
        alert("Please fill in all fields.");
        return;
    }

    // Validate plate number (should be 5 digits)
    if (!/^\d{5}$/.test(plateNumber)) {
        alert("Plate number must be exactly 5 digits.");
        return;
    }

    // Validate price (should be a positive number)
    if (parseFloat(price) <= 0) {
        alert("Price must be a positive number.");
        return;
    }

    document.querySelector('form').submit();
}

