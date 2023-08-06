from performance_data import PerformanceData


class Device(object):
    def __init__(self, device, uri, client, has_details=False):
        """
        Instantiate a new Device object
        
        :param device: A dict from the /api/device request
        :type  device: ``dict``
        
        :param client: The API client
        :type  client: :class:`Client`
        
        """
        self._client = client
        self.uri = uri
        if has_details:
            self.description = device['name']
        else:
            self.description = device['description']
        if not has_details:
            self._fill_details()
        else:
            self.details = device

    def __repr__(self):
        return self.description

    def _fill_details(self):
        """
        Get the detailed information about the device
        """
        d = self._client.get(self.uri)
        self.details = d.json()
        
    def performance_counters(self):
        """
        Get a list of performance counters for this device
        
        :rtype: ``list`` of :class:`PerformanceData`
        """
        if self.details is None:
            self._fill_details()
        counters=[]
        u = self.details['performance_data']['URI']
        for u_data in self._client.get(u).json()['result_set']:
            counters.append(PerformanceData(self._client, u_data))
        return counters
