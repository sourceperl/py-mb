from typing import Union

from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import (decode_ieee, encode_ieee, long_list_to_word,
                               word_list_to_long)


class _Response:
    def __init__(self, value: Union[list, None]) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return repr(self.value)

    def as_hex(self) -> list:
        if isinstance(self.value, list):
            return [f'0x{x:04x}' for x in self.value]
        else:
            return []

    def as_float(self, double:bool=False) -> list:
        if isinstance(self.value, list):
            return [decode_ieee(x, double=double) for x in word_list_to_long(self.value, long_long=double)]
        else:
            return []


class Cli:
    """ A custom ModbusClient for creating the cli instance. """

    def __init__(self, modbus_client: ModbusClient):
        self.modbus_client = modbus_client

    def read_bits(self, address: int, number: int = 1, d_inputs: bool = False) -> _Response:
        """ """
        if d_inputs:
            return _Response(self.modbus_client.read_discrete_inputs(address, number))
        else:
            return _Response(self.modbus_client.read_coils(address, number))

    def read_words(self, address: int, number: int = 1, i_regs: bool = False) -> _Response:
        if i_regs:
            return _Response(self.modbus_client.read_input_registers(address, number))
        else:
            return _Response(self.modbus_client.read_holding_registers(address, number))

    def write_bits(self, address: int, value: Union[bool, list, tuple]):
        if isinstance(value, (list, tuple)):
            return self.modbus_client.write_multiple_coils(address, value)
        else:
            return self.modbus_client.write_single_coil(address, value)

    def write_words(self, address: int, value: Union[int, list, tuple]):
        if isinstance(value, (list, tuple)):
            return self.modbus_client.write_multiple_registers(address, value)
        else:
            return self.modbus_client.write_single_register(address, value)

    # def _write_float(self, address: int, values: Union[int, float, list, tuple]):
    #     """Write float(s) with write multiple registers."""
    #     floats_l = values if isinstance(values, (list, tuple)) else [values]
    #     b32_l = [encode_ieee(f) for f in floats_l]
    #     b16_l = long_list_to_word(b32_l)
    #     return self.modbus_client.write_multiple_registers(address, b16_l)
