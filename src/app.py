from flask import Flask, render_template, request
import requests

from uagents import Agent, Bureau, Context, Model

app = Flask(__name__,template_folder='frontEnd')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        email = request.form['email']
        location = request.form['location']
        max_temperature = request.form['maxTemperature']
        min_temperature = request.form['minTemperature']

        data = {
            'location': location,
            'min_temp': min_temperature,
            'max_temp': max_temperature,
        }

        agent_script_url = 'http://localhost:8000' 
        response = requests.post(agent_script_url, json=data)

        if response.status_code == 200:
            return render_template('results.html', result='Agent triggered successfully')
        else:
            return render_template('results.html', result='Failed to trigger agent')

if __name__ == '__main__':
    app.run(debug=True)