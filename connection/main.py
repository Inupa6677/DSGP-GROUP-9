from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

# Load  prediction models
with open('countpredictionDTEvaluated.pkl', 'rb') as file:
    best_model = pickle.load(file)

with open('road_surface_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Load the model from the pickle file
with open('accident_severity_model.pkl', 'rb') as f:
    severity_model = pickle.load(f)

# Mapping for dropdown options to numeric values

dropdown_mapping = {'Kensington and Chelsea': 182, 'Hammersmith and Fulham': 155, 'Westminster': 398,
                    'City of London': 79, 'Tower Hamlets': 366, 'Southwark': 327, 'Hackney': 152, 'Islington': 180,
                    'Camden': 54, 'Lambeth': 190, 'Brent': 38, 'Haringey': 157, 'Barnet': 14, 'Ealing': 108,
                    'Richmond upon Thames': 276, 'Waltham Forest': 375, 'Newham': 227, 'London Airport (Heathrow)': 199,
                    'Hillingdon': 170, 'Harrow': 160, 'Hounslow': 173, 'Enfield': 129, 'Redbridge': 268,
                    'Barking and Dagenham': 13, 'Havering': 165, 'Croydon': 93, 'Wandsworth': 376, 'Sutton': 344,
                    'Lewisham': 195, 'Bromley': 45, 'Greenwich': 149, 'Bexley': 23, 'Kingston upon Thames': 187,
                    'Merton': 211, 'South Lakeland': 315, 'Barrow-in-Furness': 16, 'Carlisle': 59, 'Eden': 125,
                    'Allerdale': 3, 'Copeland': 84, 'Blackpool': 27, 'Fylde': 141, 'Lancaster': 191,
                    'Blackburn with Darwen': 26, 'Preston': 265, 'Wyre': 413, 'South Ribble': 320,
                    'West Lancashire': 391, 'Chorley': 77, 'Hyndburn': 175, 'Ribble Valley': 275, 'Pendle': 257,
                    'Rossendale': 280, 'Burnley': 49, 'Wirral': 404, 'Sefton': 296, 'Liverpool': 198, 'Knowsley': 189,
                    'St. Helens': 331, 'Manchester': 205, 'Oldham': 252, 'Salford': 289, 'Bury': 50, 'Rochdale': 278,
                    'Trafford': 367, 'Tameside': 348, 'Stockport': 336, 'Wigan': 400, 'Bolton': 31, 'Chester': 72,
                    'Warrington': 378, 'Halton': 153, 'Macclesfield': 201, 'Crewe and Nantwich': 92, 'Vale Royal': 371,
                    'Congleton': 82, 'Ellesmere Port and Neston': 127, 'Newcastle upon Tyne': 225, 'Sunderland': 342,
                    'North Tyneside': 242, 'Alnwick': 4, 'Wansbeck': 377, 'Blyth Valley': 29, 'Gateshead': 142,
                    'South Tyneside': 324, 'Tynedale': 369, 'Castle Morpeth': 62, 'Berwick-upon-Tweed': 22,
                    'Wear Valley': 384, 'Sedgefield': 294, 'Durham': 107, 'Easington': 109, 'Chester-le-Street': 73,
                    'Derwentside': 101, 'Teesdale': 352, 'Darlington': 95, 'York': 415, 'Scarborough': 292,
                    'Craven': 90, 'Harrogate': 159, 'Hambleton': 154, 'Richmondshire': 277, 'Selby': 297,
                    'Ryedale': 288, 'Leeds': 192, 'Calderdale': 52, 'Bradford': 35, 'Kirklees': 188, 'Wakefield': 373,
                    'Doncaster': 102, 'Rotherham': 282, 'Barnsley': 15, 'Sheffield': 299,
                    'North East Lincolnshire': 234, 'North Lincolnshire': 238, 'East Riding of Yorkshire': 121,
                    'Kingston upon Hull, City of': 186, 'Hartlepool': 162, 'Redcar and Cleveland': 269,
                    'Middlesbrough': 216, 'Stockton-on-Tees': 337, 'Birmingham': 24, 'Wolverhampton': 407,
                    'Walsall': 374, 'Dudley': 104, 'Sandwell': 291, 'Solihull': 305, 'Coventry': 89,
                    'Stoke-on-Trent': 338, 'Stafford': 332, 'Staffordshire Moorlands': 333, 'Newcastle-under-Lyme': 226,
                    'East Staffordshire': 122, 'Cannock Chase': 55, 'South Staffordshire': 323, 'Lichfield': 196,
                    'Tamworth': 349, 'Worcester': 408, 'Wychavon': 411, 'Malvern Hills': 204, 'Wyre Forest': 414,
                    'Bromsgrove': 46, 'Redditch': 270, 'Bridgnorth': 41, 'Herefordshire, County of': 166,
                    'Shrewsbury and Atcham': 302, 'North Shropshire': 240, 'Oswestry': 254, 'South Shropshire': 321,
                    'Telford and Wrekin': 354, 'Stratford-upon-Avon': 339, 'Warwick': 379, 'Rugby': 283,
                    'North Warwickshire': 243, 'Nuneaton and Bedworth': 250, 'Erewash': 132, 'Amber Valley': 5,
                    'Bolsover': 30, 'Derbyshire Dales': 100, 'High Peak': 168, 'North East Derbyshire': 233,
                    'Chesterfield': 74, 'South Derbyshire': 310, 'Derby': 99, 'Mansfield': 206, 'Ashfield': 9,
                    'Newark and Sherwood': 224, 'Bassetlaw': 19, 'Rushcliffe': 285, 'Nottingham': 249, 'Broxtowe': 48,
                    'Gedling': 143, 'South Holland': 313, 'South Kesteven': 314, 'North Kesteven': 236,
                    'East Lindsey': 117, 'West Lindsey': 392, 'Boston': 32, 'Lincoln': 197, 'Leicester': 193,
                    'Harborough': 156, 'Charnwood': 66, 'North West Leicestershire': 244, 'Rutland': 287, 'Blaby': 25,
                    'Hinckley and Bosworth': 171, 'Oadby and Wigston': 251, 'Melton': 208, 'Kettering': 184,
                    'Corby': 85, 'East Northamptonshire': 119, 'Daventry': 97, 'Northampton': 246,
                    'South Northamptonshire': 318, 'Wellingborough': 385, 'South Cambridgeshire': 309, 'Cambridge': 53,
                    'Huntingdonshire': 174, 'Peterborough': 260, 'East Cambridgeshire': 111, 'Fenland': 136,
                    'Breckland': 37, "King's Lynn and West Norfolk": 185, 'Great Yarmouth': 148, 'Broadland': 44,
                    'North Norfolk': 239, 'Norwich': 248, 'South Norfolk': 317, 'Suffolk Coastal': 341,
                    'St. Edmundsbury': 330, 'Ipswich': 177, 'Forest Heath': 139, 'Mid Suffolk': 214, 'Babergh': 12,
                    'Waveney': 381, 'Bedford': 21, 'Mid Bedfordshire': 212, 'Luton': 200, 'South Bedfordshire': 307,
                    'East Hertfordshire': 116, 'North Hertfordshire': 235, 'Welwyn Hatfield': 386, 'Broxbourne': 47,
                    'St. Albans': 329, 'Watford': 380, 'Three Rivers': 360, 'Hertsmere': 167, 'Dacorum': 94,
                    'Stevenage': 334, 'Uttlesford': 370, 'Braintree': 36, 'Colchester': 81, 'Epping Forest': 130,
                    'Chelmsford': 67, 'Harlow': 158, 'Basildon': 17, 'Thurrock': 361, 'Brentwood': 39, 'Maldon': 203,
                    'Tendring': 355, 'Southend-on-Sea': 326, 'Castle Point': 63, 'Rochford': 279, 'Aylesbury Vale': 11,
                    'Wycombe': 412, 'South Bucks': 308, 'Milton Keynes': 218, 'Chiltern': 76, 'Slough': 304,
                    'Cherwell': 69, 'South Oxfordshire': 319, 'Windsor and Maidenhead': 403, 'Vale of White Horse': 372,
                    'West Oxfordshire': 394, 'Oxford': 255, 'West Berkshire': 387, 'Wokingham': 406, 'Reading': 267,
                    'Bracknell Forest': 34, 'Isle of Wight': 179, 'Southampton': 325, 'East Hampshire': 115,
                    'Havant': 164, 'Gosport': 146, 'Fareham': 135, 'Winchester': 402, 'Hart': 161, 'Eastleigh': 124,
                    'Basingstoke and Deane': 18, 'New Forest': 223, 'Portsmouth': 263, 'Test Valley': 356,
                    'Rushmoor': 286, 'Elmbridge': 128, 'Runnymede': 284, 'Guildford': 150, 'Mole Valley': 219,
                    'Spelthorne': 328, 'Epsom and Ewell': 131, 'Reigate and Banstead': 271, 'Woking': 405,
                    'Waverley': 382, 'Surrey Heath': 343, 'Tandridge': 350, 'Medway': 207, 'Dartford': 96,
                    'Gravesham': 147, 'Sevenoaks': 298, 'Dover': 103, 'Shepway': 300, 'Thanet': 358, 'Canterbury': 56,
                    'Tunbridge Wells': 368, 'Swale': 345, 'Ashford': 10, 'Tonbridge and Malling': 362, 'Maidstone': 202,
                    'Brighton and Hove': 42, 'Wealden': 383, 'Mid Sussex': 215, 'Eastbourne': 123, 'Lewes': 194,
                    'Chichester': 75, 'Rother': 281, 'Hastings': 163, 'Crawley': 91, 'Horsham': 172, 'Worthing': 409,
                    'Arun': 8, 'Adur': 2, 'Kerrier': 183, 'Carrick': 61, 'Penwith': 258, 'Restormel': 273,
                    'North Cornwall': 230, 'West Devon': 388, 'Torridge': 365, 'Caradon': 57, 'North Devon': 231,
                    'Exeter': 133, 'East Devon': 112, 'Teignbridge': 353, 'Mid Devon': 213, 'Plymouth': 261,
                    'South Hams': 312, 'Torbay': 363, 'Sedgemoor': 295, 'Bath and North East Somerset': 20,
                    'Mendip': 209, 'Bristol, City of': 43, 'South Gloucestershire': 311, 'West Somerset': 395,
                    'Taunton Deane': 351, 'South Somerset': 322, 'North Somerset': 241, 'Stroud': 340,
                    'Tewkesbury': 357, 'Cheltenham': 68, 'Gloucester': 145, 'Forest of Dean': 140, 'Cotswold': 87,
                    'Salisbury': 290, 'Kennet': 181, 'West Wiltshire': 396, 'North Wiltshire': 245, 'Swindon': 347,
                    'Bournemouth': 33, 'Poole': 262, 'Christchurch': 78, 'East Dorset': 113, 'North Dorset': 232,
                    'Purbeck': 266, 'West Dorset': 389, 'Weymouth and Portland': 399, 'Isle of Anglesey': 178,
                    'Conwy': 83, 'Gwynedd': 151, 'Denbighshire': 98, 'Wrexham': 410, 'Flintshire': 138,
                    'Caerphilly': 51, 'Blaenau Gwent': 28, 'Newport': 228, 'Torfaen': 364, 'Monmouthshire': 220,
                    'Swansea': 346, 'Merthyr Tydfil': 210, 'Neath Port Talbot': 222, 'Bridgend': 40, 'Cardiff': 58,
                    'The Vale of Glamorgan': 359, 'Rhondda, Cynon, Taff': 274, 'Carmarthenshire': 60, 'Ceredigion': 65,
                    'Pembrokeshire': 256, 'Powys': 264, 'Highland': 169, 'Western Isles': 397, 'Orkney Islands': 253,
                    'Shetland Islands': 301, 'Aberdeen City': 0, 'Moray': 221, 'Aberdeenshire': 1,
                    'Perth and Kinross': 259, 'Dundee City': 106, 'Angus': 6, 'Fife': 137, 'Edinburgh, City of': 126,
                    'Scottish Borders': 293, 'West Lothian': 393, 'Midlothian': 217, 'East Lothian': 118,
                    'Falkirk': 134, 'Stirling': 335, 'Clackmannanshire': 80, 'Glasgow City': 144,
                    'East Dunbartonshire': 114, 'East Renfrewshire': 120, 'Renfrewshire': 272, 'Inverclyde': 176,
                    'Argyll and Bute': 7, 'West Dunbartonshire': 390, 'North Lanarkshire': 237,
                    'South Lanarkshire': 316, 'North Ayrshire': 229, 'East Ayrshire': 110, 'South Ayrshire': 306,
                    'Dumfries and Galloway': 105, 'Cheshire East': 70, 'Cheshire West and Chester': 71,
                    'Northumberland': 247, 'County Durham': 88, 'Shropshire': 303, 'Central Bedfordshire': 64,
                    'Cornwall': 86, 'Wiltshire': 401}

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

road_condition_mapping_inverse = {
    4: 'Wet or damp',
    0: ' Dry',
    2: 'Frost or ice',
    3: 'Snow',
    1: 'Flood over 3cm. deep',
}

Number_of_vehicle_mapping = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
}

