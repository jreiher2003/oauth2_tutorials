#!/usr/bin/python
from flask import Flask, redirect, request, flash
# Import required packages, including the oauthlib package discussed earlier in the tutorial
import oauth2, urlparse, hmac, hashlib, urllib, urllib3

app = Flask(__name__)

# Set the consumer key and secret
CONSUMER_KEY = 'W1YV441FkQls40s1VBZ3TvulQ'
CONSUMER_SECRET = 'zLz2VO9FGPjBv3BDy3z7KtXUx3gP2Y6OcxkSiw4mzZ2o7C3HJU'
CONSUMER = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

def twitter_request_token(): 
    resp, content = oauth2.Client(CONSUMER).request('https://api.twitter.com/oauth/request_token', "GET")
    request_token = dict(urlparse.parse_qsl(content))
    return request_token

request_token = twitter_request_token()

@app.route("/")
def index():
    global request_token
    # Redirect user to authorization page, encapsulating request token in URL
    return redirect("%s?oauth_token=%s" % ('https://api.twitter.com/oauth/authorize', request_token['oauth_token']))


@app.route("/twitter_connect")
def twit():
    global request_token
    
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(request.args.get('oauth_verifier'))
    # Create a new oauth2.Client object, wrapping both the consumer and token objects
    client = oauth2.Client(CONSUMER, token)
    # Call the Twitter access token endpoint
    resp, content = client.request('https://api.twitter.com/oauth/access_token', "POST")
    # Create a standard dictionary from the response body, using parse_qsl as a convenience to parse the query string in the response
    access_token = dict(urlparse.parse_qsl(content))


    screen_name='programmableweb'
    url='https://api.twitter.com/1.1/statuses/update.json'
    status="Hello World @%s!" % screen_name
    manager = urllib3.PoolManager()

    # Set the parameters required to build the base of the signature, using a dictionary for convenience
    parameters = {
        "oauth_consumer_key": CONSUMER_KEY,
        "oauth_nonce":  hashlib.sha1(str(random.random)).hexdigest(),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": access_token['oauth_token'],
        "oauth_version": "1.0",
        "status": status
    }

    # Build the string that forms the base of the signature, iterating through the dictionary and using the key/values in the string
    base_string = "%s&%s&%s" % (method,urllib.quote(url,""),urllib.quote('&'.join(sorted("%s=%s" % (key,value)
                    for key,value in parameters.iteritems())),""))

    # Create the signature using signing key composed of consumer secret and token secret obtained during 3-legged dance
    signature = hmac.hmac.new("%s&%s" % (urllib.quote(CONSUMER_SECRET,""),urllib.quote(access_token['oauth_token_secret'],"")),
                    base_string,hashlib.sha1)

    # Add result to parameters and create a string in required format for header
    parameters['oauth_signature'] = signature.digest().encode("base64").rstrip('\n')
    auth_header = 'OAuth %s' % ', '.join(sorted('%s="%s"' % (urllib.quote(key,""),urllib.quote(value,""))
                    for key,value in parameters.iteritems() if key != 'status'))

    # Set HTTP headers                
    http_headers={"Authorization": auth_header, 'Content-Type': 'application/x-www-form-urlencoded'}

    # Send the request
    response = manager.urlopen("POST", url, headers=headers,body=status)

    # Set messages that will be used in modal dialogs
    if response.status == 200:
        flash("Tweet sent mentioning @%s" % screen_name)
    else:
        flash("Error sending tweet: %s" % response.data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004)