from enum import Enum


class AuthProviderType(str, Enum):
    CUSTOM = "custom"
    GOOGLE = "google"
    GITHUB = "github"

    def __str__(self):
        return self.value


class VerificationType(str, Enum):
    EMAIL = "email"
    PASSWORD_RESET = "password_reset"

    def __str__(self):
        return self.value


AVAILABLE_AUTH_PROVIDERS = [e.value for e in AuthProviderType]
AVAILABLE_VERIFICATIONS = [e.value for e in VerificationType]
