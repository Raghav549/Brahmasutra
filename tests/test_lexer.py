"""Lexer tests."""

from __future__ import annotations

import pytest

from brahma import LexError, TokenKind, tokenize


def kinds(tokens):
    return [token.kind for token in tokens]


def values(source):
    return [(token.kind, token.value) for token in tokenize(source)[:-1]]


class TestBasics:
    def test_empty_source_has_only_eof(self):
        tokens = tokenize("")
        assert len(tokens) == 1
        assert tokens[0].kind is TokenKind.EOF

    def test_numbers(self):
        assert values("42 3.5 1e3 २ १०") == [
            (TokenKind.NUMBER, 42),
            (TokenKind.NUMBER, 3.5),
            (TokenKind.NUMBER, 1000.0),
            (TokenKind.NUMBER, 2),
            (TokenKind.NUMBER, 10),
        ]

    def test_devanagari_digits_full_set(self):
        tokens = tokenize("० १ २ ३ ४ ५ ६ ७ ८ ९")
        assert [token.value for token in tokens[:-1]] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_multi_digit_devanagari_number(self):
        assert values("२०२६") == [(TokenKind.NUMBER, 2026)]

    def test_strings_and_escapes(self):
        assert values(r'"नमस्ते" "a\nb" "q\"uote" "tab\there"') == [
            (TokenKind.STRING, "नमस्ते"),
            (TokenKind.STRING, "a\nb"),
            (TokenKind.STRING, 'q"uote'),
            (TokenKind.STRING, "tab\there"),
        ]

    def test_single_quoted_string(self):
        assert values("'abc'") == [(TokenKind.STRING, "abc")]

    def test_unicode_escape(self):
        assert values(r'"\u0950"') == [(TokenKind.STRING, "\u0950")]

    def test_unicode_identifier(self):
        tokens = tokenize("कर्म_संख्या")
        assert tokens[0].kind is TokenKind.NAME
        assert tokens[0].value == "कर्म_संख्या"

    def test_ascii_identifier(self):
        assert values("foo_bar1") == [(TokenKind.NAME, "foo_bar1")]

    def test_keywords_sanskrit_and_ascii(self):
        assert values("यदि if सत्य true") == [
            (TokenKind.KEYWORD, "IF"),
            (TokenKind.KEYWORD, "IF"),
            (TokenKind.KEYWORD, "TRUE"),
            (TokenKind.KEYWORD, "TRUE"),
        ]

    def test_operators_longest_match(self):
        assert [token.value for token in tokenize("** == != <= >= += -=")[:-1]] == [
            "**",
            "==",
            "!=",
            "<=",
            ">=",
            "+=",
            "-=",
        ]

    def test_comments_are_ignored(self):
        assert values("# पूरी पंक्ति\n1 # पंक्ति के बाद\n2") == [
            (TokenKind.NEWLINE, "\n"),
            (TokenKind.NUMBER, 1),
            (TokenKind.NEWLINE, "\n"),
            (TokenKind.NUMBER, 2),
        ]

    def test_semicolon_is_a_token(self):
        assert values("1;2") == [
            (TokenKind.NUMBER, 1),
            (TokenKind.OP, ";"),
            (TokenKind.NUMBER, 2),
        ]

    def test_newlines_are_preserved(self):
        assert kinds(tokenize("1\n2")) == [
            TokenKind.NUMBER,
            TokenKind.NEWLINE,
            TokenKind.NUMBER,
            TokenKind.EOF,
        ]

    def test_positions(self):
        tokens = tokenize("दर्शय\n  अ")
        assert (tokens[0].line, tokens[0].column) == (1, 1)
        assert (tokens[2].line, tokens[2].column) == (2, 3)

    def test_tokenize_is_repeatable(self):
        lexer = tokenize
        assert lexer("1")[0].value == 1


class TestErrors:
    def test_invalid_character(self):
        with pytest.raises(LexError) as info:
            tokenize("1 @ 2")
        assert "अमान्य चिह्न" in info.value.message
        assert info.value.line == 1
        assert info.value.column == 3

    def test_unterminated_string(self):
        with pytest.raises(LexError) as info:
            tokenize('"abc')
        assert "असमाप्त" in info.value.message

    def test_newline_in_string(self):
        with pytest.raises(LexError):
            tokenize('"abc\ndef"')

    def test_bad_escape(self):
        with pytest.raises(LexError):
            tokenize(r'"a\qb"')

    def test_incomplete_unicode_escape(self):
        with pytest.raises(LexError):
            tokenize(r'"\u12"')

    def test_error_has_source_name(self):
        with pytest.raises(LexError) as info:
            tokenize("@", source_name="demo.sutra")
        assert "demo.sutra" in info.value.format()

    def test_type_check(self):
        with pytest.raises(TypeError):
            tokenize(123)

    def test_lexer_class_reuses_tokens(self):
        from brahma import Lexer

        lexer = Lexer("1 + 2")
        first = lexer.tokenize()
        second = lexer.tokenize()
        assert [t.kind for t in first] == [t.kind for t in second]
