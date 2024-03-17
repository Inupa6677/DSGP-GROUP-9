window.addEventListener('message', function(event) {
    // Check origin if needed
    if (event.origin !== 'http://127.0.0.1:8000') return;

    // Parse message data
    var message = event.data;

    // Handle different types of messages
    switch (message.type) {
        case 'coordinates':
            var coordinates = message.data;

            // Ensure coordinates is an object and has numeric keys
            if (typeof coordinates === 'object' && coordinates !== null) {
                // Assign values to variables a and b using the keys
                var a = coordinates[0]; // Assuming this is latitude
                var b = coordinates[1]; // Assuming this is longitude

                // Store the coordinates in localStorage
                localStorage.setItem('latitude', a);
                localStorage.setItem('longitude', b);

                // Retrieve to confirm
                var storedLatitude = localStorage.getItem('latitude');
                var storedLongitude = localStorage.getItem('longitude');

                // Confirm that the values are stored correctly
                if(storedLatitude == a && storedLongitude == b) {
                    alert("Coordinates are successfully stored in localStorage.");
                } else {
                    alert("Failed to store coordinates in localStorage.");
                }
            } else {
                // Alert if coordinates is not an object or is null
                alert("Coordinates is not an object or is null.");
            }
            break; // Add break statement to exit the switch case

        // Add more cases for different message types if needed
    }
});
