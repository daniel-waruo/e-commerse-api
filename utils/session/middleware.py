import time
from importlib import import_module

from django.conf import settings
from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.middleware import (
    SessionMiddleware as DjSessionMiddleware
)
from django.core.exceptions import SuspiciousOperation
from django.utils.cache import patch_vary_headers
from django.utils.http import http_date
from ipware.ip import get_real_ip, get_ip

from .models import AnonymousSession


class AnonymousSessionMiddleware(DjSessionMiddleware):

    def __init__(self, get_response=None):
        self.get_response = get_response
        engine = import_module(settings.ANONYMOUS_SESSION_ENGINE)
        self.AnonymousSessionStore = engine.AnonymousSessionStore
        super().__init__(get_response)

    def process_request(self, request):
        # get your session key
        session_key = request.COOKIES.get(
            settings.ANONYMOUS_SESSION_NAME
        )
        if 'anonymous-session' in request.headers:
            session_key = request.headers['anonymous-session']
        # set cart session in
        request.anonymous_session = self.AnonymousSessionStore(
            ip=get_real_ip(request) or get_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            session_key=session_key
        )

        if not request.user.is_authenticated:
            if not request.anonymous_session.session_key:
                request.anonymous_session.ip = get_real_ip(request) or get_ip(request)
                request.anonymous_session.user_agent = request.META.get('HTTP_USER_AGENT', '')
                request.anonymous_session.save()
            else:
                if not AnonymousSession.objects.filter(session_key=session_key).exists():
                    request.anonymous_session.save()

    def process_response(self, request, response):
        """
        If request.anonymous_session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie or delete
        the session cookie if the session has been emptied.
        """
        try:
            accessed = request.anonymous_session.accessed
            modified = request.anonymous_session.modified
            empty = request.anonymous_session.is_empty()
        except AttributeError:
            pass
        else:
            # First check if we need to delete this cookie.
            # The session should be deleted only if the session is entirely empty
            if settings.ANONYMOUS_SESSION_NAME in request.COOKIES and empty:
                response.delete_cookie(
                    settings.ANONYMOUS_SESSION_NAME,
                    path=settings.SESSION_COOKIE_PATH,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                )
            else:
                if accessed:
                    patch_vary_headers(response, ('Cookie',))
                if (modified or settings.SESSION_SAVE_EVERY_REQUEST) and not empty:
                    if request.anonymous_session.get_expire_at_browser_close():
                        max_age = None
                        expires = None
                    else:
                        max_age = request.anonymous_session.get_expiry_age()
                        expires_time = time.time() + max_age
                        expires = http_date(expires_time)
                    # Save the session data and refresh the client cookie.
                    # Skip session save for 500 responses, refs #3881.
                    if response.status_code != 500:
                        try:
                            request.anonymous_session.save()
                        except UpdateError:
                            raise SuspiciousOperation(
                                "The request's session was deleted before the "
                                "request completed. The user may have logged "
                                "out in a concurrent request, for example."
                            )
                        response.set_cookie(
                            settings.ANONYMOUS_SESSION_NAME,
                            request.anonymous_session.session_key, max_age=None,
                            expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                            path=settings.SESSION_COOKIE_PATH,
                            secure=getattr(settings, 'ANONYMOUS_SESSION_COOKIE_SECURE', None),
                            httponly=getattr(settings, 'ANONYMOUS_SESSION_COOKIE_HTTPONLY', None),
                            samesite=None,
                        )
        return response
