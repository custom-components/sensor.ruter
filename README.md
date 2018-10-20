# sensor.ruter [![Build Status](https://travis-ci.com/custom-components/sensor.ruter.svg?branch=master)](https://travis-ci.com/custom-components/sensor.ruter)

A sensor platform that gives you information about next departures.
  
To get started put `/custom_components/sensor/ruter.py` here:  
`<config directory>/custom_components/sensor/ruter.py`  
  
**Example configuration.yaml:**

```yaml
sensor:
  platform: ruter
  stopid: 129302
  destination: 'Sandvika (Bussterminal)'
```

**Configuration variables:**  
  
key | description  
:--- | :---  
**platform (Required)** | The platform name.  
**stopid (Required)** | The ID of the stop you are monitoring.  
**destination (Optional)** | The destination stop of the line you want to monitor.  
**numer_of_departures (Optional)** | The number of future departures you want a sensor for. defaults to 1.
  
## Sample overview

![Sample overview](overview.png)
  
This platform is using the [Ruter reisapi API](http://reisapi.ruter.no/Help) to get the information.
 This component is only usefull for users living near Oslo, Norway that uses Ruter for transportation.
 To find the stopid go to https://ruter.no/reiseplanlegger/Stoppested and search for your stop.
 in the url after you have searched there will be an ID right after the 'Stoppested/' in a format like this (129302), the numbers there is what you need to put in the `stopid:` config option.
 The `destionation:` can be used to filter the responses, the name must be exactly the same as on the ruter.no site.  
  
***
Due to how `custom_componentes` are loaded, it is normal to see a `ModuleNotFoundError` error on first boot after adding this, to resolve it, restart Home-Assistant.

***

[buymeacoffee.com](https://www.buymeacoffee.com/ludeeus)
