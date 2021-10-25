import dataclasses as d
import subprocess, re

class DeviceList:

    def __init__(self):
        res = subprocess.run(R'iio_info -S', shell=True, stdout=subprocess.PIPE)
        lines = res.stdout.decode('utf-8').splitlines()
        adress_re = re.compile(r'\d+:.*')
        serial_re = re.compile(r'[\d|a-f]{34}')
        usb_re = re.compile(r'usb:\d+\.\d+\.\d+')
        devices = []
        for line in lines:
            line = line.strip()
            if not adress_re.fullmatch(line):
                continue
            serial = serial_re.search(line)
            uri_usb = usb_re.search(line)
            if serial == None or uri_usb == None:
                continue
            devices.append(Device(serial.group(), uri_usb.group()))
        self.devices = devices
    
    def find_by_serial(self, serial: str):
        for device in self.devices:
            if device.serial == serial:
                return device
        return None

@d.dataclass
class Device:

    serial: str
    uri_usb: str = None
