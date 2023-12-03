"""
Untruncates json. Machine translated from untruncate-json by dphilipson
"""
from __future__ import annotations
from enum import Enum
from typing import Optional


class ContextType(Enum):
    """The type of context that the parser is in."""

    TOP_LEVEL = "topLevel"
    STRING = "string"
    STRING_ESCAPED = "stringEscaped"
    STRING_UNICODE = "stringUnicode"
    NUMBER = "number"
    NUMBER_NEEDS_DIGIT = "numberNeedsDigit"
    NUMBER_NEEDS_EXPONENT = "numberNeedsExponent"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    ARRAY_NEEDS_VALUE = "arrayNeedsValue"
    ARRAY_NEEDS_COMMA = "arrayNeedsComma"
    OBJECT_NEEDS_KEY = "objectNeedsKey"
    OBJECT_NEEDS_COLON = "objectNeedsColon"
    OBJECT_NEEDS_VALUE = "objectNeedsValue"
    OBJECT_NEEDS_COMMA = "objectNeedsComma"


class RespawnReason(Enum):
    """ "The reason why the parser needs to respawn."""

    STRING_ESCAPE = "stringEscape"
    COLLECTION_ITEM = "collectionItem"


def is_whitespace(char: str) -> bool:
    """Returns true if the character is whitespace."""
    return char in "\u0020\u000D\u000A\u0009"


