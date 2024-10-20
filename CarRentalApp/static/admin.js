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

function deleteCar(model) {
   fetch('/delete_car', {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json',
       },
       body: JSON.stringify({ model: model })
   })
   .then(response => response.json())
   .then(data => {
       if (data.success) {
           alert(data.message);
           location.reload(); // Refreshes the page
       } else {
           alert(data.message);
       }
   })
   .catch(error => console.error('Error:', error));
}







