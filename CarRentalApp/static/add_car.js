// Function to validate the form before submission
function validateForm() {
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
    if (parseFloat(price) <= 1000) {
        alert("Price must be more than three digits.");
        return;
    }

    // Validate phone number (should be 11 digits, start with 0, no letters)
    if (!/^[0]\d{10}$/.test(renterPhone)) {
        alert("Phone number must be 11 digits and start with 0, with no letters.");
        return;
    }

    document.querySelector('form').submit();
}
