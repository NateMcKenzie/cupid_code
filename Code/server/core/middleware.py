import requests
import os
from django.http import StreamingHttpResponse


def asset_proxy_middleware(next):
    def middleware(request):
        # checking for .
        if '.' in request.path:
            # Proxy request to asset server
            asset_url = os.environ.get('ASSET_URL')
            request_path = request.path.replace('/static', '')
            response = requests.get(f'{asset_url}{request_path}', stream=True)

            # Stream response
            return StreamingHttpResponse(
                response.raw,
                content_type=response.headers.get('content-type'),
                status=response.status_code,
                reason=response.reason
            )

        # call next middleware
        return next(request)

    return middleware
