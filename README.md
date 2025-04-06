# Tartabit IoT Bridge Onboarding Demo
The purpose of this project is to demonstrate how to achieve a simple "data as a service" offering.

## Building & Running
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
.venv/bin/flask run
```

Open your browser and navigate to `http://localhost:5000/` to see the demo in action.

## How it works
The application uses the Tartabit IoT Bridge Python client to make API calls to a bridge instance.
You can onboard new customers, and check the status of customer accounts.

## Support
For additional support, visit https://support.tartabit.com or email support@tartabit.com.
