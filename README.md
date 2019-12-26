# SlackPush - Logging to Slack made easy

SlackPush provides a wrapper on requests to push messages, logs, exceptions and attachments to slack. 
It also supports basic formating: Bold and Perforated. 

## Installation
To get started, clone the repository and run
> pip install slackpush

## Usage
1. Import the SlackPush object.

``` from slackpush import SlackPush```

2. Initialise SlackPush object with a webhook_url and channel to be posted in. To know more about incoming webhooks read [here](https://api.slack.com/messaging/webhooks).

```slackpush = SlackPush(webhook_url= <your webhook_url>, channel=<your channel>)```

3. Push messages/ logs using `send_message` method.

```slackpush.send_message('It is up and running')```

4. Similarly you can push specific exceptions as alerts to slack using `send_exception` method. This pushes the whole stack trace of the error to slack.

```
try:
    < your code here>
except Exception as e:
    slackpush.send_exception(e)
```

5. To send attachments to slack, you need to pass Slack OAuth token. More details can be found [here](https://api.slack.com/tokens). 

**Note:** See that the token has relevant persmissions to post the attachement

To add token to the object use `add_token` method. To send an attachment to Slack:

```slackpush.send_attachment(<path to attachment>)```

