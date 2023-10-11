from flask import Flask, render_template, request,jsonify
import json
import requests
from models.models import Message

storage = "src/data/data.json"

app = Flask(__name__,template_folder='frontEnd')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
async def submit():
    if request.method == 'POST':
        email = request.form['email']
        location = request.form['location']
        max_temperature = request.form['maxTemperature']
        min_temperature = request.form['minTemperature']

        data = {
            'location': location,
            'min_temp': min_temperature,
            'max_temp': max_temperature,
            'email' : email
        }
        print(data)
        write_to_json(storage,data)

        return render_template('results.html', result='Agent triggered successfully')
    

def write_to_json(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error writing to JSON file: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)