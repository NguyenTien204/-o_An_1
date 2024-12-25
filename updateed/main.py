from flask import Flask

app = Flask(__name__)
app.secret_key = '1234'

def setup_routes():
    from routes import setup_routes  # Lazy import 
    setup_routes(app)

if __name__ == '__main__':
    setup_routes()  
    app.run(debug=True)