import strawberry


@strawberry.input
class UpdateTimezoneInput:
    timezone: str
