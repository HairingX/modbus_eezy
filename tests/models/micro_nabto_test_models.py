from collections.abc import Callable
from src.modbus_remote import *

class ModbusTestDatapointKey(ModbusDatapointKey):
    MAJOR_VERSION = "major_version"
    
class ModbusTestDevice(ModbusDeviceBase):
    def __init__(self, device_info: ModbusDeviceInfo):
        super().__init__(device_info)

        self._attr_manufacturer="TEST"
        self._attr_model_name="TEST"
        self._attr_datapoints = [
            ModbusDatapoint(key=ModbusTestDatapointKey.MAJOR_VERSION, read_address=1, divider=1, signed=True, extra={"default_read": True}),
        ]
        self._attr_setpoints = []

class ModbusTestDeviceAdapter(ModbusDeviceAdapter):

    def _translate_to_model(self, device_info: ModbusDeviceInfo) -> Callable[[ModbusDeviceInfo], ModbusDevice]|None:
        return ModbusTestDevice

class ModbusTestMicroNabto(MicroNabto):
   _attr_adapter = ModbusTestDeviceAdapter()