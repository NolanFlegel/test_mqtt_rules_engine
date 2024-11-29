# test_mqtt_rules_engine
Determine a client’s eligibility for the Winter Supplement

# MQTT Python Project Setup
### Prerequisites
- Python 3.9+ installed
- pyenv installed (for setting up a Python virtual environment)
- pip installed and updated (https://pip.pypa.io/en/stable/installation/)

## Setup Instructions (Linux - Bash/Zsh)
1. Clone the Repository

    `git clone https://github.com/NolanFlegel/test_mqtt_rules_engine.git`

2. Create Virtual Environment (Optional - install alternative python versions)
    ```
    pyenv install 3.12.5 
    pyenv virtualenv 3.12.5 mqtt
    pyenv activate mqtt
    ```
3. Install Dependencies

    `pip install -r requirements.txt`

4. Configure Environment Variables
    
    create a .env file in the project root directory

    `touch .env`

    Add the following environment variables (replace placeholder values)
    ```
    MQTT_BROKER = 'test.mosquitto.org'
    MQTT_PORT = 1833
    MQTT_TOPIC_ID = '' 
    ```
5. Run the MQTT rules engine

    ```python rule_engine.py```

## Testing
The repository utilizes github actions to run the test suite on commits or PRs into `main` branch. 
These actions can be manually triggered on the Actions Tab in GitHub or tests can be run manually using the command `pytest tests` in the project root directory.

## Notes
- Deactivate python virtual environment with `pyenv deactivate`
