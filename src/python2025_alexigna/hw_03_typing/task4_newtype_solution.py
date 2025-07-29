from typing import NewType

Email = NewType("Email", str)


def validate_email(email: str) -> Email:
    if "@" not in email:
        raise ValueError("Invalid email")
    return Email(email)


def send_email(email: Email) -> None:
    print(f"отправка почты на {email}")


if __name__ == "__main__":
    send_email(validate_email("user@example.com"))
    send_email("user@example.com")  # type: ignore
    send_email("user-example.com")  # type: ignore
