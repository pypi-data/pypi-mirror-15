# pndatapush
Python module to push data to the Pervasive Nation IoT network. It saves data locally until there is internet access. 

#To install

```python
pip install --upgrade pndatapush
```

#To run an example

```python
python examples/gatherdata.py
```

# Easiest way to add to your project
Create an instance of the Offline class.


```python
from pndatapush.offline import Offline
from pndatapush.pushdata import PNPushData
#Set the PervasiveNation Auth token
pnpushdata = PNPushData(pervasivenation_authtoken="MYREALLYLONGTOKENIGOTSECRET")
offline = Offline(payload_consumers=[pnpushdata])
```

## OR if you want to use environment variables:

```
#set your PervasiveNation Auth token by using an environment variable before starting your applicaiton
export PERVASIVENATION_AUTHTOKEN="MYREALLYLONGTOKENIGOTSECRET"
```

```python
from pndatapush.offline import Offline
from pndatapush.pushdata import PNPushData
offline = Offline(payload_consumers=[PNPushData]) #PNPushData is a data consumer class. see pnpushdata.pushdata.PNPushData
```

## AND if you want the local database in your current directory:

```python
import os
from pndatapush.offline import Offline
from pndatapush.pushdata import PNPushData
#Set the PervasiveNation Auth token
pnpushdata = PNPushData(pervasivenation_authtoken="MYREALLYLONGTOKENIGOTSECRET")
#Set the local SQLite DB path
offline = Offline(payload_consumers=[pnpushdata], dbpath='sqlite:///%s/sensordata.db' % os.path.dirname(os.path.realpath(__file__)))
```

Then when sensor data is received save the data

```python
device_identifier = '12456'
offline.save(device_identifier, 30.00) #save(self, deviceid, payload):
```

