from typing import Any, Self


class Box:
    def __init__(self, value: Any) -> None:
        self.value: Any = value

    def __eq__(self, other: Any) -> Any:
        """Defines behavior for the equality operator, ==."""
        return self.value == other

    def __ne__(self, other: Any):
        """Defines behavior for the inequality operator, !=."""
        return self.value != other

    def __lt__(self, other: Any):
        """Defines behavior for the less-than operator, <."""
        return self.value < other

    def __gt__(self, other: Any):
        """Defines behavior for the greater-than operator, >."""
        return self.value > other

    def __le__(self, other: Any):
        """Defines behavior for the less-than-or-equal-to operator, <=."""
        return self.value <= other

    def __ge__(self, other: Any):
        """Defines behavior for the greater-than-or-equal-to operator, >=."""
        return self.value >= other

    def __add__(self, other: Any) -> Any:
        """Implements addition."""
        return self.value + other

    def __iadd__(self, other: Any) -> Self:
        """Implements inline addition."""
        self.value += other
        return self

    def __radd__(self, other: Any) -> Any:
        """Implements reverse addition."""
        return other + self.value

    def __sub__(self, other: Any) -> Any:
        """Implements subtraction."""
        return self.value - other

    def __isub__(self, other: Any) -> None:
        """Implements inline subtraction."""
        self.value -= other
        return self

    def __rsub__(self, other: Any) -> Any:
        """Implements reverse subtraction."""
        return other - self.value

    def __mul__(self, other: Any) -> Any:
        """Implements multiplication."""
        return self.value * other

    def __rmul__(self, other: Any) -> Any:
        """Implements reverse multiplication."""
        return self.value * other

    def __floordiv__(self, other: Any) -> Any:
        """Implements integer division using the // operator."""
        return self.value // other

    def __div__(self, other: Any) -> Any:
        """Implements division using the / operator."""
        return self.value / other

    def __rdiv__(self, other: Any) -> Any:
        """Implements reverse division using the / operator."""
        return other / self.value

    def __truediv__(self, other: Any) -> Any:
        """Implements true division."""
        return self.value / other

    def __mod__(self, other: Any) -> Any:
        """Implements modulo using the % operator."""
        return self.value % other

    def __int__(self) -> int:
        """Implements conversion of object to int."""
        return int(self.value)

    def __str__(self) -> str:
        """Implements conversion of object to string."""
        return str(self.value)

    def __repr__(self) -> Any:
        return str(self.value)
