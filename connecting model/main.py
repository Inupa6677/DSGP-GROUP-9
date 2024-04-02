import json
from datetime import time
import gzip

from flask import Flask, render_template, request, jsonify, Response
import pickle

app = Flask(__name__)

districts = {
    "Kensington and Chelsea": [51.50379515, -0.20078938323179596],
    "Hammersmith and Fulham": [51.498314199999996, -0.22787818358222445],
    "Westminster": [51.5004439, -0.1265398],
    "City of London": [51.5156177, -0.0919983],
    "Tower Hamlets": [51.1288633, 1.2986686],
    "Southwark": [51.5022549, -0.093898],
    "Hackney": [51.5432402, -0.0493621],
    "Islington": [51.5384287, -0.0999051],
    "Camden": [51.54279655, -0.16248031357798964],
    "Lambeth": [51.4952111, -0.1163354],
    "Brent": [51.5639957, -0.27590641378489267],
    "Haringey": [51.587929849999995, -0.10541771297992009],
    "Barnet": [51.65309, -0.2002261],
    "Ealing": [51.5126553, -0.3051952],
    "Richmond upon Thames": [51.4405529, -0.3076394377337949],
    "Waltham Forest": [51.59816935, -0.01783667461048707],
    "Newham": [51.5300157, 0.029309078788513746],
    "Hillingdon": [51.542519299999995, -0.44833493117949663],
    "Harrow": [51.596827149999996, -0.3373046180437286],
    "Hounslow": [51.4686132, -0.3613471],
    "Enfield": [51.6520851, -0.0810175],
    "Redbridge": [51.5765828, 0.0453401],
    "Barking and Dagenham": [51.5540907, 0.15048888801039415],
    "Havering": [51.55792615, 0.24981280474568598],
    "Croydon": [51.3713049, -0.101957],
    "Wandsworth": [51.4570271, -0.1932607],
    "Sutton": [51.357464449999995, -0.17362689496950337],
    "Lewisham": [51.4624292, -0.0101787],
    "Bromley": [51.36685695, 0.061709076090816765],
    "Greenwich": [51.46862565, 0.04883057313755089],
    "Bexley": [51.4416793, 0.150488],
    "Kingston upon Thames": [51.4096275, -0.3062621],
    "Merton": [51.41086985, -0.18809708858824303],
    "South Lakeland": [54.272069099999996, -2.7713616872258533],
    "Barrow-in-Furness": [54.128879600000005, -3.2269008205428933],
    "Carlisle": [54.8948478, -2.9362311],
    "Eden": [54.605648099999996, -2.671522203148835],
    "Allerdale": [54.70888095, -3.252788011003595],
    "Copeland": [54.3876165, -3.331125339681134],
    "Blackpool": [53.8179442, -3.0509812],
    "Fylde": [53.79336215, -2.89426008005],
    "Lancaster": [54.0484068, -2.7990345],
    "Preston": [53.7593363, -2.6992717],
    "Wyre": [59.1193222, -2.970156643353808],
    "South Ribble": [53.72715265, -2.733006645899704],
    "West Lancashire": [53.6109397, -2.856571332507083],
    "Chorley": [53.6531915, -2.6294313],
    "Hyndburn": [53.7607317, -2.39005491388217],
    "Ribble Valley": [53.902644050000006, -2.42285603548628],
    "Pendle": [53.87904015, -2.17177953034584],
    "Rossendale": [53.6848806, -2.261439758907419],
    "Burnley": [53.7907262, -2.2439196],
    "Wirral": [53.3409714, -3.0500916],
    "Sefton": [53.5034122, -2.9714708],
    "Liverpool": [53.4071991, -2.99168],
    "Knowsley": [53.4552358, -2.8546852],
    "St. Helens": [53.4535471, -2.7343231],
    "Manchester": [53.4794892, -2.2451148],
    "Oldham": [53.5415797, -2.1147831],
    "Salford": [53.4877463, -2.2891921],
    "Bury": [53.5927543, -2.2972827],
    "Rochdale": [53.6153659, -2.1557561],
    "Trafford": [53.41893605, -2.359297161165271],
    "Tameside": [53.4786454, -2.0770211633705165],
    "Stockport": [53.407901, -2.160243],
    "Wigan": [53.5457188, -2.6264624],
    "Bolton": [53.5782863, -2.4300367],
    "Chester": [53.1908873, -2.8908955],
    "Warrington": [53.3899497, -2.5943178],
    "Halton": [51.7827392, -0.7329026],
    "Macclesfield": [53.2606635, -2.1255158],
    "Congleton": [53.1631463, -2.2110691],
    "Newcastle upon Tyne": [54.9738474, -1.6131572],
    "Sunderland": [54.9058512, -1.3828727],
    "North Tyneside": [55.02979945, -1.5082559996141889],
    "Alnwick": [55.4133398, -1.7072354],
    "Wansbeck": [55.1550294, -1.8408528],
    "Blyth Valley": [55.131547, -1.5355715433078085],
    "Gateshead": [54.9625789, -1.6019294],
    "South Tyneside": [54.969874250000004, -1.4476805465645368],
    "Tynedale": [54.8344126, -2.4626971],
    "Berwick-upon-Tweed": [55.7692442, -2.0026472],
    "Wear Valley": [54.6808089, -1.7443224],
    "Sedgefield": [54.6531916, -1.4496577],
    "Durham": [54.7770139, -1.5756205],
    "Easington": [54.7850506, -1.3530807],
    "Chester-le-Street": [54.8543237, -1.5750431],
    "Derwentside": [53.01238235, -1.4797318589285722],
    "Teesdale": [54.5629815, -1.3058935],
    "Darlington": [54.5242081, -1.5555812],
    "York": [53.9590555, -1.0815361],
    "Scarborough": [54.2820009, -0.4011868],
    "Craven": [54.05375295, -2.1615123808472636],
    "Harrogate": [53.9921491, -1.5391039],
    "Hambleton": [54.25045835, -1.4368783044428555],
    "Richmondshire": [54.357404700000004, -1.9849524966858705],
    "Selby": [53.785097, -1.099040720243205],
    "Ryedale": [54.198424200000005, -0.8614246108484555],
    "Leeds": [53.7974185, -1.5437941],
    "Calderdale": [53.720474800000005, -1.9622886329676708],
    "Bradford": [53.7944229, -1.7519186],
    "Kirklees": [53.64226345, -1.7809432689150708],
    "Wakefield": [53.6829541, -1.4967286],
    "Doncaster": [53.5227681, -1.1335312],
    "Rotherham": [53.4310417, -1.355187],
    "Barnsley": [53.5527719, -1.4827755],
    "Sheffield": [53.3806626, -1.4702278],
    "North East Lincolnshire": [53.56438835, -0.0810723322393459],
    "North Lincolnshire": [53.58801535, -0.6926116415797723],
    "East Riding of Yorkshire": [53.873596500000005, -0.5347787525091569],
    "Hartlepool": [54.6857276, -1.2093696],
    "Middlesbrough": [54.5760419, -1.2344047],
    "Stockton-on-Tees": [54.564094, -1.3129164],
    "Birmingham": [52.4796992, -1.9026911],
    "Wolverhampton": [52.5847651, -2.127567],
    "Walsall": [52.5847949, -1.9822687],
    "Dudley": [52.5110832, -2.0816813],
    "Sandwell": [52.5151278, -2.013562373718973],
    "Solihull": [52.4130189, -1.7768935],
    "Coventry": [52.4081812, -1.510477],
    "Stoke-on-Trent": [53.0162014, -2.1812607],
    "Stafford": [52.8063157, -2.1163818],
    "Staffordshire Moorlands": [53.07155675, -1.9742007118455929],
    "Newcastle-under-Lyme": [53.0117627, -2.2273919],
    "East Staffordshire": [52.8878642, -1.9030802448726154],
    "Cannock Chase": [52.7069197, -1.9784347546729857],
    "South Staffordshire": [52.6047717, -2.259164838541728],
    "Lichfield": [52.6843696, -1.8275286],
    "Tamworth": [52.6345819, -1.6948438],
    "Worcester": [52.1911849, -2.2206585],
    "Wychavon": [52.1803417, -2.0623136726812445],
    "Malvern Hills": [52.1675333, -2.3311602038846546],
    "Wyre Forest": [52.385059150000004, -2.2347966141505187],
    "Bromsgrove": [52.3390519, -2.0532017992446177],
    "Redditch": [52.3057655, -1.9417444],
    "Bridgnorth": [52.5345626, -2.4194132],
    "Oswestry": [52.8603096, -3.0548201],
    "South Shropshire": [52.51314745, -2.6916002805195407],
    "Stratford-upon-Avon": [52.1927803, -1.70634],
    "Warwick": [52.2814519, -1.5815742],
    "Rugby": [52.3726682, -1.2620038],
    "North Warwickshire": [52.561361, -1.6296344436864212],
    "Nuneaton and Bedworth": [52.5010313, -1.4677391944516698],
    "Erewash": [52.93800485, -1.3513172392396116],
    "Amber Valley": [53.029038400000005, -1.4625031096700565],
    "Bolsover": [53.228666, -1.2912756],
    "Derbyshire Dales": [53.1302876, -1.6561732789685428],
    "High Peak": [53.3675462, -1.8528746491564894],
    "North East Derbyshire": [53.2226728, -1.5239285999071135],
    "Chesterfield": [53.2352134, -1.4264097],
    "South Derbyshire": [52.8224616, -1.5026362190000033],
    "Derby": [52.9212617, -1.4761491],
    "Mansfield": [53.1443785, -1.1964165],
    "Ashfield": [53.089773750000006, -1.2518767461557148],
    "Newark and Sherwood": [53.10895395, -0.9443017980263069],
    "Bassetlaw": [53.34945205, -0.9616604011939824],
    "Rushcliffe": [52.91250105, -1.0110622291190852],
    "Nottingham": [52.9534193, -1.1496461],
    "Broxtowe": [52.9782566, -1.2170642],
    "Gedling": [53.02605385, -1.1071169188526024],
    "South Holland": [52.8127195, -0.0012627972576260693],
    "South Kesteven": [52.850266500000004, -0.49519247416097134],
    "North Kesteven": [53.07252915, -0.44735386588179665],
    "East Lindsey": [53.2680103, 0.012775773043408906],
    "West Lindsey": [53.39772845, -0.5035287500531207],
    "Boston": [52.9776561, -0.0237985],
    "Lincoln": [53.2293545, -0.5404819],
    "Leicester": [52.6362, -1.1331969],
    "Harborough": [52.538568850000004, -0.9200444888910031],
    "Charnwood": [52.7392639, -1.1370832780406597],
    "North West Leicestershire": [52.770420099999996, -1.3965046691471592],
    "Rutland": [52.6423036, -0.6632643077026672],
    "Blaby": [52.5731976, -1.1646389],
    "Hinckley and Bosworth": [52.608409, -1.4171909963481428],
    "Oadby and Wigston": [52.5870666, -1.0997802143476827],
    "Melton": [52.8117106, -0.8592867292244459],
    "Kettering": [52.3994233, -0.728004],
    "Corby": [52.4877341, -0.7032713],
    "East Northamptonshire": [52.448520650000006, -0.5084214504274196],
    "Daventry": [52.2578681, -1.1626569],
    "Northampton": [52.2378853, -0.8963639],
    "South Northamptonshire": [52.11838535, -1.080081479517063],
    "Wellingborough": [52.30189, -0.6937309],
    "South Cambridgeshire": [52.179654049999996, -0.0034368130503711347],
    "Cambridge": [52.2055314, 0.1186637],
    "Huntingdonshire": [52.37104395, -0.22357789271655937],
    "Peterborough": [52.5725769, -0.2427336],
    "East Cambridgeshire": [52.33498865, 0.26289392438863995],
    "Fenland": [52.56284005, 0.010157722129947797],
    "Breckland": [52.5903063, 0.7590363095765305],
    "King's Lynn and West Norfolk": [52.71316265, 0.4348749234835659],
    "Great Yarmouth": [52.6071742, 1.7314845],
    "Broadland": [52.6928977, 1.2564875194162244],
    "North Norfolk": [52.835651999999996, 1.12765976862862],
    "Norwich": [52.6285576, 1.2923954],
    "South Norfolk": [52.5169106, 1.3661677814433835],
    "Suffolk Coastal": [52.150302749999994, 1.399856666807915],
    "St. Edmundsbury": [52.22719735, 0.6902500874730714],
    "Ipswich": [52.0579324, 1.1528095],
    "Forest Heath": [52.3326306, 0.5386848363954675],
    "Mid Suffolk": [52.23476185, 1.0451342631685334],
    "Babergh": [52.06297535, 0.9122241568513769],
    "Waveney": [52.43089725, 1.55359640688228],
    "Bedford": [52.1363806, -0.4675041],
    "Luton": [51.8784385, -0.4152837],
    "East Hertfordshire": [51.86567885, 0.012485012653673036],
    "North Hertfordshire": [51.956864949999996, -0.22305090784172493],
    "Welwyn Hatfield": [51.77310555, -0.20951705297322926],
    "Broxbourne": [51.7465723, -0.0190782],
    "St. Albans": [51.753051, -0.3379675],
    "Watford": [51.6553875, -0.3957425],
    "Three Rivers": [51.670137600000004, -0.47380132279242626],
    "Hertsmere": [51.68082975, -0.2681113103109687],
    "Dacorum": [51.768954050000005, -0.5515510187562057],
    "Stevenage": [51.9016663, -0.2027155],
    "Uttlesford": [51.929989500000005, 0.2708364751351891],
    "Braintree": [51.8780637, 0.5537161],
    "Colchester": [51.8896903, 0.8994651],
    "Epping Forest": [51.6676884, 0.054801129257444646],
    "Chelmsford": [51.7345329, 0.4730532],
    "Harlow": [51.7676194, 0.0974893],
    "Basildon": [51.5754602, 0.4757363],
    "Thurrock": [51.5080169, 0.3962817395437666],
    "Brentwood": [51.6201654, 0.3018662],
    "Maldon": [51.7155563, 0.6843547574257541],
    "Tendring": [51.8753236, 1.1128842],
    "Southend-on-Sea": [51.54063195, 0.7161146725194144],
    "Castle Point": [51.54450755, 0.5840084067307691],
    "Rochford": [51.584060199999996, 0.6787130935643773],
    "Aylesbury Vale": [51.899954750000006, -0.8782710004180965],
    "Wycombe": [51.66356185, -0.818083680966309],
    "South Bucks": [51.5601709, -0.5851035437631282],
    "Milton Keynes": [52.0406502, -0.7594092],
    "Chiltern": [51.67893035, -0.6295205849333023],
    "Slough": [51.5111014, -0.5940682],
    "Cherwell": [51.974716900000004, -1.2262941038785593],
    "South Oxfordshire": [51.6366088, -1.0804971850045213],
    "Vale of White Horse": [51.654201, -1.4857034705882355],
    "West Oxfordshire": [51.84036295, -1.512127443949482],
    "Oxford": [51.7520131, -1.2578499],
    "Wokingham": [51.4120318, -0.8324037],
    "Reading": [51.4564242, -0.9700664],
    "Isle of Wight": [50.67108245, -1.3328042802764226],
    "Southampton": [50.9025349, -1.404189],
    "East Hampshire": [51.07788895, -0.9439075864537129],
    "Havant": [50.8334197, -0.9826589433165432],
    "Gosport": [50.7952074, -1.1210853],
    "Fareham": [50.8526637, -1.1783134],
    "Winchester": [51.0612766, -1.3131692],
    "Hart": [51.2761671, -0.8927989805623809],
    "Eastleigh": [50.9202337, -1.2992656195130934],
    "Basingstoke and Deane": [51.2587797, -1.221107318149007],
    "New Forest": [50.8556349, -1.595562812670837],
    "Portsmouth": [50.800031, -1.0906023],
    "Test Valley": [51.13379045, -1.5182864265840892],
    "Rushmoor": [51.27523885, -0.7693917288354035],
    "Elmbridge": [52.308409, -2.1474369],
    "Runnymede": [51.3948374, -0.5519609464752796],
    "Guildford": [51.2356068, -0.5732063],
    "Mole Valley": [51.220094450000005, -0.33475519270708765],
    "Spelthorne": [51.4250347, -0.45928607609154937],
    "Epsom and Ewell": [51.3363098, -0.26738169267465284],
    "Reigate and Banstead": [51.25164045, -0.18646821513076053],
    "Woking": [51.3201891, -0.5564726],
    "Waverley": [51.158322999999996, -0.6233216066405007],
    "Surrey Heath": [51.33588905, -0.6916534194642882],
    "Tandridge": [51.2393372, -0.0344318],
    "Medway": [51.2011154, 0.3053652],
    "Dartford": [51.4443059, 0.21807],
    "Gravesham": [51.39723695, 0.3961725871463415],
    "Sevenoaks": [51.27452185, 0.1961165562194977],
    "Dover": [51.1251275, 1.3134228],
    "Shepway": [51.2545962, 0.5444141],
    "Thanet": [51.353304550000004, 1.3319865973513279],
    "Canterbury": [51.2800275, 1.0802533],
    "Tunbridge Wells": [51.1371483, 0.2673446],
    "Swale": [51.3367451, 0.801369798606056],
    "Ashford": [51.148555, 0.8722566],
    "Tonbridge and Malling": [51.2717306, 0.3566598007492124],
    "Maidstone": [51.2748258, 0.5231646],
    "Wealden": [50.94216925, 0.19728012945979825],
    "Mid Sussex": [51.0053398, -0.1273113444043321],
    "Eastbourne": [50.7664372, 0.2781546],
    "Lewes": [50.8746139, 0.005115324110936268],
    "Chichester": [50.8364862, -0.7791721],
    "Rother": [50.9514264, 0.5740489897457741],
    "Hastings": [50.8553888, 0.5824703],
    "Crawley": [51.1103444, -0.1801094],
    "Horsham": [51.0630273, -0.3295028],
    "Worthing": [50.8115402, -0.3699697],
    "Arun": [50.8312375, -0.5667058666407475],
    "Adur": [50.8453169, -0.2939886608407643],
    "Carrick": [56.1085281, -4.9068527],
    "Penwith": [50.1243845, -5.6797375],
    "Restormel": [50.40880465, -4.665969289258948],
    "West Devon": [50.651997449999996, -4.0743108539440955],
    "Torridge": [50.86260145, -4.261205563247918],
    "Caradon": [53.016360500000005, -2.192684977897874],
    "North Devon": [51.061456, -3.923923297566936],
    "Exeter": [50.7255794, -3.5269497],
    "East Devon": [50.7568771, -3.221564289113528],
    "Teignbridge": [50.6125552, -3.6559105980908284],
    "Mid Devon": [50.86839225, -3.5996999898540123],
    "Plymouth": [50.3714122, -4.1424451],
    "South Hams": [50.3720497, -3.8162519907888086],
    "Torbay": [57.481626250000005, -3.110758130615536],
    "Sedgemoor": [51.186833899999996, -2.96842123193061],
    "Mendip": [51.1943905, -2.5419221103264027],
    "Bristol, City of": [51.48189155, -2.6762564101791533],
    "West Somerset": [51.1187353, -3.503574888540328],
    "Taunton Deane": [51.00478595, -3.1646086380896605],
    "South Somerset": [50.9843053, -2.776156179800813],
    "Stroud": [51.745424, -2.2198605],
    "Tewkesbury": [51.9925394, -2.1560169592908442],
    "Cheltenham": [51.8995685, -2.0711559],
    "Gloucester": [51.8653705, -2.2458192],
    "Forest of Dean": [51.7996179, -2.5305841628747032],
    "Cotswold": [51.84516805, -1.891330800141246],
    "Salisbury": [51.0690613, -1.7954134],
    "Kennet": [51.411627, -1.8560933],
    "West Wiltshire": [51.0040755, -1.9698799243801026],
    "Swindon": [51.5613683, -1.7856853],
    "Bournemouth": [50.744673199999994, -1.85795768008541],
    "Poole": [50.7179472, -1.981521],
    "Christchurch": [50.734902, -1.7778853],
    "East Dorset": [50.86741225, -1.9479660395581657],
    "North Dorset": [50.91989035, -2.2311490001616763],
    "Purbeck": [50.68477665, -2.125601238918458],
    "West Dorset": [50.79511975, -2.5993664646317165],
    "Weymouth and Portland": [50.5956611, -2.471982556506139],
    "Conwy": [53.2811822, -3.8287012],
    "Gwynedd": [52.9089585, -3.8335244282124785],
    "Denbighshire": [53.054215, -3.3019677117412627],
    "Wrexham": [53.0465084, -2.9937869],
    "Flintshire": [53.2164585, -3.140152518830291],
    "Caerphilly": [51.5745432, -3.2208487],
    "Newport": [51.5882332, -2.9974967],
    "Torfaen": [51.77523025, -3.0947368958238295],
    "Monmouthshire": [51.72930045, -2.9686601316219794],
    "Swansea": [51.6195955, -3.9459248],
    "Merthyr Tydfil": [51.7455659, -3.3786082],
    "Neath Port Talbot": [51.63005975, -3.8241807330430637],
    "Bridgend": [51.5049859, -3.5756674],
    "Cardiff": [51.4816546, -3.1791934],
    "Carmarthenshire": [51.6736943, -4.1438947575183676],
    "Pembrokeshire": [52.016880150000006, -4.825812543299195],
    "Powys": [52.32714995, -3.3553352394722493],
    "Highland": [52.33163395, -1.9289503086172042],
    "Orkney Islands": [58.8520573, -3.2869398422535223],
    "Aberdeen City": [57.1482429, -2.0928095],
    "Moray": [57.7871935, -3.6312684],
    "Aberdeenshire": [57.583682550000006, -2.085348718118604],
    "Angus": [56.715141349999996, -2.890562836754113],
    "Fife": [56.3193913, -3.0116545],
    "Edinburgh, City of": [55.9533456, -3.1883749],
    "Scottish Borders": [55.58869195, -2.435109743288253],
    "West Lothian": [55.89393925, -3.6252888543587343],
    "Midlothian": [55.99447265, -3.3432274069999997],
    "East Lothian": [56.00534005, -2.867991337896362],
    "Falkirk": [55.9991959, -3.784376],
    "Stirling": [56.1181242, -3.9360012],
    "Clackmannanshire": [56.10695545, -3.7892856919373257],
    "Glasgow City": [55.8498675, -4.2415293426103755],
    "Cheshire West and Chester": [53.122604249999995, -2.8077988826624622],
    "Northumberland": [55.2970562, -2.0677894217139507],
    "County Durham": [54.68483225, -1.774017169596316],
    "Shropshire": [52.65233935, -2.64356407027027],
    "Central Bedfordshire": [51.90559305, -0.5469384734010054],
    "Cornwall": [50.443348900000004, -4.62465658489158],
    "Wiltshire": [51.324162, -1.9032486699002247],
    "London Airport (Heathrow)": [51.470020, -0.454295],
    "Blackburn with Darwen": [53.7402, -2.4728],
    "Crewe and Nantwich": [53.0932, -2.4870],
    "Vale Royal": [53.2247, -2.5426],
    "Ellesmere Port and Neston": [53.279812, -2.897404],
    "Castle Morpeth": [55.16435, -1.68768],
    "Kingston upon Hull, City of": [53.767750, -0.335827],
    "Redcar and Cleveland": [54.5792, -1.0341],
    "Herefordshire, County of": [52.056499, -2.716000],
    "Shrewsbury and Atcham": [52.853638, -2.726712],
    "North Shropshire": [52.853638, -2.726712],
    "Telford and Wrekin": [52.6863, -2.4259],
    "Mid Bedfordshire": [52.136436, -0.460739],
    "South Bedfordshire": [52.136436, -0.460739],
    "Windsor and Maidenhead": [51.572803, -0.776339],
    "West Berkshire": [51.401409, -1.323114],
    "Bracknell Forest": [51.416039, -0.753980],
    "Brighton and Hove": [50.827778, -0.152778],
    "Kerrier": [50.21397625, -5.22676628],
    "North Cornwall": [50.5160, -4.8350],
    "Bath and North East Somerset": [51.3900, -2.3200],
    "South Gloucestershire": [51.864445, -2.244444],
    "North Somerset": [51.33333000, -2.83333000],
    "North Wiltshire": [51.25000000, -1.91667000],
    "Isle of Anglesey": [53.2833, -4.3333],
    "Blaenau Gwent": [51.7500, -3.1667],
    "The Vale of Glamorgan": [51.41667000, -3.41667000],
    "Rhondda, Cynon, Taff": [51.6500, -3.4373],
    "Ceredigion": [52.415089, -4.083116],
    "Western Isles": [57.666667, -7.166667],
    "Shetland Islands": [60.346958, -1.235660],
    "Perth and Kinross": [56.704361, -3.729711],
    "Dundee City": [56.462002, -2.970700],
    "East Dunbartonshire": [55.97431620, -4.20229800],
    "East Renfrewshire": [55.75000000, -4.33333000],
    "Renfrewshire": [55.8299, -4.5428],
    "Inverclyde": [55.93165690, -4.68001580],
    "Argyll and Bute": [56.37004630000001, -5.031896500000016],
    "West Dunbartonshire": [56.002716, -4.580081],
    "North Lanarkshire": [55.86624320, -3.96131440],
    "South Lanarkshire": [55.7510, -4.0510],
    "North Ayrshire": [55.723331, -4.898329],
    "East Ayrshire": [55.45184960, -4.26444780],
    "South Ayrshire": [55.458565, -4.629179],
    "Dumfries and Galloway": [55.07010730, -3.60525810],
    "Cheshire East": [53.1670, -2.3625],
}

