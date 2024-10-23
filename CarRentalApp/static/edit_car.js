function validateEditCarForm() {
    // Get form values
    const imagePath = document.getElementById('image_path').value;
    const model = document.getElementById('model').value;
    const carType = document.getElementById('car_type').value;
    const capacity = document.getElementById('capacity').value;
    const doors = document.getElementById('doors').value;
    const luggage = document.getElementById('luggage').value;
    const transmission = document.getElementById('transmission').value;
    const location = document.getElementById('location').value;
    const price = document.getElementById('price').value;
    const duration = document.getElementById('duration').value;
    const owner = document.getElementById('owner').value;
    const phone = document.getElementById('phone').value;

    // Ensure all required fields are filled
    if (!model || !carType || !capacity || !doors || !luggage || !transmission || !location || 
        !price || !duration || !owner || !phone) {
        alert("Please fill in all required fields.");
        return false;
    }

    // Ensure price is a positive number and at least 4 digits
    if (parseFloat(price) < 1000) {
        alert("Price must be at least four digits and positive number.");
        return false;
    }

    // Validate phone number (should be 11 digits, start with 0, no letters)
    if (!/^[0]\d{10}$/.test(phone)) {
        alert("Phone number must be 11 digits and start with 0, with no letters and positive!.");
        return false;
    }

    // If validation passes, submit the form
    document.querySelector('form').submit();
}
