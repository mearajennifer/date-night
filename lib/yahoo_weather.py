# Yahoo Weather API and OAuth

import time, uuid, urllib, urllib.parse, urllib.request
import hmac, hashlib
import os

# Basic info
url = 'https://weather-ydn-yql.media.yahoo.com/forecastrss'
method = 'GET'
app_id = os.environ['YAHOO_APP_ID']
consumer_key = os.environ['YAHOO_CONSUMER_KEY']
consumer_secret = os.environ['YAHOO_CONSUMER_SECRET']
concat = '&'
query = {'location': 'sunnyvale,ca', 'format': 'json'}
oauth = {
    'oauth_consumer_key': consumer_key,
    'oauth_nonce': uuid.uuid4().hex,
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_timestamp': str(int(time.time())),
    'oauth_version': '1.0'
}

# Prepare signature string (merge all params and SORT them)
merged_params = query.copy()
merged_params.update(oauth)
sorted_params = [k + '=' + urllib.parse.quote(merged_params[k], safe='')
                 for k in sorted(merged_params.keys())]
signature_base_str = method + concat + urllib.parse.quote(url, safe='') + concat + urllib.parse.quote(concat.join(sorted_params), safe='')

# Generate signature
composite_key = urllib.parse.quote(consumer_secret, safe='') + concat
oauth_signature = hmac.new(b'composite_key', b'signature_base_str', hashlib.sha1).digest()

# Prepare Authorization header
oauth['oauth_signature'] = oauth_signature
auth_header = 'OAuth ' + ', '.join(['{}="{}"'.format(k, v) for k, v in oauth.items()])

# Send request
url = url + '?' + urllib.parse.urlencode(query)
request = urllib.request.Request(url)
request.add_header('Authorization', auth_header)
request.add_header('Yahoo-App-Id', app_id)
response = urllib.request.urlopen(request).read()
print(response)
