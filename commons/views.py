from asyncio import new_event_loop, coroutine, get_event_loop

from django.http import HttpRequest
from rest_framework.request import Request
from rest_framework.views import APIView


class AsyncAPIView(APIView):

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        """
        Call request handler using event loop. The rest of the implementation
        is same as APIView dispatch().
        """
        request = self.initialize_request(request, *args, **kwargs)

        self.args = args
        self.kwargs = kwargs
        self.request = request
        self.headers = self.default_response_headers

        try:
            self.initial(request, *args, **kwargs)
            handler = self._get_handler(request)
            if handler is not None:
                future_response = handler(request, *args, **kwargs)
                loop = new_event_loop()
                response = loop.run_until_complete(future_response)
            else:
                response = self.http_method_not_allowed(request, *args, **kwargs)
        except Exception as e:
            response = self.handle_exception(e)

        self.response = self.finalize_response(request, response, *args, **kwargs)

        return self.response

    def _get_handler(self, request: Request) -> coroutine:
        method = request.method.lower()
        handler = getattr(self, method, None)
        return handler