MODEL_FILENAME = 'best_random_forest_model_zip.pkl.gz'


def load_model(filename):
    with gzip.open(filename, 'rb') as f:
        model = pickle.load(f)
    return model


model = load_model(MODEL_FILENAME)

# Load  prediction models


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
                    'Cornwall': 86, 'Wiltshire': 401,
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

Road_type_mapping = {
    'Dual carriageway': 0,
    'Single carriageway': 3,
    'One way street': 1,
    'Roundabout': 2,
    'Slip road': 4,
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
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,

}

Number_of_Casualties_mapping = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    '11': 11,
    '12': 12,
    '13': 13,
    '14': 14,
    '15': 15,
    '16': 16,
    '17': 17,
    '18': 18,
    '19': 19,
    '20': 20,
    '21': 21,
    '22': 22,
    '23': 23,
    '24': 24,
    '25': 25,

}

Weather_condition_for_severity_mapping = {
    'Raining no high winds': 2,
    'Fine no high winds': 1,
    'Snowing no high winds': 3,
    'fine + high winds': 4,
    'raining + high winds': 5,
    'snowing + high winds': 6,
    'fog or mist': 7,

}

Light_condition_for_severity_mapping = {
    'Daylight': 1,
    'Darkness - lights lit': 4,
    'Darkness - lighting unknown': 7,
    'Darkness - no lighting': 6,
    'Darkness - lights unlit': 5,
}

