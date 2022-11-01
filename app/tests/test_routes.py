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


'''
Test Cases - Valid Number and Format (status=200)
'''
#when the input for G1 scores is valid (between 0 and 20)
def test_valid_G1():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #G1 at high edge
    data={'G1':"20", 'G2':"5", 'Studytime':1, 'Absences':43}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

    #G1 at low edge
    data={'G1':"0", 'G2':"3", 'Studytime':2, 'Absences':4}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

    #G1 in between
    data={'G1':"8", 'G2':"17", 'Studytime':3, 'Absences':71}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

#when the input for G2 scores are valid (not between 0 and 20)
def test_valid_G2():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #G2 at high edge
    data={'G1':"19", 'G2':"20", 'Studytime':4, 'Absences':7}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

    #G2 at low edge
    data={'G1':"18", 'G2':"0", 'Studytime':1, 'Absences':88}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

    #G2 in between
    data={'G1':"2", 'G2':"6", 'Studytime':3, 'Absences':11}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

#when the input for studytime is valid (integer in 1 <= n <= 4)
def test_valid_studytime():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #studytime at high edge
    data={'G1':"20", 'G2':"20", 'Studytime':4, 'Absences':1}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

    #studytime at low edge
    data={'G1':"10", 'G2':"10", 'Studytime':1, 'Absences':40}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

    #studytime in between
    data={'G1':"10", 'G2':"10", 'Studytime':2, 'Absences':12}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

#when the input for absences is valid (integer in 0 <= n <= 93)
def test_valid_absences():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #absences at high edge
    data={'G1':"8", 'G2':"13", 'Studytime':1, 'Absences':93}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

    #absences at low edge
    data={'G1':"18", 'G2':"20", 'Studytime':3, 'Absences':0}
    response = client.get(url, query_string=data)
    assert response.status_code == 200

    #absences decimal
    data={'G1':"10", 'G2':"10", 'Studytime':2, 'Absences':66}
    response = client.get(url, query_string=data)
    assert response.status_code == 200


'''
Test Cases - Invalid Number (status=422)
'''
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

    #G1 non-numeric
    data={'G1':True, 'G2':"5", 'Studytime':1, 'Absences':43}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

#when the input for G2 scores are invalid (not between 0 and 20)
def test_invalid_G2():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #G2 too high
    data={'G1':"19", 'G2':"22", 'Studytime':4, 'Absences':0}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #G2 too low
    data={'G1':"19", 'G2':"-5", 'Studytime':4, 'Absences':0}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #G2 non-numeric
    data={'G1':"19", 'G2':'badinput', 'Studytime':1, 'Absences':43}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

#when the input for studytime is invalid (not an integer 1 <= n <= 4)
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

    #studytime non-numeric
    data={'G1':"10", 'G2':"10", 'Studytime':False, 'Absences':12}
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
