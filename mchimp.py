from flask import Flask, render_template, request
import requests
import json
import urllib
import mailchimp

# Uncomment if you want logging
# import httplib as http_client
# import logging

# http_client.HTTPConnection.debuglevel = 1

# logging.basicConfig() 
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

app = Flask(__name__)

# app.debug = True

OAUTH_clientID = "xxxxxxxx"
OAUTH_client_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

AUTHORIZE_URI = "https://login.mailchimp.com/oauth2/authorize"
ACCESS_TOKEN_URI = "https://login.mailchimp.com/oauth2/token"
REDIRECT_URI = "http://127.0.0.1:5000/oauth"
METADATA_URI = "https://login.mailchimp.com/oauth2/metadata"

API_ENDPOINT = "https://us10.api.mailchimp.com/2.0/"

def authorize_url(auth_url, client_id, redirect_uri):
    params = ["response_type=code", "client_id=" + client_id, "redirect_uri=" + redirect_uri]
    url_params = reduce(lambda acc, x: acc + '&' + x, params)
    return auth_url + '?' + url_params

@app.route("/")
def hello():
    auth_url = authorize_url(AUTHORIZE_URI, OAUTH_clientID, REDIRECT_URI)
    return render_template('index.html', authorize_url = auth_url)

@app.route("/oauth")
def oauth_redirect():
    code = request.args.get('code')
    request_obj = [
                   ('grant_type', 'authorization_code'),
                   ('client_id', OAUTH_clientID),
                   ('client_secret', OAUTH_client_secret),
                   ('code', code),
                   ('redirect_uri', REDIRECT_URI)
                   ]
    data = reduce(lambda acc, x: acc + x[0] + '=' + x[1] + '&', request_obj, '')[:-1]
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(ACCESS_TOKEN_URI, data=data, headers = headers)
    response_json = response.json()
    token = response_json['access_token'] 
    r = meta_mailchimp_api_info(METADATA_URI, token)
    dc = r['dc']
    api_key = token + '-' + dc #Can store the api_key in db
    rest_api(api_key)
    return code

def meta_mailchimp_api_info(url, token):
    headers = {'Authorization': 'OAuth ' + token }
    response = requests.get(url, headers = headers)
    return response.json()

def rest_api(api_key):
    """
    api_key: API key
    """
    mc = mailchimp.Mailchimp(api_key)
    print mc.lists.list()
    return mc.lists.list()

if __name__ == '__main__':
    app.run()
