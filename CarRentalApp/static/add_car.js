// add_car.js

// Function to validate the form before submission
function validateForm(event) {
    event.preventDefault(); // Prevent the default form submission

    const imagePath = document.getElementById('image_path').value;
    const model = document.getElementById('model').value;
    const carType = document.getElementById('car_type').value;
    const seats = document.getElementById('seats').value;
    const doors = document.getElementById('doors').value;
    const bags = document.getElementById('bags').value;
    const transmission = document.getElementById('transmission').value;
    const availability = document.getElementById('availability').value;
    const location = document.getElementById('location').value;
    const price = document.getElementById('price').value;
    const duration = document.getElementById('duration').value;
    const renterName = document.getElementById('renter_name').value;
    const renterPhone = document.getElementById('renter_phone').value;
    const plateNumber = document.getElementById('plate_number').value;

    // Basic validation checks
    if (!imagePath || !model || !carType || !seats || !doors || !bags || 
        !transmission || !availability || !location || !price || 
        !duration || !renterName || !renterPhone || !plateNumber) {
        alert("Please fill in all fields.");
        return;
    }

    // Additional validation can be added here (e.g., phone number format, numeric fields)
    
    // If validation passes, submit the form
    document.querySelector('form').submit();
}

// Event listener for form submission
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.addEventListener('submit', validateForm);
});