road_condition_mapping_severity = {
    'Wet or damp': 2,
    'Dry': 1,
    'snow': 3,
    'Frost or Ice': 4,
}

severity_mapping_inverse = {
    3: 'Slight',
    2: 'Serious',
    1: 'Fatal',
}


@app.route('/')
def index():
    return render_template('loginpage.html')


@app.route('/analysis_page')
def analysis():
    return render_template('analystpage.html')


@app.route('/home_page')
def home_page():
    return render_template('homepage.html')


coordinates = ""


@app.route('/update_coordinates', methods=['POST'])
def update_coordinates():
    data = request.get_json()
    coordinates = data.get('coordinates')
    # Log received coordinates
    print('Received coordinates:', coordinates)

    # Store the coordinates in a global variable or a data structure
    # (e.g., a queue or a list) for later retrieval
    global latest_coordinates
    latest_coordinates = coordinates

    response_data = {'status': 'success', 'message': 'Coordinates received successfully'}
    return jsonify(response_data)


@app.route('/coordinates', methods=['GET'])
def get_coordinates():
    def stream_coordinates():
        # Wait until new coordinates are available
        global latest_coordinates
        while True:
            if latest_coordinates:
                coordinates = latest_coordinates
                latest_coordinates = None
                yield 'data: {}\n\n'.format(str(coordinates))
            else:
                time.sleep(0.1)  # Reduce CPU usage by introducing a small delay

    return Response(stream_coordinates(), mimetype="text/event-stream")


