"""
A component which allows you to get information about next departure from spesified stop.
For more details about this component, please refer to the documentation at
https://github.com/HalfDecent/HA-Custom_components/ruter
"""
import logging
import dateutil.parser
import voluptuous as vol
from datetime import timedelta
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (PLATFORM_SCHEMA)

REQUIREMENTS = ['pyruter==0.0.4']

CONF_STOPID = 'stopid'
CONF_DESTINATION = 'destination'

ATTR_DESTINATION = 'destination'
ATTR_LINE = 'line'
ATTR_STOPID = 'stopid'
ATTR_COMPONENT = 'component'
ATTR_COMPONENT_VERSION = 'component_version'

SCAN_INTERVAL = timedelta(seconds=10)

ICON = 'mdi:bus'
COMPONENT_NAME = 'ruter'
COMPONENT_VERSION = '2.1.0'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_STOPID): cv.string,
    vol.Optional(CONF_DESTINATION, default='None'): cv.string,
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    stopid = config.get(CONF_STOPID)
    destination = config.get(CONF_DESTINATION)
    add_devices([RuterSensor(stopid, destination)])

class RuterSensor(Entity):
    def __init__(self, stopid, destination):
        from pyruter import Ruter
        self._state = None
        self._line = None
        self._destination = None
        self._ruter = Ruter()
        self._stopid = stopid
        self._defined_destination = destination
        self._component = COMPONENT_NAME
        self._componentversion = COMPONENT_VERSION  
        self.update()


    def update(self):
        result = self._ruter.getDepartureInfo(self._stopid, 
            self._defined_destination)
        if not result :
            return False
        else:
            self._line = result[1]
            self._destination = result[2]
            time = result[0]
            deptime = dateutil.parser.parse(time)
            self._state = deptime.strftime("%H:%M")
    
    @property
    def name(self):
        if not self._defined_destination:
            return 'Ruter'
        else:
            return 'Ruter - Neste avgang mot ' + self._defined_destination

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def device_state_attributes(self):
        return {
            ATTR_LINE: self._line,
            ATTR_DESTINATION: self._destination,
            ATTR_STOPID: self._stopid,
            ATTR_COMPONENT: self._component,
            ATTR_COMPONENT_VERSION: self._componentversion
        }