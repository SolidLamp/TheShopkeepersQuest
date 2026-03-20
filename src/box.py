import math
from typing import Any, Generic, Self, TypeVar

T = TypeVar("T")


class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value: T = value

    def _normalise_type(
        self, to_type: type
    ) -> int | float | str | bool | list[Any] | dict[Any, Any] | T:
        # converts the given type to a string for pattern matching
        pattern: str = str(to_type)[8:-2]
        match pattern:
            case "int":
                return int(self.value)
            case "float":
                return float(self.value)
            case "str":
                return str(self.value)
            case "bool":
                return bool(self.value)
            case "list":
                return list(self.value)
            case "dict":
                return dict(self.value)
            case _:
                return self.value

    def __eq__(self, other: Any) -> bool:
        """Defines behavior for the equality operator, ==."""
        try:
            equal: bool = self.value == other
        except:
            equal: bool = False
        return equal

    def __ne__(self, other: Any) -> bool:
        """Defines behavior for the inequality operator, !=."""
        try:
            notequal: bool = self.value != other
        except:
            notequal: bool = False
        return notequal

    def __lt__(self, other: Any) -> bool:
        """Defines behavior for the less-than operator, <."""
        try:
            less_than: bool = self.value < other
        except:
            less_than: bool = False
        return less_than

    def __gt__(self, other: Any) -> bool:
        """Defines behavior for the greater-than operator, >."""
        try:
            more_than: bool = self.value > other
        except:
            more_than: bool = False
        return more_than

    def __le__(self, other: Any):
        """Defines behavior for the less-than-or-equal-to operator, <=."""
        try:
            less_than: bool = self.value <= other
        except:
            less_than: bool = False
        return less_than

    def __ge__(self, other: Any):
        """Defines behavior for the greater-than-or-equal-to operator, >=."""
        try:
            more_than: bool = self.value >= other
        except:
            more_than: bool = False
        return more_than

    def __add__(self, other: Any) -> Any:
        """Implements addition."""
        return self.value + other

    def __iadd__(self, other: Any) -> Self:
        """Implements inline addition."""
        self.value += other
        return self

    def __radd__(self, other: Any) -> Any:
        """Implements reverse addition."""
        value = self._normalise_type(type(other))
        return other + value

    def __sub__(self, other: Any) -> Any:
        """Implements subtraction."""
        return self.value - other

    def __isub__(self, other: Any) -> Self:
        """Implements inline subtraction."""
        self.value -= other
        return self

    def __rsub__(self, other: Any) -> Any:
        """Implements reverse subtraction."""
        value = self._normalise_type(type(other))
        return other - value

    def __mul__(self, other: Any) -> Any:
        """Implements multiplication."""
        return self.value * other

    def __rmul__(self, other: Any) -> Any:
        """Implements reverse multiplication."""
        value = self._normalise_type(type(other))
        return value * other

    def __floordiv__(self, other: Any) -> Any:
        """Implements integer division using the // operator."""
        return self.value // other

    def __rfloordiv__(self, other: Any) -> Any:
        """Implements reverse integer division using the // operator."""
        value = self._normalise_type(type(other))
        return other // value

    def __div__(self, other: Any) -> Any:
        """Implements division using the / operator."""
        return self.value / other

    def __rdiv__(self, other: Any) -> Any:
        """Implements reverse division using the / operator."""
        value = self._normalise_type(type(other))
        return other / value

    def __truediv__(self, other: Any) -> Any:
        """Implements true division."""
        return self.value / other

    def __rtruediv__(self, other: Any) -> Any:
        """Implements reverse true division."""
        value = self._normalise_type(type(other))
        return other / value

    def __mod__(self, other: Any) -> Any:
        """Implements modulo using the % operator."""
        return self.value % other

    def __rmod__(self, other: Any) -> Any:
        """Implements reverse modulo using the % operator."""
        value = self._normalise_type(type(other))
        return other % value

    def __abs__(self) -> Any:
        """Implements absolute value."""
        return abs(self.value)

    def __ceil__(self) -> Any:
        """Implements ceiling operator."""
        return math.ceil(self.value)

    def __floor__(self) -> Any:
        """Implements floor operator."""
        return math.floor(self.value)

    def __and__(self, other: Any) -> Any:
        """Implements boolean AND operator."""
        return self.value and other

    def __inv__(self) -> T:
        """Implements the boolean inverted data."""
        return ~(self.value)

    def __invert__(self) -> T:
        """Implements the boolean inverted data."""
        return ~(self.value)

    def __neg__(self) -> T:
        """Implements bitwise negation operation."""
        return -(self.value)

    def __or__(self, other: Any) -> Any:
        """Implements boolean OR operator"""
        return self.value or other

    def __bool__(self) -> bool:
        """Implements conversion of object to bool."""
        return bool(self.value)

    def __float__(self) -> float:
        """Implements conversion of object to float."""
        return float(self.value)

    def __int__(self) -> int:
        """Implements conversion of object to int."""
        return int(self.value)

    def __str__(self) -> str:
        """Implements conversion of object to string."""
        return str(self.value)

    def __repr__(self) -> Any:
        """String representation of the box."""
        return str(self.value)

    def __index__(self) -> int:
        """Returns an integer index of the object."""
        try:
            value = int(self.value)
        except TypeError as e:
            raise TypeError(f"{type(self.index)} is not compatible with int.\n{e}")
        return value

    def __copy__(self) -> Self:
        """Duplicates the immutable box to a new box object."""
        copied_box: Box[T] = Box(self.value)
        return copied_box

    def copy(self) -> Self:
        copied_box = self.__copy__()
        return copied_box
