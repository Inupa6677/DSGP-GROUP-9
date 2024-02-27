window.addEventListener('storage', function(event) {
    // Check if the event is related to the specific key you're interested in
    alert("hello world");
    if (event.key === 'myData') {

        // Retrieve the updated data from local storage
        var storedData = localStorage.getItem('myData');
        var data = JSON.parse(storedData);

        // Update the center of the map based on the new latitude and longitude values
        map_6e83edfb4ac1d51db68b2448762ecd8e.setView([data.latitude, data.longitude]);


}

});

