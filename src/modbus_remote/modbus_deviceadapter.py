import logging
from typing import Dict, List
from collections.abc import Callable

from .modbus_models import ( MODBUS_VALUE_TYPES, ModbusDeviceInfo, ModbusPointKey, ModbusDevice, ModbusDatapoint, ModbusDatapointKey, ModbusSetpoint, ModbusSetpointKey )

_LOGGER = logging.getLogger(__name__)

class ModbusDeviceAdapter(ModbusDevice):
    _device_info: ModbusDeviceInfo
    _loaded_model: ModbusDevice|None
    
    def __init__(self):
        pass
    
    def instantiate(self, device_info: ModbusDeviceInfo) -> None:
        self._device_info = device_info
        model_to_load = self._translate_to_model(device_info)
        if model_to_load == None:
            raise Exception("Invalid model")
        loaded_model = model_to_load(device_info)
        loaded_model.instantiate(device_info)
        self._loaded_model = loaded_model
        self.ready = True
     
    def _translate_to_model(self, device_info: ModbusDeviceInfo) -> Callable[[ModbusDeviceInfo], ModbusDevice]|None:
        """Translate the model to the correct device model, must be implemented in the subclass"""
        raise NotImplementedError("Method not implemented")

    def provides_model(self, device_info: ModbusDeviceInfo) -> bool:
        return self._translate_to_model(device_info) is not None
    
    #region ModbusDevice
    
    def _get_loaded_model(self) -> ModbusDevice:
        if self._loaded_model is None:
            raise Exception("No model loaded")
        return self._loaded_model

    def get_datapoint(self, key: ModbusDatapointKey) -> ModbusDatapoint|None:
        return self._get_loaded_model().get_datapoint(key)

    def get_datapoints_for_read(self) -> List[ModbusDatapoint]:
        return self._get_loaded_model().get_datapoints_for_read()

    def get_device_model(self) -> int: 
        return self._get_loaded_model().get_device_model()
    
    def get_device_number(self) -> int: 
        return self._get_loaded_model().get_device_number()
    
    def get_device_id(self) -> str:
        return self._get_loaded_model().get_device_id()

    def get_device_host(self) -> str:
        return self._get_loaded_model().get_device_host()

    def get_device_port(self) -> int:
        return self._get_loaded_model().get_device_port()
  
    def get_manufacturer(self) -> str:
        return self._get_loaded_model().get_manufacturer()
    
    def get_max_value(self, key: ModbusSetpointKey) -> float|int|None:
        return self._get_loaded_model().get_max_value(key)

    def get_min_value(self, key: ModbusSetpointKey) -> float|int|None:
        return self._get_loaded_model().get_min_value(key)

    def get_model_name(self) -> str:
        return self._get_loaded_model().get_model_name()

    def get_setpoint(self, key: ModbusSetpointKey) -> ModbusSetpoint|None:
        return self._get_loaded_model().get_setpoint(key)

    def get_setpoint_step(self, key: ModbusSetpointKey) -> float|int:
        return self._get_loaded_model().get_setpoint_step(key)

    def get_setpoints_for_read(self) -> List[ModbusSetpoint]:
        return self._get_loaded_model().get_setpoints_for_read()
    
    def get_slave_device_model(self) -> int: 
        return self._get_loaded_model().get_slave_device_model()
    
    def get_slave_device_number(self) -> int: 
        return self._get_loaded_model().get_slave_device_number()
    
    def get_unit_of_measure(self, key: ModbusPointKey) -> str|None:
        return self._get_loaded_model().get_unit_of_measure(key)
    
    def get_value(self, key: ModbusPointKey) -> MODBUS_VALUE_TYPES|None:
        return self._get_loaded_model().get_value(key)
   
    def get_values(self) -> Dict[ModbusPointKey, MODBUS_VALUE_TYPES|None]:
        return self._get_loaded_model().get_values()
    
    def has_value(self, key: ModbusPointKey) -> bool:
        return self._get_loaded_model().has_value(key)

    def provides(self, key: ModbusPointKey) -> bool:
        return self._get_loaded_model().provides(key)

    def set_read(self, key: ModbusPointKey, read: bool) -> bool:
        return self._get_loaded_model().set_read(key, read)

    def set_value(self, key: ModbusPointKey, value: MODBUS_VALUE_TYPES) -> MODBUS_VALUE_TYPES|None:
        return self._get_loaded_model().set_value(key, value)
    
    #endregion ModbusDevice