Number_of_Casualties_mapping = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
}

Weather_condition_for_severity_mapping = {
    'Raining no high winds': 4,
    'Fine no high winds': 1,
    'Snowing no high winds': 6,
    'Fine + high winds': 0,
    'Raining + high winds': 3,
    'Fog or mist': 2,
    'Snowing + high winds': 5,
}

Light_condition_for_severity_mapping = {
    'Daylight': 4,
    'Darkness - lights lit': 1,
    'Darkness - lighting unknown': 7,
    'Darkness - lights unlit': 5,
    'Darkness - no lighting': 6,
}

road_condition_mapping_severity = {
    'Wet or damp': 1,
    'Dry': 2,
    'Frost or ice': 3,
    'Snow': 4,
    'Flood over 3cm. deep': 5,
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
        prediction_2 = road_type_prediction()

        return render_template('aaa.html', predictions=[predictions, road_condition_mapping_inverse[prediction_2[0]]])

    return render_template('aaa.html', predictions=None)

def road_type_prediction():
    if request.method == 'POST':
        road_type = 3
        accident_severity = 3
        input_data = [Weather_condition_mapping[request.form['Weather conditions']],
                      Light_condition_mapping[request.form['Light conditions']],
                      road_type, accident_severity
                      ]

        # Make prediction using the new model
        prediction = loaded_model.predict([input_data])
        print(prediction)

        return prediction


@app.route('/new_page', methods=['GET', 'POST'])
def new_page():
    if request.method == 'POST':
        # Get values from the form
        input_values_severity = [
            Number_of_vehicle_mapping[request.form['Number_of_Vehicles']],
            Number_of_Casualties_mapping[request.form['Number_of_Casualties']],
            Weather_condition_for_severity_mapping[request.form['Weather_Conditions']],
            road_condition_mapping_severity[request.form['Road_Surface_Conditions']],
            Light_condition_for_severity_mapping[request.form['Light conditions']],
        ]

        # Make predictions
        predictions_severity = severity_model.predict([input_values_severity])

        return render_template('bbb.html', predictions=[predictions_severity])

    return render_template('bbb.html', predictions=None)


if __name__ == '__main__':
    app.run(debug=True)