def complete(json_str: str) -> str:
    """Completes the json string."""
    context_stack: list[ContextType] = [ContextType.TOP_LEVEL]
    position = 0
    respawn_position: Optional[int] = None
    respawn_stack_length: Optional[int] = None
    respawn_reason: Optional[RespawnReason] = None

    def push(context: ContextType) -> None:
        """Pushes the context onto the stack."""
        context_stack.append(context)

    def replace(context: ContextType) -> None:
        """Replaces the context on the stack."""
        context_stack[-1] = context

    def set_respawn(reason: RespawnReason) -> None:
        """Sets the respawn position."""
        nonlocal respawn_position, respawn_stack_length, respawn_reason
        if respawn_position is None:
            respawn_position = position
            respawn_stack_length = len(context_stack)
            respawn_reason = reason

    def clear_respawn(reason: RespawnReason) -> None:
        """Clears the respawn position."""
        nonlocal respawn_position, respawn_stack_length, respawn_reason
        if reason == respawn_reason:
            respawn_position = None
            respawn_stack_length = None
            respawn_reason = None

    def pop() -> None:
        """Pops the context stack."""
        context_stack.pop()

    def dont_consume_character() -> None:
        """Doesn't consume the character."""
        nonlocal position
        position -= 1

    def start_any(char: str) -> None:
        """Starts any context."""
        if "0" <= char <= "9":
            push(ContextType.NUMBER)
            return
        if char == '"':
            push(ContextType.STRING)
            return
        if char == "-":
            push(ContextType.NUMBER_NEEDS_DIGIT)
            return
        if char == "t":
            push(ContextType.TRUE)
            return
        if char == "f":
            push(ContextType.FALSE)
            return
        if char == "n":
            push(ContextType.NULL)
            return
        if char == "[":
            push(ContextType.ARRAY_NEEDS_VALUE)
            return
        if char == "{":
            push(ContextType.OBJECT_NEEDS_KEY)
            return

    while position < len(json_str):
        char = json_str[position]
        current_context = context_stack[-1]

        if current_context == ContextType.TOP_LEVEL:
            start_any(char)
        elif current_context == ContextType.STRING:
            if char == '"':
                pop()
            elif char == "\\":
                set_respawn(RespawnReason.STRING_ESCAPE)
                push(ContextType.STRING_ESCAPED)
        elif current_context == ContextType.STRING_ESCAPED:
            if char == "u":
                push(ContextType.STRING_UNICODE)
            else:
                clear_respawn(RespawnReason.STRING_ESCAPE)
                pop()
        elif current_context == ContextType.STRING_UNICODE:
            if position - json_str.rfind("u", 0, position) == 4:
                clear_respawn(RespawnReason.STRING_ESCAPE)
                pop()
        elif current_context == ContextType.NUMBER:
            if char == ".":
                replace(ContextType.NUMBER_NEEDS_DIGIT)
            elif char in ["e", "E"]:
                replace(ContextType.NUMBER_NEEDS_EXPONENT)
            elif not "0" <= char <= "9":
                dont_consume_character()
                pop()
        elif current_context == ContextType.NUMBER_NEEDS_DIGIT:
            replace(ContextType.NUMBER)
        elif current_context == ContextType.NUMBER_NEEDS_EXPONENT:
            if char in ["+", "-"]:
                replace(ContextType.NUMBER_NEEDS_DIGIT)
            else:
                replace(ContextType.NUMBER)
        elif current_context in [ContextType.TRUE, ContextType.FALSE, ContextType.NULL]:
            if not "a" <= char <= "z":
                dont_consume_character()
                pop()
        elif current_context == ContextType.ARRAY_NEEDS_VALUE:
            if char == "]":
                pop()
            elif not is_whitespace(char):
                clear_respawn(RespawnReason.COLLECTION_ITEM)
                replace(ContextType.ARRAY_NEEDS_COMMA)
                start_any(char)
        elif current_context == ContextType.ARRAY_NEEDS_COMMA:
            if char == "]":
                pop()
            elif char == ",":
                set_respawn(RespawnReason.COLLECTION_ITEM)
                replace(ContextType.ARRAY_NEEDS_VALUE)
        elif current_context == ContextType.OBJECT_NEEDS_KEY:
            if char == "}":
                pop()
            elif char == '"':
                set_respawn(RespawnReason.COLLECTION_ITEM)
                replace(ContextType.OBJECT_NEEDS_COLON)
                push(ContextType.STRING)
        elif current_context == ContextType.OBJECT_NEEDS_COLON:
            if char == ":":
                replace(ContextType.OBJECT_NEEDS_VALUE)
        elif current_context == ContextType.OBJECT_NEEDS_VALUE:
            if not is_whitespace(char):
                clear_respawn(RespawnReason.COLLECTION_ITEM)
                replace(ContextType.OBJECT_NEEDS_COMMA)
                start_any(char)
        elif current_context == ContextType.OBJECT_NEEDS_COMMA:
            if char == "}":
                pop()
            elif char == ",":
                set_respawn(RespawnReason.COLLECTION_ITEM)
                replace(ContextType.OBJECT_NEEDS_KEY)
        position += 1

    if respawn_stack_length is not None:
        context_stack = context_stack[:respawn_stack_length]

    # Final assembly of the result
    result = [json_str[:respawn_position]] if respawn_position is not None else [json_str]

    def finish_word(word: str) -> None:
        """Finishes the word."""
        result.append(word[len(json_str) - json_str.rfind(word[0]) :])

    for i in range(len(context_stack) - 1, -1, -1):
        context = context_stack[i]

        if context == ContextType.STRING:
            result.append('"')
        elif context in (ContextType.NUMBER_NEEDS_DIGIT, ContextType.NUMBER_NEEDS_EXPONENT):
            result.append("0")
        elif context == ContextType.TRUE:
            finish_word("true")
        elif context == ContextType.FALSE:
            finish_word("false")
        elif context == ContextType.NULL:
            finish_word("null")
        elif context in (ContextType.ARRAY_NEEDS_VALUE, ContextType.ARRAY_NEEDS_COMMA):
            result.append("]")
        elif context in (
            ContextType.OBJECT_NEEDS_KEY,
            ContextType.OBJECT_NEEDS_COLON,
            ContextType.OBJECT_NEEDS_VALUE,
            ContextType.OBJECT_NEEDS_COMMA,
        ):
            result.append("}")

    return "".join(result)
