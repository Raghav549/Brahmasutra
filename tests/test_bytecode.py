"""Bytecode container tests: serialisation, validation and compatibility."""

from __future__ import annotations

import json

import pytest

from brahma import BytecodeError, compile_source
from brahma.bytecode import (
    FORMAT_NAME,
    FORMAT_VERSION,
    MAGIC,
    CodeObject,
    Instruction,
    disassemble,
    dump_bytecode,
    load_bytecode,
)


class TestRoundTrip:
    def test_dump_and_load(self, tmp_path):
        code = compile_source('दर्शय "नमस्ते"')
        path = tmp_path / "program.sbc"
        dump_bytecode(code, str(path))
        loaded = load_bytecode(str(path))
        assert disassemble(loaded) == disassemble(code)

    def test_magic_prefix(self):
        blob = dump_bytecode(compile_source("दर्शय 1"))
        assert blob.startswith(MAGIC)

    def test_payload_is_utf8_json(self):
        blob = dump_bytecode(compile_source("दर्शय 1"))
        data = json.loads(blob[len(MAGIC) :].decode("utf-8"))
        assert data["format"] == FORMAT_NAME
        assert data["version"] == FORMAT_VERSION
        assert data["entry"]["instructions"][-1]["op"] == "HALT"

    def test_load_from_bytes(self):
        blob = dump_bytecode(compile_source("दर्शय 1"))
        assert isinstance(load_bytecode(blob), CodeObject)

    def test_load_from_file_object(self, tmp_path):
        blob = dump_bytecode(compile_source("दर्शय 1"))
        path = tmp_path / "x.sbc"
        path.write_bytes(blob)
        with open(str(path), "rb") as handle:
            assert isinstance(load_bytecode(handle), CodeObject)

    def test_nested_function_survives_round_trip(self):
        code = compile_source("कार्य f(a)\n प्रत्यागमन a\nअन्त")
        loaded = load_bytecode(dump_bytecode(code))
        nested = [i for i in loaded.instructions if i.op == "MAKE_FUNCTION"][0].arg
        assert isinstance(nested, CodeObject)
        assert nested.params == ["a"]

    def test_unicode_preserved(self):
        code = compile_source('स्थापय नाम = "विश्व"\nदर्शय नाम')
        loaded = load_bytecode(dump_bytecode(code))
        text = disassemble(loaded)
        assert "विश्व" in text


class TestValidation:
    def test_rejects_garbage(self):
        with pytest.raises(BytecodeError):
            load_bytecode(b"not bytecode")

    def test_rejects_wrong_format(self):
        blob = json.dumps({"format": "something", "version": 1, "entry": {}}).encode()
        with pytest.raises(BytecodeError):
            load_bytecode(blob)

    def test_rejects_newer_version(self):
        blob = json.dumps({"format": FORMAT_NAME, "version": 999, "entry": {}}).encode()
        with pytest.raises(BytecodeError) as info:
            load_bytecode(blob)
        assert "संस्करण" in str(info.value)

    def test_rejects_missing_entry(self):
        blob = json.dumps({"format": FORMAT_NAME, "version": FORMAT_VERSION}).encode()
        with pytest.raises(BytecodeError):
            load_bytecode(blob)

    def test_rejects_unknown_instruction(self):
        entry = {"name": "m", "params": [], "instructions": [{"op": "BOGUS", "line": 1}]}
        blob = json.dumps({"format": FORMAT_NAME, "version": FORMAT_VERSION, "entry": entry}).encode()
        with pytest.raises(BytecodeError):
            load_bytecode(blob)

    def test_rejects_bad_jump_in_file(self):
        entry = {
            "name": "m",
            "params": [],
            "instructions": [
                {"op": "JUMP", "arg": 999, "line": 1},
                {"op": "HALT", "line": 1},
            ],
        }
        blob = json.dumps({"format": FORMAT_NAME, "version": FORMAT_VERSION, "entry": entry}).encode()
        with pytest.raises(BytecodeError):
            load_bytecode(blob)

    def test_instruction_to_from_dict(self):
        instruction = Instruction(op="LOAD_CONST", arg=5, line=3)
        assert Instruction.from_dict(instruction.to_dict()) == instruction

    def test_nested_code_serialisation(self):
        inner = CodeObject(name="f", params=["a"])
        inner.emit("LOAD_CONST", None)
        inner.emit("RETURN")
        outer = CodeObject(name="m")
        outer.emit("MAKE_FUNCTION", inner)
        outer.emit("HALT")
        restored = CodeObject.from_dict(outer.to_dict())
        assert isinstance(restored.instructions[0].arg, CodeObject)


class TestDisassembler:
    def test_nested_listing_is_indented(self):
        text = disassemble(compile_source("कार्य f()\n प्रत्यागमन 1\nअन्त"))
        assert "    ==" in text

    def test_indent_argument(self):
        text = disassemble(compile_source("दर्शय 1"), indent=">> ")
        assert text.startswith(">> ")
