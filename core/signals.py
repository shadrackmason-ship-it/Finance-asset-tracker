import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger('masontrack')


def _get_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def _notify_owner(subject, body):
    owner = getattr(settings, 'OWNER_EMAIL', '')
    if not owner:
        return
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [owner], fail_silently=True)
    except Exception:
        pass


@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    ip = _get_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '')[:120]
    logger.info('LOGIN_SUCCESS user=%s ip=%s ua=%s', user.username, ip, ua)
    _notify_owner(
        f'[MasonTrack] Login — {user.username}',
        f'User "{user.username}" just signed in.\n\nIP: {ip}\nBrowser: {ua}\n\nIf this was not you, secure your admin immediately.'
    )


@receiver(user_login_failed)
def on_login_failed(sender, credentials, request, **kwargs):
    ip = _get_ip(request)
    username = credentials.get('username', 'unknown')
    ua = request.META.get('HTTP_USER_AGENT', '')[:120]
    logger.warning('LOGIN_FAILED user=%s ip=%s ua=%s', username, ip, ua)
    _notify_owner(
        f'[MasonTrack] ⚠️ Failed Login Attempt — {username}',
        f'Failed login attempt on your platform.\n\nUsername tried: {username}\nIP: {ip}\nBrowser: {ua}\n\nIf you see many of these, an attacker may be targeting your app.'
    )


@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    if user:
        ip = _get_ip(request)
        logger.info('LOGOUT user=%s ip=%s', user.username, ip)
