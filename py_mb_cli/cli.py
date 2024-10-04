import logging
import struct
from binascii import hexlify
from typing import List, Optional, Sequence, Union

from pyModbusTCP.client import ModbusClient


class Convert:
    """ A class for easy conversion of Modbus data formats. """

    class To:
        def __init__(self, raw: bytes) -> None:
            # args
            self.raw = raw

        def _raw_to_items(self, fmt: str) -> list:
            byte_size = struct.calcsize(fmt)
            items_l = []
            for i in range(0, len(self.raw), byte_size):
                items_l.append(struct.unpack(fmt, self.raw[i:i+byte_size])[0])
            return items_l

        def to_bytes(self) -> bytes:
            """to raw bytes"""
            return self.raw

        def to_hex(self) -> str:
            """to raw bytes"""
            return hexlify(self.raw, '-', 2).upper().decode()

        def to_str(self, encoding: str = 'iso-8859-1') -> Optional[str]:
            """to str"""
            return self.raw.rstrip(b'\x00').decode(encoding)

        def to_regs(self) -> List[int]:
            """to modbus registers (words of 16 bits)"""
            return self._raw_to_items(fmt='>H')

        def to_u16(self) -> List[int]:
            """to unsigned 16 bits"""
            return self._raw_to_items(fmt='>H')

        def to_i16(self) -> List[int]:
            """to signed 16 bits"""
            return self._raw_to_items(fmt='>h')

        def to_u32(self) -> List[int]:
            """to unsigned 32 bits"""
            return self._raw_to_items(fmt='>I')

        def to_i32(self) -> List[int]:
            """to signed 32 bits"""
            return self._raw_to_items(fmt='>i')

        def to_u64(self) -> List[int]:
            """to unsigned 64 bits"""
            return self._raw_to_items(fmt='>Q')

        def to_i64(self) -> List[int]:
            """to signed 64 bits"""
            return self._raw_to_items(fmt='>q')

        def to_f32(self) -> List[float]:
            """to IEEE single precision 32 bits"""
            return self._raw_to_items(fmt='>f')

        def to_f64(self) -> List[float]:
            """to IEEE double precision 64 bits"""
            return self._raw_to_items(fmt='>d')

        def swap_bytes(self):
            """apply a swap to bytes (b'1234' -> b'2143')"""
            sw_value = bytearray(len(self._raw))
            for i in range(0, len(self._raw), 2):
                sw_value[i] = self._raw[i+1]
                sw_value[i+1] = self._raw[i]
            self._raw = bytes(sw_value)
            return self

        def swap_words(self):
            """apply a swap to words (b'1234' -> b'3412')"""
            sw_value = bytearray(len(self._raw))
            for i in range(0, len(self._raw), 4):
                sw_value[i:i+2] = self._raw[i+2:i+4]
                sw_value[i+2:i+4] = self._raw[i:i+2]
            self._raw = bytes(sw_value)
            return self

    def _build_convert_to(self, items: Optional[Sequence], fmt: str):
        raw = bytes()
        if items:
            for item in items:
                raw += struct.pack(fmt, item)
        return Convert.To(raw)

    def from_regs(self, items: Optional[Sequence[int]]):
        """from modbus registers (words of 16 bits)"""
        return self._build_convert_to(items, fmt='>H')

    def from_u16(self, items: Union[int, Sequence[int]]):
        """from unsigned 16 bits"""
        items = [items] if isinstance(items, int) else items
        return self._build_convert_to(items, fmt='>H')

    def from_i16(self, items: Union[int, Sequence[int]]):
        """from signed 16 bits"""
        items = [items] if isinstance(items, int) else items
        return self._build_convert_to(items, fmt='>h')

    def from_u32(self, items: Union[int, Sequence[int]]):
        """from unsigned 32 bits"""
        items = [items] if isinstance(items, int) else items
        return self._build_convert_to(items, fmt='>I')

    def from_i32(self, items: Union[int, Sequence[int]]):
        """from signed 32 bits"""
        items = [items] if isinstance(items, int) else items
        return self._build_convert_to(items, fmt='>i')

    def from_u64(self, items: Union[int, Sequence[int]]):
        """from unsigned 64 bits"""
        items = [items] if isinstance(items, int) else items
        return self._build_convert_to(items, fmt='>Q')

    def from_i64(self, items: Union[int, Sequence[int]]):
        """from signed 64 bits"""
        items = [items] if isinstance(items, int) else items
        return self._build_convert_to(items, fmt='>q')

    def from_f32(self, items: Union[float, Sequence[float]]):
        """from IEEE single precision 64 bits"""
        items = [items] if isinstance(items, (int, float)) else items
        return self._build_convert_to(items, fmt='>f')

    def from_f64(self, items: Union[float, Sequence[float]]):
        """from IEEE double precision 64 bits"""
        items = [items] if isinstance(items, (int, float)) else items
        return self._build_convert_to(items, fmt='>d')


class Cli:
    """ A custom ModbusClient for creating the cli instance. """

    def __init__(self, modbus_client: ModbusClient, debug: bool):
        self.modbus_client = modbus_client
        self.debug = debug

    @property
    def debug(self):
        return logging.getLogger('pyModbusTCP.client').getEffectiveLevel() == logging.DEBUG

    @debug.setter
    def debug(self, value: bool):
        logging.getLogger('pyModbusTCP.client').setLevel(logging.DEBUG if value else logging.INFO)

    def read_bits(self, address: int, number: int = 1, d_inputs: bool = False):
        if d_inputs:
            return self.modbus_client.read_discrete_inputs(address, number)
        else:
            return self.modbus_client.read_coils(address, number)

    def read_words(self, address: int, number: int = 1, i_regs: bool = False, convert: bool = False):
        if i_regs:
            read_l = self.modbus_client.read_input_registers(address, number)
        else:
            read_l = self.modbus_client.read_holding_registers(address, number)
        if convert:
            return Convert().from_regs(read_l)
        else:
            return read_l

    def write_bits(self, address: int, value: Union[bool, list, tuple]) -> bool:
        if isinstance(value, (list, tuple)):
            return self.modbus_client.write_multiple_coils(address, value)
        else:
            return self.modbus_client.write_single_coil(address, value)

    def write_words(self, address: int, value: Union[int, list, tuple, Convert.To]) -> bool:
        if isinstance(value, Convert.To):
            value = value.to_regs()
        if isinstance(value, (list, tuple)):
            return self.modbus_client.write_multiple_registers(address, value)
        else:
            return self.modbus_client.write_single_register(address, value)
