function storeUsername() {
    const firstName = document.getElementById('first_name').value;
    localStorage.setItem('first_name', firstName);
}
