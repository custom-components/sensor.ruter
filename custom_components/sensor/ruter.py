"""
A sensor platform that gives you information about next departures.

For more details about this component, please refer to the documentation at
https://github.com/custom-components/sensor.ruter
"""
import logging
from datetime import timedelta
import dateutil.parser
import voluptuous as vol
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (PLATFORM_SCHEMA)

__version__ = '3.0.0'

REQUIREMENTS = ['pyruter==0.1.1']

CONF_STOPID = 'stopid'
CONF_DESTINATION = 'destination'
CONF_DEPARTURES = 'numer_of_departures'

ATTR_DESTINATION = 'destination'
ATTR_LINE = 'line'
ATTR_STOPID = 'stopid'

SCAN_INTERVAL = timedelta(seconds=10)

UNAVAILABLE = 'Not Available'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_STOPID): cv.string,
    vol.Required(CONF_DEPARTURES, default=1): cv.positive_int,
    vol.Optional(CONF_DESTINATION, default='None'): cv.string,
})

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the platform."""
    sensors = []
    stopid = config.get(CONF_STOPID)
    destination = config.get(CONF_DESTINATION)
    numer_of_departures = config.get(CONF_DEPARTURES)
    if numer_of_departures > 1:
        index = 1
        while index < (numer_of_departures + 1):
            sensors.append(RuterSensor(stopid, destination, index))
            index = index + 1
        add_devices(sensors)
    else:
        add_devices([RuterSensor(stopid, destination, numer_of_departures)])


class RuterSensor(Entity):
    """Sensor class."""

    def __init__(self, stopid, destination, index):
        """Initialize the sensor."""
        import pyruter
        self._ruter = pyruter
        self._stopid = stopid
        self._defined_destination = destination
        self._index = index
        self.update()

    def update(self):
        """Update the sensor."""
        result = self._ruter.get_departure_info(self._stopid,
                                                self._defined_destination)
        if result[0]['success']:
            self._line = result[self._index]['line']
            self._destination = result[self._index]['destination']
            time = result[self._index]['time']
            deptime = dateutil.parser.parse(time)
            self._state = deptime.strftime("%H:%M")
        else:
            self._state = UNAVAILABLE
            self._line = UNAVAILABLE
            self._destination = UNAVAILABLE

    @property
    def name(self):
        """Set sensor name."""
        if not self._defined_destination:
            name = 'Ruter'
        else:
            name = 'Ruter - ' + self._defined_destination
        return name

    @property
    def state(self):
        """Set sensor state."""
        return self._state

    @property
    def icon(self):
        """Set sensor icon."""
        return 'mdi:bus'

    @property
    def device_state_attributes(self):
        """Set sensor attributes."""
        return {
            ATTR_LINE: self._line,
            ATTR_DESTINATION: self._destination,
            ATTR_STOPID: self._stopid
        }
