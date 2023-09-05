# Commute Companion

A Python script that provides you with a preview of your day, including commute ETA and weather information, using the Google Routes and Open-Meteo APIs. This information is sent via text message from a Twilio phone number to your cell phone.


Example message:

```
Your ETA to ****** is approximately 49 minutes today. 
The weather forecast for today is as follows:
- Max Temperature: 89.0°F
- Min Temperature: 68.3°F
- Precipitation Sum: 0.0 inch
- Precipitation Hours: 0.0 hours
- Max Precipitation Probability: 0%
- Max Windspeed: 9.6 mp/h

Have a great day!
```

The script is run as a lambda function on AWS Lambda, and scheduled by AWS EventBridge. 
Dependencies are listed in `requirements.txt`. When setting up the Lambda function, it's recommended to create a Lambda layer containing these dependencies for easy integration.
Environment variables are used to supply origin and destination coordinates, Twilio credentials, Google API key, and personal phone number.

To use this script, follow these steps:

1. Clone this repository to your local machine.
2. Deploy the script as a Lambda function on AWS Lambda.
3. ZIP a directory containing required dependencies and create a new Lambda layer using this ZIP.
4. Add newly created layer to Lambda function
5. Configure required environment variables
6. Schedule the Lambda function with AWS EventBridge using a cron expression to run on a recurring schedule.
