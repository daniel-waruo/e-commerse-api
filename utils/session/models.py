import django.core.cache
from django.db import models
from .cached_db import CheckoutSessionStore
from django.conf import settings
from qsessions.models import (
    SessionManager as BaseSessionManager,
    Session as AbstractBaseSession
)
from django.utils import timezone


class CheckoutSessionQuerySet(models.QuerySet):
    def delete(self):
        """
        Delete sessions from both DB and cache (first cache, then DB)
        """
        django.core.cache.caches[settings.ANONYMOUS_SESSION_CACHE_ALIAS].delete_many(CheckoutSessionStore.cache_key_prefix + s.session_key for s in self)
        return super(CheckoutSessionQuerySet, self).delete()


class CheckoutSessionManager(BaseSessionManager.from_queryset(CheckoutSessionQuerySet)):
    use_in_migrations = True


class CheckoutSession(AbstractBaseSession):
    objects = CheckoutSessionManager()

    @classmethod
    def get_session_store_class(cls):
        return CheckoutSessionStore

    def save(self, *args, **kwargs):
        # FIXME: find a better solution for `created_at` field which does not need an extra query.
        # https://code.djangoproject.com/ticket/17654
        if CheckoutSession.objects.filter(pk=self.pk).exists():
            self.created_at = CheckoutSession.objects.get(pk=self.pk).created_at
        else:
            self.created_at = timezone.now()
        super(CheckoutSession, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete session from both DB and cache (first cache, then DB)
        """
        django.core.cache.caches[settings.ANONYMOUS_SESSION_CACHE_ALIAS].delete(
            CheckoutSessionStore.cache_key_prefix + self.session_key
        )
        return super(CheckoutSession, self).delete(*args, **kwargs)
