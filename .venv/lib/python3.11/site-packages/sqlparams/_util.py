"""
This module defines internal utility methods.
"""

from collections.abc import Iterable, Sequence


def is_iterable(value):
	"""
	Check whether the value is an iterable (excludes strings).

	*value* is the value to check,

	Returns whether *value* is a iterable (:class:`bool`).
	"""
	return isinstance(value, Iterable) and not isinstance(value, (str, bytes))


def is_sequence(value):
	"""
	Check whether the value is a sequence (excludes strings).

	*value* is the value to check,

	Returns whether *value* is a sequence (:class:`bool`).
	"""
	return isinstance(value, Sequence) and not isinstance(value, (str, bytes))
