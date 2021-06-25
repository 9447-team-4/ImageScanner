from __future__ import print_function
import time
import os
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

# Configure API key authorization: AccessToken
configuration = swagger_client.Configuration()
configuration.api_key['access_token'] = os.getenv('GITEA_TOKEN')
# Host
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['access_token'] = 'Bearer'
# Configure API key authorization: AuthorizationHeaderToken
configuration = swagger_client.Configuration()
configuration.api_key['Authorization'] = os.getenv('GITEA_TOKEN')
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'
# Configure HTTP basic authorization: BasicAuth
configuration = swagger_client.Configuration()
configuration.username = os.getenv('GITEA_USERNAME')
configuration.password = os.getenv('GITEA_PASSWORD')
# Configure API key authorization: SudoHeader
configuration = swagger_client.Configuration()
configuration.api_key['Sudo'] = os.getenv('GITEA_TOKEN')
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Sudo'] = 'Bearer'
# Configure API key authorization: SudoParam
configuration = swagger_client.Configuration()
configuration.api_key['sudo'] = os.getenv('GITEA_TOKEN')
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['sudo'] = 'Bearer'
# Configure API key authorization: TOTPHeader
configuration = swagger_client.Configuration()
configuration.api_key['X-GITEA-OTP'] = os.getenv('GITEA_TOKEN')
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-GITEA-OTP'] = 'Bearer'
# Configure API key authorization: Token
configuration = swagger_client.Configuration()
configuration.api_key['token'] = os.getenv('GITEA_TOKEN')
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['token'] = 'Bearer'

# Setting the client api with custom host to be the default api
configuration.host = f"http://{os.getenv('GITEA_HOST')}:{os.getenv('GITEA_PORT')}/api/v1"
api_client = swagger_client.ApiClient(configuration=configuration)


