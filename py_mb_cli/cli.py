import struct
from typing import List, Optional, Sequence, Union

from pyModbusTCP.client import ModbusClient


class _Convert:
    """ A class for easy conversion of Modbus data formats. """

    def __init__(self, swap_bytes: bool = False, swap_word: bool = False) -> None:
        # args
        # self.swap_bytes = swap_bytes
        # self.swap_word = swap_word
        # private
        self._raw = bytes()

    def from_u16(self, items: Sequence):
        """ from unsigned 16 bits """
        self._raw = bytes()
        for item in items:
            self._raw += struct.pack('>H', item)
        return self

    def from_f32(self, items: Sequence):
        """ from IEEE single precision 64 bits """
        self._raw = bytes()
        for item in items:
            self._raw += struct.pack('>f', item)
        return self

    def from_f64(self, items: Sequence):
        """ from IEEE double precision 64 bits """
        self._raw = bytes()
        for item in items:
            self._raw += struct.pack('>d', item)
        return self

    def to_bytes(self) -> bytes:
        """ as raw bytes """
        return self._raw

    def to_u16(self) -> List[int]:
        """ as unsigned 16 bits """
        u16_l = []
        for i in range(0, len(self._raw), 2):
            u16_l.append(struct.unpack('>H', self._raw[i:i+2])[0])
        return u16_l

    def to_i16(self) -> List[int]:
        """ as signed 16 bits """
        i16_l = []
        for i in range(0, len(self._raw), 2):
            i16_l.append(struct.unpack('>h', self._raw[i:i+2])[0])
        return i16_l

    def to_u32(self) -> List[int]:
        """ as unsigned 32 bits """
        u32_l = []
        for i in range(0, len(self._raw), 4):
            u32_l.append(struct.unpack('>I', self._raw[i:i+4])[0])
        return u32_l

    def to_i32(self) -> List[int]:
        """ as signed 32 bits """
        i32_l = []
        for i in range(0, len(self._raw), 4):
            i32_l.append(struct.unpack('>i', self._raw[i:i+4])[0])
        return i32_l

    def to_f32(self) -> List[float]:
        """ to IEEE single precision 32 bits """
        f32_l = []
        for i in range(0, len(self._raw), 4):
            f32_l.append(struct.unpack('>f', self._raw[i:i+4])[0])
        return f32_l

    def to_f64(self) -> List[float]:
        """ to IEEE double precision 64 bits """
        f64_l = []
        for i in range(0, len(self._raw), 8):
            f64_l.append(struct.unpack('>d', self._raw[i:i+8])[0])
        return f64_l

    def swap_bytes(self):
        """ Swapped bytes in the input bytearray (b'1234' -> b'2143') """
        sw_value = bytearray(len(self._raw))
        for i in range(0, len(self._raw), 2):
            sw_value[i] = self._raw[i+1]
            sw_value[i+1] = self._raw[i]
        self._raw = bytes(sw_value)
        return self

    def swap_words(self):
        """ Swapped words in the input bytearray (b'1234' -> b'3412') """
        sw_value = bytearray(len(self._raw))
        for i in range(0, len(self._raw), 4):
            sw_value[i:i+2] = self._raw[i+2:i+4]
            sw_value[i+2:i+4] = self._raw[i:i+2]
        self._raw = bytes(sw_value)
        return self


convert = _Convert()


class _Response:
    """ An helper class for formatting the output of Modbus client functions. """

    def __init__(self, items: Union[list, None]) -> None:
        self.items = items

    # def __str__(self) -> str:
    #     return str(self.items)

    # def __repr__(self) -> str:
    #     return repr(self.items)

    def as_bytes(self) -> Optional[bytes]:
        if isinstance(self.items, list):
            return convert.from_u16(self.items).to_bytes()

    def as_str(self, encoding: str = 'iso-8859-1') -> Optional[str]:
        if isinstance(self.items, list):
            ret_str = convert.from_u16(self.items).to_bytes().decode(encoding)
            return ret_str.rstrip('\x00')

    def as_hex(self) -> Optional[list]:
        if isinstance(self.items, list):
            return [f'0x{x:04x}' for x in self.items]

    def as_u16(self) -> Optional[list]:
        if isinstance(self.items, list):
            return convert.from_u16(self.items).to_u16()

    def as_i16(self) -> Optional[list]:
        if isinstance(self.items, list):
            return convert.from_u16(self.items).to_i16()

    def as_u32(self) -> Optional[list]:
        if isinstance(self.items, list):
            return convert.from_u16(self.items).to_u32()

    def as_i32(self) -> Optional[list]:
        if isinstance(self.items, list):
            return convert.from_u16(self.items).to_i32()

    def as_f32(self) -> Optional[list]:
        if isinstance(self.items, list):
            return _Convert().from_u16(self.items).to_f32()

    def as_f64(self) -> Optional[list]:
        if isinstance(self.items, list):
            return convert.from_u16(self.items).to_f64()


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
