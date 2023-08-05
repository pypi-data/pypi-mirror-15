from requests.auth import AuthBase


class BroodBearerTokenAuth(AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer {0}'.format(self.token)
        return request
