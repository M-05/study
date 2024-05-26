import logging
logger = logging.getLogger(__name__)


def add(a: int, b: int) -> int:
    if isinstance(a, float):
        logger.warning(
            """add() only supports adding two integers but got float type.
            Running anyway..."""
        )
        return a+b
