$(document).ready(function() {
    // Initialize Select2 for all dropdowns with search functionality
    $('#numberOfVehicles').select2({
        placeholder: "Select number of vehicles",
        allowClear: true
    });
    $('#NumberOfCasualties').select2({
        placeholder: "Select number of casualties",
        allowClear: true
    });
    $('#WeatherConditions').select2({
        placeholder: "Select weather conditions",
        allowClear: true
    });
    $('#RoadSurfaceConditions').select2({
        placeholder: "Select road surface conditions",
        allowClear: true
    });
    $('#light_conditions_id').select2({
        placeholder: "Select light conditions",
        allowClear: true
    });
    clearDefaultValues();
});

// Function to clear default values from Select2 dropdowns
function clearDefaultValues() {
    $('#numberOfVehicles').val(null).trigger('change');
    $('#NumberOfCasualties').val(null).trigger('change');
    $('#WeatherConditions').val(null).trigger('change');
    $('#RoadSurfaceConditions').val(null).trigger('change');
    $('#light_conditions_id').val(null).trigger('change');
}