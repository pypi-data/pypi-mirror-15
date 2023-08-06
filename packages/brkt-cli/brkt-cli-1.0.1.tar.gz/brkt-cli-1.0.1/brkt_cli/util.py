# Copyright 2015 Bracket Computing, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# https://github.com/brkt/brkt-cli/blob/master/LICENSE
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and
# limitations under the License.
import abc
import base64
import logging
import re
import time
import uuid

from brkt_cli.validation import ValidationError

SLEEP_ENABLED = True
MAX_BACKOFF_SECS = 10


log = logging.getLogger(__name__)


class BracketError(Exception):
    pass


class Deadline(object):
    """Convenience class for bounding how long execution takes."""

    def __init__(self, secs_from_now, clock=time):
        self.deadline = clock.time() + secs_from_now
        self.clock = clock

    def is_expired(self):
        """Return whether or not the deadline has passed.

        Returns:
            True if the deadline has passed. False otherwise.
        """
        return self.clock.time() >= self.deadline


class RetryExceptionChecker(object):
    """ Abstract class, implemented by callsites that need custom
    exception checking for the retry() function.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_expected(self, exception):
        pass


def retry(function, on=None, exception_checker=None, timeout=15.0,
          initial_sleep_seconds=0.25):
    """ Retry the given function until it completes successfully.  Before
    retrying, sleep for initial_sleep_seconds. Double the sleep time on each
    retry.  If the timeout is exceeded or an unexpected exception is raised,
    raise the underlying exception.

    :param function the function that will be retried
    :param on a list of expected Exception classes
    :param exception_checker an instance of RetryExceptionChecker that is
        used to determine if the exception is expected
    :param timeout stop retrying if this number of seconds have lapsed
    :param initial_sleep_seconds
    """
    start_time = time.time()

    def _wrapped(*args, **kwargs):
        for attempt in xrange(1, 1000):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                now = time.time()

                expected = False
                if exception_checker and exception_checker.is_expected(e):
                    expected = True
                if on and e.__class__ in on:
                    expected = True

                if not expected:
                    raise
                if now - start_time > timeout:
                    log.error(
                        'Exceeded timeout of %s seconds for %s',
                        timeout,
                        function.__name__)
                    raise
                else:
                    time.sleep(initial_sleep_seconds * float(attempt))
    return _wrapped


def sleep(seconds):
    if SLEEP_ENABLED:
        time.sleep(seconds)


def add_brkt_env_to_brkt_config(brkt_env, brkt_config):
    """ Add BracketEnvironment values to the config dictionary
    that will be passed to the metavisor via userdata.

    :param brkt_env a BracketEnvironment object
    :param brkt_config a dictionary that contains configuration data
    """
    if brkt_env:
        if 'brkt' not in brkt_config:
            brkt_config['brkt'] = {}
        api_host_port = '%s:%d' % (brkt_env.api_host, brkt_env.api_port)
        hsmproxy_host_port = '%s:%d' % (
            brkt_env.hsmproxy_host, brkt_env.hsmproxy_port)
        brkt_config['brkt']['api_host'] = api_host_port
        brkt_config['brkt']['hsmproxy_host'] = hsmproxy_host_port


def get_domain_from_brkt_config(brkt_config):
    """Return the domain string from the api_host in the brkt_config.

    Raises ValidationError if it doesn't like brkt_config.
    """

    if not brkt_config or 'brkt' not in brkt_config:
        raise ValidationError('Invalid brkt_config: %s' % brkt_config)
    brkt_env = brkt_config['brkt']

    if 'api_host' not in brkt_env:
        raise ValidationError('api_host endpoint not in brkt_env: %s' %
                              brkt_env)
    # Remove the port string from api_host
    api_host = brkt_env['api_host'].split(':')[0]

    # Consider the domain to be everything after the first '.' in
    # the api_host.
    return api_host.split('.', 1)[1]


def add_token_to_brkt_config(identity_token, user_data):
    if 'brkt' not in user_data:
        user_data['brkt'] = {}
    user_data['brkt']['identity_token'] = identity_token


def make_nonce():
    """Returns a 32bit nonce in hex encoding"""
    return str(uuid.uuid4()).split('-')[0]


def validate_dns_name_ip_address(hostname):
    """ Verifies that the input hostname is indeed a valid
    host name or ip address

    :return True if valid, returns False otherwise
    """
    # ensure length does not exceed 255 characters
    if len(hostname) > 255:
        return False
    # remove the last dot from the end
    if hostname[-1] == ".":
        hostname = hostname[:-1]
    valid = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(valid.match(x) for x in hostname.split("."))


def append_suffix(name, suffix, max_length=None):
    """ Append the suffix to the given name.  If the appended length exceeds
    max_length, truncate the name to make room for the suffix.

    :return: The possibly truncated name with the suffix appended
    """
    if not suffix:
        return name
    if max_length:
        truncated_length = max_length - len(suffix)
        name = name[:truncated_length]
    return name + suffix


def urlsafe_b64encode(content):
    """ Encode the given content as URL-safe base64 and remove padding. """
    return base64.urlsafe_b64encode(content).replace(b'=', b'')


def urlsafe_b64decode(base64_string):
    """ Decode the given base64 string, generated by urlsafe_b64encode().
    """
    # Reinstate removed padding.
    removed = len(base64_string) % 4
    if removed > 0:
        base64_string += b'=' * (4 - removed)

    return base64.urlsafe_b64decode(base64_string)


def parse_name_value(name_value):
    """ Parse a string in NAME=VALUE format.

    :return: a tuple of name, value
    :raise: ValidationError if name_value is malformed
    """
    m = re.match(r'([^=]+)=(.+)', name_value)
    if not m:
        raise ValidationError(
            '%s is not in the format NAME=VALUE' % name_value)
    return m.group(1), m.group(2)
