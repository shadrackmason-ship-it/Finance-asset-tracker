class StealthMiddleware:
    """
    Removes all headers that reveal the tech stack.
    No one can tell this is Django, Python, or what server it runs on.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Strip fingerprint headers
        for header in ['X-Powered-By', 'Server', 'X-Django-Version', 'X-Runtime']:
            if header in response:
                del response[header]
        # Add generic server header
        response['Server'] = 'nginx'
        return response
