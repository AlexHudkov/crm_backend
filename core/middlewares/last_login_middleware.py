from django.utils.timezone import now, localtime


class UpdateLastLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            local_time = localtime(now())
            request.user.last_login = local_time
            request.user.save(update_fields=["last_login"])

        return response
