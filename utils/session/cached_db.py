from qsessions.backends.cached_db import SessionStore as CachedDBStore

KEY_PREFIX: str = "utils.session.cached_db"


class AnonymousSessionStore(CachedDBStore):
    """
    Implements cached, database backed sessions, with a foreign key to User.
    It also stores IP and User Agent.
    """
    cache_key_prefix = KEY_PREFIX

    def __init__(self, session_key=None, user_agent=None, ip=None):
        self.modified = False
        self.user_agent = user_agent[:300] if user_agent else user_agent
        self.ip = ip
        super(AnonymousSessionStore, self).__init__(session_key)

    @classmethod
    def get_model_class(cls):
        from .models import AnonymousSession
        return AnonymousSession

    def save(self, must_create=False):
        super(AnonymousSessionStore, self).save(must_create)


