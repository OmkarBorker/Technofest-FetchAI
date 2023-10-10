from flask import Flask, render_template, request

app = Flask(__name__)

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

        # Perform some operation with the form data (you can replace this with your logic)
        result = f'Max temperature for {location}: {max_temperature}°C, Min temperature: {min_temperature}°C'

        # Render the result page with the obtained result
        return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
