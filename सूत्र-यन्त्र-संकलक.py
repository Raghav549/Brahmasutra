"""🕉️ सूत्र यन्त्र-कोड संकलक.

Historically this module wrote ``struct.pack("B B I")`` records — a third
incompatible layout (opcodes 1-5 with a different meaning for 5).  It now
assembles to the format documented in :mod:`brahma_bytecode`, so the bytecode it
produces runs on :class:`सूत्र_यन्त्र_निष्पादक.यन्त्रनिष्पादक`.

Its old mnemonics are still accepted by the assembler.
"""

from __future__ import annotations

import brahma_bytecode

opcode = dict(brahma_bytecode.OPCODES)
register_map = dict(brahma_bytecode.REGISTERS)


def संकलन(इनपुट, आउटपुट):
    """Assemble ``इनपुट`` into ``आउटपुट``; return the bytecode."""
    code = brahma_bytecode.assemble_file(इनपुट, आउटपुट)
    print("संकलन पूर्ण:", आउटपुट)
    return code


def main(argv=None):
    """CLI: ``python सूत्र-यन्त्र-संकलक.py इनपुट.सूत्र आउटपुट.यन्त्र``."""
    import argparse

    parser = argparse.ArgumentParser(description="सूत्र यन्त्र कोड संकलक")
    parser.add_argument("input", nargs="?", help="सूत्र संचिका")
    parser.add_argument("output", nargs="?", help="यन्त्र संचिका")
    args = parser.parse_args(argv)
    if not args.input or not args.output:
        parser.print_usage()
        return 2
    संकलन(args.input, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
