from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2

DDP_SCOPE = 'https://ddp.googleapis.com/api/ddp'
DDP_REDIRECT_URL = 'urn:ietf:wg:oauth:2.0:oob'
API_CREDENTIAL_FILE = '.ddp_credentials'


class Auth:
    def __init__(self):
        self.storage = Storage(API_CREDENTIAL_FILE)

    def authorize_url(self, client_id, client_secret):
        flow = OAuth2WebServerFlow(client_id=client_id,
                                   client_secret=client_secret,
                                   scope=DDP_SCOPE,
                                   redirect_uri=DDP_REDIRECT_URL,
                                   access_type='offline')

        return flow.step1_get_authorize_url()

    def authorise(self, client_id, client_secret, auth_code):
        flow = OAuth2WebServerFlow(client_id=client_id,
                                   client_secret=client_secret,
                                   scope=DDP_SCOPE,
                                   redirect_uri=DDP_REDIRECT_URL)

        credentials = flow.step2_exchange(auth_code)
        self.storage.put(credentials)

        return credentials

    def get_credentials(self):
        credentials = self.storage.get()

        if credentials.access_token_expired:
            http = httplib2.Http()
            credentials.refresh(http)

        return credentials
