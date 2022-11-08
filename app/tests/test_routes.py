from flask import Flask

from app.handlers.routes import configure_routes

def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'to interact with this API, use the predict route'

'''
Test Cases - Valid Number and Format (status=200)
'''
#when the input for failures is valid (integer in 0 <= n <= 3)
def test_valid_failures():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #failures at high edge
    data={'failures':3, 'absences':11, 'G1':19, 'G2':2}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

    #failures at low edge
    data={'failures':0, 'absences':40, 'G1':10, 'G2':10}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

    #failures in between
    data={'failures':1, 'absences':12, 'G1':10, 'G2':10}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

#when the input for absences is valid (integer in 0 <= n <= 93)
def test_valid_absences():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #absences at high edge
    data={'failures':1, 'absences':93, 'G1':8, 'G2':13}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

    #absences at low edge
    data={'failures':1, 'absences':0, 'G1':18, 'G2':20}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

    #absences decimal
    data={'failures':0, 'absences':66, 'G1':10, 'G2':10}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

#when the input for G1 scores is valid (between 0 and 20)
def test_valid_G1():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #G1 at high edge
    data={'failures':1, 'absences':43, 'G1':20, 'G2':5}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

    #G1 at low edge
    data={'failures':0, 'absences':4, 'G1':0, 'G2':3}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

    #G1 in between
    data={'failures':1, 'absences':71, 'G1':8, 'G2':17}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

#when the input for G2 scores are valid (not between 0 and 20)
def test_valid_G2():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #G2 at high edge
    data={'failures':2, 'absences':7, 'G1':19, 'G2':20}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

    #G2 at low edge
    data={'failures':0, 'absences':88, 'G1':18, 'G2':0}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()

    #G2 in between
    data={'failures':0, 'absences':11, 'G1':2, 'G2':6}
    response = client.get(url, query_string=data)
    assert response.status_code == 200
    assert 'high_quality' in response.get_json()


'''
Test Cases - Invalid Number (status=422)
'''
#when the input for failures is invalid (not an integer between 0 and 3)
def test_invalid_failures():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #failures too high (>4)
    data={'failures':5, 'absences':11, 'G1':19, 'G2':2}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #failures too low
    data={'failures':-1000, 'absences':40, 'G1':10, 'G2':10}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #failures decimal
    data={'failures':1.5, 'absences':12, 'G1':10, 'G2':10}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #failures non-numeric
    data={'failures':'hello', 'absences':12, 'G1':10, 'G2':10}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

#when the input for absences is invalid (not an integer between 0 and 93)
def test_invalid_absences():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #absences too high (>93)
    data={'failures':0, 'absences':100, 'G1':8, 'G2':13}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #absences too low
    data={'failures':2, 'absences':-4, 'G1':18, 'G2':20}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #absences decimal
    data={'failures':1, 'absences':15.2, 'G1':10, 'G2':10}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #absences non-numeric
    data={'failures':1, 'absences':'123abc', 'G1':10, 'G2':10}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

#when the input for G1 scores are invalid (not between 0 and 20)
def test_invalid_G1():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #G1 too high
    data={'failures':0, 'absences':43, 'G1':21, 'G2':5}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #G1 too low
    data={'failures':0, 'absences':43, 'G1':-1, 'G2':5}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #G1 decimal
    data={'failures':0, 'absences':43, 'G1':10.001, 'G2':5}
    response = client.get(url, query_string=data)
    assert response.status_code == 422
    
    #G1 non-numeric
    data={'failures':0, 'absences':43, 'G1':True, 'G2':5}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

#when the input for G2 scores are invalid (not between 0 and 20)
def test_invalid_G2():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #G2 too high
    data={'failures':1, 'absences':0, 'G1':19, 'G2':22}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #G2 too low
    data={'failures':1, 'absences':3, 'G1':19, 'G2':-5}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #G2 decimal
    data={'failures':0, 'absences':43, 'G1':19, 'G2':0.123}
    response = client.get(url, query_string=data)
    assert response.status_code == 422

    #G2 non-numeric
    data={'failures':0, 'absences':43, 'G1':19, 'G2':'badinput'}
    response = client.get(url, query_string=data)
    assert response.status_code == 422


'''
Test Cases - Invalid Input Format (status=400)
'''
def test_data_format():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    #Data uses wrong feature names
    data={'failures':2, 'absences':11, 'G11':19, 'G22':2}
    response = client.get(url, query_string=data)
    assert response.status_code == 400

    #Data doesnt use all 4 feature names
    data={'failures':2, 'G1':19, 'G2':2}
    response = client.get(url, query_string=data)
    assert response.status_code == 400

    #Data given is None
    data={'failures':0, 'absences':3, 'G1':19, 'G2':None}
    response = client.get(url, query_string=data)
    assert response.status_code == 400