@app.route('/prediction_page', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get values from the form (other inputs remain unchanged)
        input_values = [
            month_mapping[request.form['month']],
            Hour_mapping[request.form['Hour of the day']],
            day_of_the_week_mapping[request.form['Day of the week']],
            dropdown_mapping[request.form['District']],  # Continue mapping for your model
            Weather_condition_mapping[request.form['Weather conditions']],
            Light_condition_mapping[request.form['Light conditions']],
        ]

        # Make predictions
        predictions = model.predict([input_values])
        import numpy as np

        # Assuming `predictions` is a NumPy array containing the predicted values
        rounded_predictions = np.round(predictions)
        print("Mapped Input Values:", input_values)

        # Pass the form data to road_type_prediction
        prediction_2 = road_type_prediction(request.form['Weather conditions'], request.form['Light conditions'], request.form['Road Type'])

        global coordinates

        # Pass the raw district string and predictions to the template
        return render_template('aaa.html', predictions=[rounded_predictions, road_condition_mapping_inverse[prediction_2[0]]],
                               data=coordinates)
    return render_template('aaa.html', predictions=None, district=None)


def road_type_prediction(weather_condition, light_condition, road_type):
    accident_severity = 3
    input_data = [
        Weather_condition_mapping[weather_condition],
        Light_condition_mapping[light_condition],
        Road_type_mapping[road_type],
        accident_severity
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

        return render_template('bbb.html', predictions=severity_mapping_inverse[predictions_severity[0]])

    return render_template('bbb.html', predictions=None)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
