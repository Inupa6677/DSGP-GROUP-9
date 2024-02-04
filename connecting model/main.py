from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the model
with open('countpredictionDTFinal.pkl', 'rb') as file:
    best_model = pickle.load(file)

# Mapping for dropdown options to numeric values
dropdown_mapping = {
    'Kensington and Chelsea': 169,
    'Hammersmith and Fulham': 155,
    'Westminster': 398,
    'City of London': 79,
    'Tower Hamlets': 366,
    'Southwark': 327,
    'Hackney': 152,
    'Islington': 180,
    'Camden': 54,
    # Add more mappings as needed
}

month_mapping = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}

Hour_mapping = {
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    '10': 9,
    '11': 10,
    '12': 11,
    '13': 12,
    '14': 13,
    '15': 14,
    '16': 15,
    '17': 16,
    '18': 17,
    '19': 18,
    '20': 19,
    '21': 20,
    '22': 21,
    '23': 22,
    '24': 23,
}

day_of_the_week_mapping = {
    'Friday': 0,
    'Monday': 1,
    'Saturday': 2,
    'Sunday': 3,
    'Thursday': 4,
    'Tuesday': 5,
    'Wednesday': 6,
}

Weather_condition_mapping = {
    'Raining no high winds': 4,
    'Fine no high winds': 1,
    'Snowing no high winds': 6,
    'Fine + high winds': 0,
    'Raining + high winds': 3,
    'Fog or mist': 2,
    'Snowing + high winds': 5,
}

Light_condition_mapping = {
    'Daylight': 4,
    'Darkness - lights lit': 1,
    'Darkness - lighting unknown': 0,
    'Darkness - lights unlit': 2,
    'Darkness - no lighting': 3,
}



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get values from the form
        input_values = [
            month_mapping[request.form['month']],
            Hour_mapping[request.form['Hour of the day']],
            day_of_the_week_mapping[request.form['Day of the week']],
            dropdown_mapping[request.form['District']],  # Map dropdown value to numeric
            Weather_condition_mapping[request.form['Weather conditions']],
            Light_condition_mapping[request.form['Light conditions']],
        ]

        # Make predictions
        predictions = best_model.predict([input_values])

        return render_template('aaa.html', predictions=predictions[0])

    return render_template('aaa.html', predictions=None)

if __name__ == '__main__':
    app.run(debug=True)
