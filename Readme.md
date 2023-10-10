# Temperature Alert Agent

This Temperature Alert Agent utilizes the uAgent library to connect to a free weather API, fetching real-time temperatures for a user-specified location. Users can set their preferred temperature range and location, and the agent will send an alert/notification when the current temperature in the chosen location falls below the minimum or exceeds the maximum threshold.

## Requirements

- [uAgent library](https://github.com/example/uAgent)
- Open weather API access
- User's preferred temperature range and location

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/temperature-alert-agent.git
   poetry install
   poetry shell
   ```

2. **Install the uAgent library:**
   ```bash
   pip install uAgent
   ```

3. **Obtain free weather API access:**
   - Visit [weather API provider](https://openweathermap.org/api) to obtain a free API key.

4. **Set up user's preferred temperature range and location:**
   - Open `main.py` and input the desired values when prompted (location, minimum temperature, maximum temperature, email).

5. **Create an environment file:**
   - Create a file named `.env` in the root directory.
   - Add the following information to the `.env` file:
     ```env
     OPW=your_weather_api_key
     SMTP_PASSWORD=your_smtp_password
     SENDER_EMAIL=your_sender_email
     ```

## Usage

1. **Run the Temperature Alert Agent:**
   ```bash
   python main.py
   ```

2. **Wait for the agent to fetch real-time temperatures:**
   - The agent will connect to the weather API and display the current temperature.

3. **Receive an alert/notification:**
   - If the temperature goes below the set minimum or above the set maximum, an email alert will be sent to the specified email address.

## Credits

- [uAgent library](https://github.com/example/uAgent)
- openweatherapi
