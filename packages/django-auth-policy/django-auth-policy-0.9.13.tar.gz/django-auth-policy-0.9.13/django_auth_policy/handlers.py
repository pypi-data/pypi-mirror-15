import logging
import warnings
import collections

from django.conf import settings
from django.utils.module_loading import import_string
from django.db import transaction
from django.core.exceptions import ValidationError

from django_auth_policy.models import LoginAttempt, PasswordChange

logger = logging.getLogger(__name__)


class PasswordStrengthPolicyHandler(object):
    """ Runs all policies related to password strength requirements
    Raises a ValidationError when a password doesn't comply
    """
    _policies = collections.OrderedDict()
    policy_texts = []

    def __init__(self):
        if self._policies:
            return

        for policy_path, kwargs in settings.PASSWORD_STRENGTH_POLICIES:
            policy_class = import_string(policy_path)
            policy = policy_class(**kwargs)

            self._policies[policy_path] = policy

            if policy.show_policy and policy.policy_text:
                self.policy_texts.append({
                    'text': policy.policy_text,
                    'caption': policy.policy_caption,
                })

    def get_policy(self, policy_path):
        return self._policies[policy_path]

    def validate(self, password, user=None):
        """ Validate password strength against all password policies.
        One should also provide the user (when available) that (will) use
        this password.
        Policies will raise a ValidationError when the password doesn't comply
        """
        for pol in self._policies.values():
            pol.validate(password, user)


password_strength_policy_handler = PasswordStrengthPolicyHandler()


class PasswordChangePolicyHandler(object):
    """ Runs all policies related to enforced password changes
    Raises a ValidationError when a user is enforced to change its password
    """
    _policies = collections.OrderedDict()
    policy_texts = []

    def __init__(self):
        if self._policies:
            return

        for policy_path, kwargs in settings.PASSWORD_CHANGE_POLICIES:
            policy_class = import_string(policy_path)
            policy = policy_class(**kwargs)

            self._policies[policy_path] = policy

    def get_policy(self, policy_path):
        return self._policies[policy_path]

    def validate(self, user):
        try:
            last_pw_change = PasswordChange.objects.filter(
                user=user, successful=True).order_by('-id')[0]
        except IndexError:
            last_pw_change = None

        for pol in self._policies.values():
            pol.validate(last_pw_change)

    def update_session(self, request, user):
        """ Called directly after successful authentication
        """
        if not hasattr(request, 'session'):
            return

        try:
            self.validate(user)
        except ValidationError as exc:
            if request.session.get('password_change_enforce') != exc.code:
                logger.info(u'User %s must change password; %s',
                            user, exc.code)
            request.session['password_change_enforce'] = exc.code
            request.session['password_change_enforce_msg'] = \
                unicode(exc.message)
        else:
            request.session['password_change_enforce'] = False
            request.session['password_change_enforce_msg'] = None


password_change_policy_handler = PasswordChangePolicyHandler()


class AuthenticationPolicyHandler(object):
    """ Runs all policies related to authentication
    Raises a ValidationError when an authentication attempt does not comply
    """
    _policies = collections.OrderedDict()
    policy_texts = []

    def __init__(self):
        if self._policies:
            return

        for policy_path, kwargs in settings.AUTHENTICATION_POLICIES:
            policy_class = import_string(policy_path)
            policy = policy_class(**kwargs)

            self._policies[policy_path] = policy

    def get_policy(self, policy_path):
        return self._policies[policy_path]

    def pre_auth_checks(self, username, password, remote_addr, host):
        """ Policy checks before a user is authenticated
        No `User` instance is available yet

        Raises ValidationError for failed login attempts
        On success it returns a LoginAttempt instance

        `username` must be a string that uniquely identifies a user.
        """
        logger.info('Authentication attempt, username=%s, address=%s',
                    username, remote_addr)

        with transaction.atomic():
            username_len = LoginAttempt._meta.get_field('username').max_length
            hostname_len = LoginAttempt._meta.get_field('hostname').max_length
            attempt = LoginAttempt.objects.create(
                username=username[:username_len] if username else '-',
                source_address=remote_addr,
                hostname=host[:hostname_len],
                successful=False,
                lockout=True)

        for pol in self._policies.values():
            pol.pre_auth_check(attempt, password)

        return attempt

    def post_auth_checks(self, attempt):
        """ Policy checks after the user has been authenticated.
        The attempt must now have a `user` instance set.

        Raises ValidationError for failed login attempts.
        """
        assert attempt.user is not None

        for pol in self._policies.values():
            pol.post_auth_check(attempt)

        return attempt

    def auth_success(self, attempt):
        """ Run this when authentication was successful, i.e. after
        `post_auth_checks`.
        """
        logger.info(u'Authentication success, username=%s, address=%s',
                    attempt.username, attempt.source_address)

        with transaction.atomic():
            attempt.successful = True
            attempt.lockout = False
            attempt.save()

        for pol in self._policies.values():
            pol.auth_success(attempt)

        return attempt


authentication_policy_handler = AuthenticationPolicyHandler()
