import django.core.cache
from django.db import models
from .cached_db import AnonymousSessionStore
from django.conf import settings
from qsessions.models import (
    SessionManager as BaseSessionManager,
    Session as AbstractBaseSession
)
from django.utils import timezone


class AnonymousSessionQuerySet(models.QuerySet):
    def delete(self):
        """
        Delete sessions from both DB and cache (first cache, then DB)
        """
        django.core.cache.caches[settings.ANONYMOUS_SESSION_CACHE_ALIAS].delete_many(AnonymousSessionStore.cache_key_prefix + s.session_key for s in self)
        return super(AnonymousSessionQuerySet, self).delete()


class AnonymousSessionManager(BaseSessionManager.from_queryset(AnonymousSessionQuerySet)):
    use_in_migrations = True


class AnonymousSession(AbstractBaseSession):
    objects = AnonymousSessionManager()

    @classmethod
    def get_session_store_class(cls):
        return AnonymousSessionStore

    def save(self, *args, **kwargs):
        # FIXME: find a better solution for `created_at` field which does not need an extra query.
        # https://code.djangoproject.com/ticket/17654
        if AnonymousSession.objects.filter(pk=self.pk).exists():
            self.created_at = AnonymousSession.objects.get(pk=self.pk).created_at
        else:
            self.created_at = timezone.now()
        super(AnonymousSession, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete session from both DB and cache (first cache, then DB)
        """
        django.core.cache.caches[settings.ANONYMOUS_SESSION_CACHE_ALIAS].delete(
            AnonymousSessionStore.cache_key_prefix + self.session_key
        )
        return super(AnonymousSession, self).delete(*args, **kwargs)
