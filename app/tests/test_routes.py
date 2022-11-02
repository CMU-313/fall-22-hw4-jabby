from flask import Flask

from app.handlers.routes import configure_routes


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'

#when the input for G1 scores are invalid (not between 0 and 20)
def test_invalid_G1():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #G1 too high
    data={'G1':"21", 'G2':"5", 'Studytime':1, 'Absences':43}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #G1 too low
    data={'G1':"-1", 'G2':"5", 'Studytime':1, 'Absences':43}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

#when the input for G2 scores are invalid (not between 0 and 20)
def test_invalid_G2():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #G1 too high
    data={'G1':"19", 'G2':"22", 'Studytime':4, 'Absences':0}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #G1 too low
    data={'G1':"19", 'G2':"-5", 'Studytime':4, 'Absences':0}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

#when the input for studytime is invalid (not an interger 1 <= n <= 4)
def test_invalid_studytime():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #studytime too high
    data={'G1':"20", 'G2':"20", 'Studytime':5, 'Absences':0}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #studytime too low
    data={'G1':"10", 'G2':"10", 'Studytime':-1, 'Absences':40}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #studytime decimal
    data={'G1':"10", 'G2':"10", 'Studytime':2.5, 'Absences':12}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

#when the input for absences is invalid (not an integer between 0 and 93)
def test_invalid_absences():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #absences too high (> 93)
    data={'G1':"8", 'G2':"13", 'Studytime':1, 'Absences':100}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #absences too low
    data={'G1':"18", 'G2':"20", 'Studytime':3, 'Absences':-4}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #absences decimal
    data={'G1':"10", 'G2':"10", 'Studytime':2, 'Absences':15.2}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #absences non-numeric
    data={'G1':"10", 'G2':"10", 'Studytime':2, 'Absences':None}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

def test_data_format():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #Data is a list
    data=['G1',"8", 'G2',"13", 'Studytime',1, 'Absences',90]
    response = client.get(url, query_string=data)
    assert response.status_code == 400

    #Data is a string
    data= "G1,8, G2,13, Studytime,1, Absences,90"
    response = client.get(url, query_string=data)
    assert response.status_code == 400

    #Data is a uses wrong feature names
    data={'G10':"20", 'G22':"13", 'Studytime':1, 'Absences':90}
    response = client.get(url, query_string=data)
    assert response.status_code == 400

    #Data doesnt use all 4 feature names
    data={'G1':"20", 'G2':"13", 'Absences':90}
    response = client.get(url, query_string=data)
    assert response.status_code == 400





