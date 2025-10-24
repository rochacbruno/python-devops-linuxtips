from typing import Any, Callable

# Type Alias
Numeric = int | float | complex


def sum(a: Numeric, b: Numeric) -> Numeric:
    return a + b


def mul(a: int | float | str, b: int) -> int | float | str:
    return a * b


def print_result(x: Any):
    print(f"Resultado: {x}")


def converter(value, convert_function: Callable):
    return convert_function(value)


def report(items: list[str]):
    print(" | ".join(items))


report(["batata", "tomate", "45"])


print(converter(234, int))


res = sum(1.5, 2)

print_result(str(res))

nres = mul("Bruno", 5)
print_result(nres)
