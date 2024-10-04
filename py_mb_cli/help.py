HEADER_TXT = \
"""pyModbusTCP: client interactive tool.

Use 'cli' object to interract with server (like 'cli.read_coils(0)').
Type 'exit' to quit and 'help()' for more info.
"""
HELP_TXT = \
"""Usages examples:

- turn on debug mode:
    cli.debug = True

- read 4 bits at @512 in "coils" space (function 0x01):
    cli.read_bits(512, 4)

- read 4 bits at @512 in "discrete inputs" space (function 0x02):
    cli.read_bits(512, 4, d_inputs=True)

- write single coils at @512 with single request (function 0x05)
    cli.write_bits(512, True)

- write single coils at @512 with multiple request (function 0x0f)
    cli.write_bits(512, [True])

- read 2 registers in "holding registers" space (function 0x03):
    cli.read_words(20_800, 2)

- read 2 registers in "input registers" space (function 0x04):
    cli.read_words(20_800, 2, i_regs=True)

- read IEEE single-precision (32-bit) floating-point:
    cli.read_words(20_800, 4, convert=True).to_f32()

- write IEEE single-precision (32-bit) floating-point:
    cli.write_words(20_800, convert.from_f32([1.0, 2.0]))
"""
