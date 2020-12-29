from authz import db
#app is called from the conftest.py 
def test_env(app):
    #our app was auth. so app.config is actually authz.config
    #the following line will seach for ENV in config file to see what value it has
    #then it it is not equal to "testing" it will asser an error
    assert app.config["ENV"] == "testing"

def test_database(app):
    with app.app_context():
        result = db.engine.execute("SELECT database();").first()
        assert result[0] == "testing"