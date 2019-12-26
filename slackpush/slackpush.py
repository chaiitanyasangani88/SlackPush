import os
import json
import requests
import traceback


class SlackPush:

    def __init__(self, webhook_url, channel):
        self.webhook_url = webhook_url
        self.channel = channel
        self.token = None
        self.auth_url = 'https://slack.com/api/auth.test'
        self.file_upload_url = 'https://slack.com/api/files.upload'

    def bold_text(self, text):
        """
        Make the input text Bold formatted for pushing to Slack
        :param text: String
        :return: String; Formatted to be bold
        """
        return '*' + text + '*'

    def perforate_text(self, text):
        """
        Make the input text Perforated formatted for pushing to Slack
        :param text: String
        :return: String; Formatted to be perforated
        """
        return '```' + text + '```'

    def send_message(self, text):
        """
        Pushes messages to slack using the webhook_url provided
        :param text: String; Message to be sent
        """
        headers = {'Content-type': 'application/json'}
        response = requests.post(data=json.dumps({"text": text, "channel": self.channel}),
                                 url=self.webhook_url,
                                 headers=headers)
        if response.status_code == 200:
            print('Message posted to slack')
        else:
            print(f'Message sending failed with status: {response.status_code}')

    def send_exception(self, exception):
        """
        Pushes Exception with whole stack trace to slack using the webhook_url provided
        :param exception: Exception; Pass Exception to push the whole stack trace to slack
        :return:
        """
        if isinstance(exception, Exception):
            exception_traceback = ''.join(traceback.format_tb(exception.__traceback__))
            self.send_message(self.perforate_text(exception_traceback))
        else:
            print('Only Exceptions are to be passed in this method')

    def validate_token(self, token):
        """
        Validate the token issued by Slack
        :param token: String; OAuth Token issued from Slack to push attachments
        :return: boolean; If the token is valid or not
        """
        if token is not None:
            headers = {'Content-type': 'application/json', 'Authorization': f'Bearer {token}'}
            response = requests.post(self.auth_url, headers=headers).json()
            if response['ok']:
                print('Token Valid')
                return response['ok']
            else:
                print(response['error'])
                return response['ok']
        else:
            raise Exception('Token not added. Use add_token method')

    def add_token(self, token):
        """
        Adds token to  SlackPush object
        :param token: String;
        """
        self.token = token

    def send_attachment(self, attachment_path):
        """
        Pushes attachement to slack using the OAuth token
        :param attachment_path: dir path; Path to the attachment to be pushed to Slack
        """
        if self.validate_token(self.token):
            attachment_type = os.path.splitext(attachment_path)[1]
            attachment_name = os.path.split(attachment_path)[1]
            print(f'sending {attachment_name} of file type {attachment_type}')

            request_params = {'filename': attachment_name, 'token': self.token, 'channels': [self.channel], 'pretty': 1}
            attachment_payload = {'file': (attachment_name, open(attachment_path, 'rb'), attachment_type[1:])}

            attachment_upload_response = requests.post(url=self.file_upload_url,
                                                       params=request_params,
                                                       files=attachment_payload).json()
            if attachment_upload_response['ok']:
                print('Attachment sent to slack')
            else:
                print(attachment_upload_response['error'])
        else:
            raise Exception("Valid token needed to send attachments")
