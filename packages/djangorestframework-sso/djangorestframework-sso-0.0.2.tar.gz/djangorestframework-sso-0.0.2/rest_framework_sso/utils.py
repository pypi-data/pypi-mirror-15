# coding: utf-8
from __future__ import absolute_import, unicode_literals

from datetime import datetime

import jwt
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import six
from jwt.exceptions import MissingRequiredClaimError, InvalidIssuerError

from rest_framework_sso.settings import api_settings


def create_session_payload(session_token, user, **kwargs):
    return {
        'type': 'session',
        'sid': session_token.pk,
        'uid': user.pk,
        'email': user.email,
    }


def create_authorization_payload(session_token, user, **kwargs):
    return {
        'type': 'auth',
        'sid': session_token.pk,
        'uid': user.pk,
        'email': user.email,
        'scope': [],
    }


def encode_jwt_token(payload):
    if payload.get('type') not in ('session', 'auth'):
        raise RuntimeError('Unknown token type')

    if not payload.get('iss'):
        if api_settings.IDENTITY is not None:
            payload['iss'] = api_settings.IDENTITY
        else:
            raise RuntimeError('IDENTITY must be specified in settings')

    if not payload.get('aud'):
        if payload.get('type') == 'session' and api_settings.SESSION_AUDIENCE is not None:
            payload['aud'] = api_settings.SESSION_AUDIENCE
        elif payload.get('type') == 'auth' and api_settings.AUTHORIZATION_AUDIENCE is not None:
            payload['aud'] = api_settings.AUTHORIZATION_AUDIENCE
        elif api_settings.IDENTITY is not None:
            payload['aud'] = [api_settings.IDENTITY]
        else:
            raise RuntimeError('SESSION_AUDIENCE must be specified in settings')

    if not payload.get('exp'):
        if payload.get('type') == 'session' and api_settings.SESSION_EXPIRATION is not None:
            payload['exp'] = datetime.utcnow() + api_settings.SESSION_EXPIRATION
        elif payload.get('type') == 'auth' and api_settings.AUTHORIZATION_EXPIRATION is not None:
            payload['exp'] = datetime.utcnow() + api_settings.AUTHORIZATION_EXPIRATION

    if payload['iss'] not in api_settings.PRIVATE_KEYS:
        raise RuntimeError('Private key for specified issuer was not found in settings')

    private_key = open(api_settings.PRIVATE_KEYS.get(payload['iss']), 'rt').read()

    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=api_settings.ENCODE_ALGORITHM,
        json_encoder=DjangoJSONEncoder,
    ).decode('utf-8')


def decode_jwt_token(token):
    unverified_claims = jwt.decode(token, verify=False)

    if 'iss' not in unverified_claims:
        raise MissingRequiredClaimError('iss')

    unverified_issuer = six.text_type(unverified_claims['iss'])

    if api_settings.ACCEPTED_ISSUERS is not None and unverified_issuer not in api_settings.ACCEPTED_ISSUERS:
        raise InvalidIssuerError('Invalid issuer')
    if unverified_issuer not in api_settings.PUBLIC_KEYS:
        raise InvalidIssuerError('Invalid issuer')

    public_key = open(api_settings.PUBLIC_KEYS.get(unverified_issuer), 'rt').read()

    options = {
        'verify_exp': api_settings.VERIFY_EXPIRATION,
        'verify_aud': True,
        'verify_iss': True,
    }

    return jwt.decode(
        jwt=token,
        key=public_key,
        verify=api_settings.VERIFY_SIGNATURE,
        algorithms=api_settings.DECODE_ALGORITHMS or [api_settings.ENCODE_ALGORITHM],
        options=options,
        leeway=api_settings.EXPIRATION_LEEWAY,
        audience=api_settings.IDENTITY,
        issuer=unverified_issuer,
    )
