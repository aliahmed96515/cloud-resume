import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from visitor_counter.app import lambda_handler as visitor_handler
from contact_form.app import lambda_handler as contact_handler


# ── Visitor Counter Tests ──────────────────────────────

class TestVisitorCounter:

    def test_returns_200(self, mocker):
        mocker.patch('visitor_counter.app.table.update_item', return_value={
            'Attributes': {'count': 42}
        })
        response = visitor_handler({}, {})
        assert response['statusCode'] == 200

    def test_returns_count(self, mocker):
        mocker.patch('visitor_counter.app.table.update_item', return_value={
            'Attributes': {'count': 42}
        })
        response = visitor_handler({}, {})
        body = json.loads(response['body'])
        assert body['count'] == 42

    def test_has_cors_header(self, mocker):
        mocker.patch('visitor_counter.app.table.update_item', return_value={
            'Attributes': {'count': 1}
        })
        response = visitor_handler({}, {})
        assert response['headers']['Access-Control-Allow-Origin'] == '*'


# ── Contact Form Tests ─────────────────────────────────

class TestContactForm:

    def test_options_returns_200(self):
        event = {
            'requestContext': {'http': {'method': 'OPTIONS'}}
        }
        response = contact_handler(event, {})
        assert response['statusCode'] == 200

    def test_sends_email_successfully(self, mocker):
        mocker.patch('contact_form.app.ses.send_email', return_value={})
        event = {
            'requestContext': {'http': {'method': 'POST'}},
            'body': json.dumps({
                'name': 'Test User',
                'email': 'test@test.com',
                'message': 'Hello'
            })
        }
        response = contact_handler(event, {})
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['message'] == 'Email sent successfully'

    def test_missing_fields_returns_500(self, mocker):
        mocker.patch('contact_form.app.ses.send_email', return_value={})
        event = {
            'requestContext': {'http': {'method': 'POST'}},
            'body': json.dumps({'name': 'Test User'})
        }
        response = contact_handler(event, {})
        assert response['statusCode'] == 500