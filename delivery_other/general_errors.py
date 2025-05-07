from dataclasses import dataclass


@dataclass
class Error:
    code: str
    message: str

class GeneralErrors:
    @staticmethod
    def value_is_required(field_name: str) -> Error:
        return Error(
            code="value.is.required",
            message=f"Value {field_name} is required"
        )

    @staticmethod
    def value_is_invalid(field_name: str) -> Error:
        return Error(
            code="value.is.invalid",
            message=f"Value {field_name} is invalid"
        )