import pandas as pd
import pickle


model = pickle.load(
    open('models/flight-fare-predictor/random_forest_flight.pkl', 'rb'))


def flight_fare_prediction(request):
    date_dep = request.form["Dep_Time"]
    Journey_day = int(pd.to_datetime(
        date_dep, format="%Y-%m-%dT%H:%M").day)
    Journey_month = int(pd.to_datetime(
        date_dep, format="%Y-%m-%dT%H:%M").month)

    Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
    Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

    date_arr = request.form["Arrival_Time"]
    Arrival_hour = int(pd.to_datetime(
        date_arr, format="%Y-%m-%dT%H:%M").hour)
    Arrival_min = int(pd.to_datetime(
        date_arr, format="%Y-%m-%dT%H:%M").minute)

    dur_hour = abs(Arrival_hour - Dep_hour)
    dur_min = abs(Arrival_min - Dep_min)

    Total_stops = int(request.form["stops"])

    airline = request.form['airline']
    if(airline == 'Super Air Jet'):
        Super_Air_Jet = 1
        Citilink = 0
        Lion_Air = 0
        Batik_Air = 0
        NAM_Air = 0
        Sriwijaya_Air = 0
        Wings_Air = 0
        Malindo_Air = 0
        Garuda_Indonesia = 0
        Pelita_Air = 0
        TransNusa = 0

    elif (airline == 'Citilink'):
        Super_Air_Jet = 0
        Citilink = 1
        Lion_Air = 0
        Batik_Air = 0
        NAM_Air = 0
        Sriwijaya_Air = 0
        Wings_Air = 0
        Malindo_Air = 0
        Garuda_Indonesia = 0
        Pelita_Air = 0
        TransNusa = 0

    elif (airline == 'Lion Air'):
        Super_Air_Jet = 0
        Citilink = 0
        Lion_Air = 1
        Batik_Air = 0
        NAM_Air = 0
        Sriwijaya_Air = 0
        Wings_Air = 0
        Malindo_Air = 0
        Garuda_Indonesia = 0
        Pelita_Air = 0
        TransNusa = 0

    elif (airline == 'Batik Air'):
        Super_Air_Jet = 0
        Citilink = 0
        Lion_Air = 0
        Batik_Air = 1
        NAM_Air = 0
        Sriwijaya_Air = 0
        Wings_Air = 0
        Malindo_Air = 0
        Garuda_Indonesia = 0
        Pelita_Air = 0
        TransNusa = 0

    elif (airline == 'NAM Air'):
        Super_Air_Jet = 0
        Citilink = 0
        Lion_Air = 0
        Batik_Air = 0
        NAM_Air = 1
        Sriwijaya_Air = 0
        Wings_Air = 0
        Malindo_Air = 0
        Garuda_Indonesia = 0
        Pelita_Air = 0
        TransNusa = 0

    elif (airline == 'Sriwijaya Air'):
        Super_Air_Jet = 0
        Citilink = 0
        Lion_Air = 0
        Batik_Air = 0
        NAM_Air = 0
        Sriwijaya_Air = 1
        Wings_Air = 0
        Malindo_Air = 0
        Garuda_Indonesia = 0
        Pelita_Air = 0
        TransNusa = 0

    elif (airline == 'Wings Air'):
        Super_Air_Jet = 0
        Citilink = 0
        Lion_Air = 0
        Batik_Air = 0
        NAM_Air = 0
        Sriwijaya_Air = 0
        Wings_Air = 1
        Malindo_Air = 0
        Garuda_Indonesia = 0
        Pelita_Air = 0
        TransNusa = 0

    elif (airline == 'Malindo Air'):
        Super_Air_Jet = 0
        Citilink = 0
        Lion_Air = 0
        Batik_Air = 0
        NAM_Air = 0
        Sriwijaya_Air = 0
        Wings_Air = 0
        Malindo_Air = 1
        Garuda_Indonesia = 0
        Pelita_Air = 0
        TransNusa = 0

    elif (airline == 'Garuda Indonesia'):
        Super_Air_Jet = 0
        Citilink = 0
        Lion_Air = 0
        Batik_Air = 0
        NAM_Air = 0
        Sriwijaya_Air = 0
        Wings_Air = 0
        Malindo_Air = 0
        Garuda_Indonesia = 1
        Pelita_Air = 0
        TransNusa = 0

    elif (airline == 'Pelita Air'):
        Super_Air_Jet = 0
        Citilink = 0
        Lion_Air = 0
        Batik_Air = 0
        NAM_Air = 0
        Sriwijaya_Air = 0
        Wings_Air = 0
        Malindo_Air = 0
        Garuda_Indonesia = 0
        Pelita_Air = 1
        TransNusa = 0

    elif (airline == 'TransNusa'):
        Super_Air_Jet = 0
        Citilink = 0
        Lion_Air = 0
        Batik_Air = 0
        NAM_Air = 0
        Sriwijaya_Air = 0
        Wings_Air = 0
        Malindo_Air = 0
        Garuda_Indonesia = 0
        Pelita_Air = 0
        TransNusa = 1

    else:
        Super_Air_Jet = 0
        Citilink = 0
        Lion_Air = 0
        Batik_Air = 0
        NAM_Air = 0
        Sriwijaya_Air = 0
        Wings_Air = 0
        Malindo_Air = 0
        Garuda_Indonesia = 0
        Pelita_Air = 0
        TransNusa = 0

    Source = request.form["Source"]
    if (Source == 'Yogyakarta'):
        s_Yogyakarta = 1
        s_Surabaya = 0
        s_Manado = 0
        s_Makassar = 0

    elif (Source == 'Surabaya'):
        s_Yogyakarta = 0
        s_Surabaya = 1
        s_Manado = 0
        s_Makassar = 0

    elif (Source == 'Manado'):
        s_Yogyakarta = 0
        s_Surabaya = 0
        s_Manado = 1
        s_Makassar = 0

    elif (Source == 'Makassar'):
        s_Yogyakarta = 0
        s_Surabaya = 0
        s_Manado = 0
        s_Makassar = 1

    else:
        s_Yogyakarta = 0
        s_Surabaya = 0
        s_Manado = 0
        s_Makassar = 0

    Destination = request.form["Destination"]
    if (Destination == 'Denpasar'):
        d_Denpasar = 1
        d_Yogyakarta = 0
        d_Jakarta = 0
        d_Lombok = 0
        d_Surabaya = 0

    elif (Destination == 'Yogyakarta'):
        d_Denpasar = 0
        d_Yogyakarta = 1
        d_Jakarta = 0
        d_Lombok = 0
        d_Surabaya = 0

    elif (Destination == 'Jakarta'):
        d_Denpasar = 0
        d_Yogyakarta = 0
        d_Jakarta = 1
        d_Lombok = 0
        d_Surabaya = 0

    elif (Destination == 'Lombok'):
        d_Denpasar = 0
        d_Yogyakarta = 0
        d_Jakarta = 0
        d_Lombok = 1
        d_Surabaya = 0

    elif (Destination == 'Surabaya'):
        d_Denpasar = 0
        d_Yogyakarta = 0
        d_Jakarta = 0
        d_Lombok = 0
        d_Surabaya = 1

    else:
        d_Denpasar = 0
        d_Yogyakarta = 0
        d_Jakarta = 0
        d_Lombok = 0
        d_Surabaya = 0

    prediction = model.predict([[
        Total_stops,
        Journey_day,
        Journey_month,
        Dep_hour,
        Dep_min,
        Arrival_hour,
        Arrival_min,
        dur_hour,
        dur_min,
        Lion_Air,
        Wings_Air,
        Citilink,
        Super_Air_Jet,
        Garuda_Indonesia,
        Batik_Air,
        Malindo_Air,
        NAM_Air,
        TransNusa,
        Sriwijaya_Air,
        Pelita_Air,
        s_Makassar,
        s_Yogyakarta,
        s_Surabaya,
        s_Manado,
        d_Denpasar,
        d_Yogyakarta,
        d_Lombok,
        d_Surabaya,
        d_Jakarta
    ]])
    print(prediction)
    output = round(prediction[0], 2)
    return output
