import datetime
from functools import wraps
from typing import Awaitable, Callable, Optional

from authx import AuthX, RequestToken, TokenPayload
from authx.exceptions import MissingTokenError
from fastapi import Request

from config import JWT_TOKEN_CONFIG
from src.constants.custom_type import Privilege
from src.errors.http_value_exception import TokenExceptions
from src.errors.type_error_ import ServiceAuthException
from src.security.redis_client import redis_client


class Security(AuthX):

    @property
    def get_optional_refresh_from_request(
        self,
    ) -> Callable[[Request], Awaitable[RequestToken | None]]:
        request_token = self.get_token_from_request(type="refresh", optional=True)
        return request_token

    @property
    def get_optional_access_from_request(
        self,
    ) -> Callable[[Request], Awaitable[RequestToken | None]]:
        request_token = self.get_token_from_request(type="access", optional=True)
        return request_token

    def decode_token(self, token):
        return self._decode_token(token)

    @staticmethod
    def set_token_in_blacklist(token_payload: TokenPayload):
        jti = token_payload.jti
        now_date = datetime.datetime.now(datetime.timezone.utc)
        exp = token_payload.exp - now_date
        exp = int(exp.total_seconds())

        redis_client.set(name=jti, value="blocked", ex=exp)

    @staticmethod
    def token_is_blacklisted(token_payload: TokenPayload):
        value = redis_client.get(token_payload.jti)
        return False if value is None else True

    @staticmethod
    def catch_token_verification_exceptions(verifier):

        @wraps(verifier)
        def wrapper(*args, **kwargs):
            try:
                return verifier(*args, **kwargs)

            except (TypeError, AttributeError):
                raise TokenExceptions(ServiceAuthException.MISSING_TOKEN).to_exception(
                    "jwt", "Required token is missing", None
                )

            except MissingTokenError:
                raise TokenExceptions(ServiceAuthException.MISSING_TOKEN).to_exception(
                    "jwt", "Required token is missing", None
                )

            except Exception:
                raise TokenExceptions(ServiceAuthException.TOKEN_INVALID).to_exception(
                    "jwt", "The token is not valid", None
                )

        return wrapper

    @staticmethod
    def static_verify_token(
        request_token, verify_type=True, verify_fresh=False, verify_csrf=False
    ):
        instance = AuthX()
        return instance.verify_token(
            request_token, verify_type, verify_fresh, verify_csrf
        )

    @staticmethod
    @catch_token_verification_exceptions
    def validate_token(
        request_token: Optional[RequestToken],
        verify_type=True,
        verify_fresh=False,
        verify_csrf=False,
    ) -> TokenPayload:
        token_payload = Security.static_verify_token(
            request_token,
            verify_type=verify_type,
            verify_fresh=verify_fresh,
            verify_csrf=verify_csrf,
        )
        if Security.token_is_blacklisted(token_payload):
            raise TokenExceptions(ServiceAuthException.TOKEN_INVALID).to_exception(
                "jwt", "The token is not valid", None
            )

        return token_payload

    @staticmethod
    def check_validity_and_block(token: RequestToken, type: str):

        token_payload = Security.validate_token(token)
        Security.set_token_in_blacklist(token_payload)
        status = f"{type} token: is blocked"

        return status

    @staticmethod
    def checking_user_rights(
        token: TokenPayload,
        is_active: bool = True,
    ) -> bool:
        # Определяем требования к пользователю
        requirements = {
            Privilege.IS_ACTIVE: is_active,
        }

        # Проверяем права пользователя
        for privilege, required in requirements.items():
            if required and not getattr(token, privilege, False):
                raise TokenExceptions(
                    ServiceAuthException.ACCESS_RESTRICTION
                ).to_exception("jwt", "Available only for active users", None)
                # raise HTTPException(
                #     fuck
                #     **UserErrorCode.authorization_error(privilege=privilege)
                # )

        return True


TokenGetter = Callable[[Request], Awaitable[RequestToken]]
OptTokenGetter = Callable[[Request], Awaitable[RequestToken | None]]

security = Security(config=JWT_TOKEN_CONFIG)  # , model=ShowUser)
