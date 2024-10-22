
function updateDateTime() {
    const dateTimeElement = document.getElementById('datetime');
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
    dateTimeElement.textContent = now.toLocaleDateString('en-US', options);
}

// Function to load cars from cars.txt
async function loadCars() {
    try {
        const response = await fetch('../cars.txt');
        const text = await response.text();
        const lines = text.trim().split('\n');
        const carSections = {
            monthly: document.querySelector('#monthly-rentals .car-listings'),
            twoWeek: document.querySelector('#two-week-rentals .car-listings'),
            weekly: document.querySelector('#weekly-rentals .car-listings')
        };
        
        lines.forEach(line => {
            const [image, name, type, seats, doors, baggage, transmission, mileage, location, price, 
                availability, owner, phone] = line.split('|');
            
            if (!availability) {
                return; // Skip this iteration if availability is undefined
            }

            const carDiv = document.createElement('div');
            carDiv.className = 'car';
            carDiv.innerHTML = 
            `
                <img src="${image}" alt="${name}">
                <h3>${name}</h3>
                <p>${type}</p>
                <p>Seats: ${seats} - Doors: ${doors}</p>
                <p>Baggage: ${baggage} - ${transmission}</p>
                <p>${mileage}</p>
                <p>${location}</p>
                <p>Price for ${availability}: ${price}</p> 
            `;

            // Categorize cars by availability if it exists
            if (availability.includes('month')) {
                carSections.monthly.appendChild(carDiv);
            } else if (availability.includes('two weeks')) {
                carSections.twoWeek.appendChild(carDiv);
            } else {
                carSections.weekly.appendChild(carDiv);
            }
        });
    } catch (error) {
        return;
    }
}

setInterval(updateDateTime, 1000); // Update every second
// Initial call to display the current date and time immediately
updateDateTime();



function searchCars() {
    let input = document.getElementById('carSearch').value.toLowerCase();
    let carCards = document.getElementsByClassName('car-card');

    for (let i = 0; i < carCards.length; i++) {
        let model = carCards[i].querySelector('h3').innerText.toLowerCase();
        if (model.includes(input)) {
            carCards[i].style.display = ''; // Show the card
        } else {
            carCards[i].style.display = 'none'; // Hide the card
        }
    }
}



let showAvailableCars = false;

function toggleFilter() {
    // Get the filter toggle image and label
    const filterToggle = document.getElementById('filterToggle');
    const filterLabel = document.getElementById('filterLabel');

    // Toggle the filter state
    showAvailableCars = !showAvailableCars;

    // Filter the car cards based on the state
    const carCards = document.querySelectorAll('.car-card');

    carCards.forEach(card => {
        const isBooked = card.querySelector('.booked-flag') !== null;
        card.style.display = showAvailableCars && isBooked ? 'none' : 'block'; // Show or hide based on filter state
    });
}




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


































