
from typing import Callable, Dict, List

from .modbus_models import MODBUS_VALUE_TYPES, ModbusDatapointKey, ModbusSetpointKey
from .modbus_deviceadapter import ModbusDeviceAdapter

class ModbusRemote:
    _attr_adapter: ModbusDeviceAdapter
    _subscribers: Dict[ModbusDatapointKey|ModbusSetpointKey, List[Callable[[MODBUS_VALUE_TYPES|None, MODBUS_VALUE_TYPES|None], None]]] = {}
    """Callable[old_value, new_value]"""
    
    def __init__(self):
        raise NotImplementedError("Method not implemented")
    def is_connected(self) -> bool: 
        raise NotImplementedError("Method not implemented")
    
    def get_device_host(self): return self._attr_adapter.get_device_host()
    def get_device_id(self): return self._attr_adapter.get_device_id()
    def get_device_manufacturer(self): return self._attr_adapter.get_manufacturer()
    def get_device_model(self): return self._attr_adapter.get_device_model()
    def get_device_number(self): return  self._attr_adapter.get_device_number()
    def get_device_port(self): return self._attr_adapter.get_device_port()
    def get_loaded_model_name(self) -> str: return self._attr_adapter.get_model_name()
    def get_slave_device_model(self): return self._attr_adapter.get_slave_device_model()
    def get_slave_device_number(self): return self._attr_adapter.get_slave_device_number()
    
    def subscribe(self, key: ModbusDatapointKey|ModbusSetpointKey, update_method: Callable[[MODBUS_VALUE_TYPES|None, MODBUS_VALUE_TYPES|None], None]):
        if key not in self._subscribers:
            self._subscribers[key] = []
        self._subscribers[key].append(update_method)
        value = self._attr_adapter.get_value(key)
        if value is not None:
            update_method(None, value)
    
    def unsubscribe(self, key: ModbusDatapointKey|ModbusSetpointKey, update_method: Callable[[MODBUS_VALUE_TYPES|None, MODBUS_VALUE_TYPES|None], None]):
        subscribers = self._subscribers.get(key)
        if subscribers is None: return
        if update_method in subscribers:
            if len(subscribers) == 1:
                del self._subscribers[key]
            else: 
                subscribers.remove(update_method)
    
    
    
   