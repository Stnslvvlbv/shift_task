from config import PasswordValidateParams


def message_separator(mess):
    return mess + " "


def password_mach_pattern(passwd):

    detail = ""

    if len(passwd) < PasswordValidateParams.min_length:
        detail += message_separator(
            f"Length should be at least {PasswordValidateParams.min_length}."
        )

    if len(passwd) > PasswordValidateParams.max_length:
        detail += message_separator(
            f"Length should be not be greater than {PasswordValidateParams.max_length}."
        )

    if PasswordValidateParams.one_digit_is_required and not any(
        char.isdigit() for char in passwd
    ):
        detail += message_separator("Password should have at least one numeral.")

    if PasswordValidateParams.one_upper_is_required and not any(
        char.isupper() for char in passwd
    ):
        detail += message_separator(
            "Password should have at least one uppercase letter."
        )

    if PasswordValidateParams.one_lower_is_required and not any(
        char.islower() for char in passwd
    ):
        detail += message_separator(
            "Password should have at least one lowercase letter."
        )

    if len(PasswordValidateParams.special_sym) > 0 and not any(
        char in PasswordValidateParams.special_sym for char in passwd
    ):
        detail += message_separator(
            f"Password should have at least one of the symbols {', '.join(PasswordValidateParams.special_sym)}. "
        )

    detail = detail.strip(" ")

    return detail if len(detail) > 0 else False
