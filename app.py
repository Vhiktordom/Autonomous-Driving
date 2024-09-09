from flask import Flask
from db_manager import DatabaseConnection
from simulations import DrivingSimulator
import routes

# Initialize the Flask application
app = Flask(__name__)


# Create an instance of the DrivingSimulator
simulator = DrivingSimulator()

# Register routes
routes.init_app(app, simulator)

if __name__ == '__main__':
    app.run(debug=True)