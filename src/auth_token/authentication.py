from rest_framework.authentication import TokenAuthentication


class QueryTokenAuthentication(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://www.example.com/?auth_token=<token_key>"

    :url: https://stackoverflow.com/a/29435607
    """

    def authenticate(self, request):
        # Check if 'token_auth' is in the request query params.
        # Give precedence to 'Authorization' header.
        if (
            "auth_token" in request.query_params
            and "HTTP_AUTHORIZATION" not in request.META
        ):
            return self.authenticate_credentials(request.query_params.get("auth_token"))
        else:
            return super(QueryTokenAuthentication, self).authenticate(request)
