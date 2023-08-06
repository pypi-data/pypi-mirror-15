import logging
from pyhomematic.devicetypes.generic import HMDevice
from pyhomematic.devicetypes.helper import HelperLowBat, HelperSabotage, HelperBinaryState

LOG = logging.getLogger(__name__)


class HMSensor(HMDevice):
    pass


class HMBinarySensor(HMDevice):
    pass


class ShutterContact(HMBinarySensor, HelperBinaryState, HelperLowBat, HelperSabotage):
    """
    HM-Sec-SC, HM-Sec-SC-2, ZEL STG RM FFK, HM-Sec-SCo
    Door / Window contact that emits its open/closed state.
    """
    def is_open(self, channel=1):
        """ Returns True if the contact is open. """
        return bool(self.get_state(channel))

    def is_closed(self, channel=1):
        """ Returns True if the contact is closed. """
        return not bool(self.get_state(channel))


class RotaryHandleSensor(HMBinarySensor, HelperBinaryState, HelperLowBat, HelperSabotage):
    """
    HM-Sec-RHS, ZEL STG RM FDK, HM-Sec-RHS-2, HM-Sec-xx
    Window handle contact
    """
    def is_open(self, channel=1):
        """ Returns True if the handle is set to open. """
        return self.get_state(channel) == 2

    def is_closed(self, channel=1):
        """ Returns True if the handle is set to closed. """
        return self.get_state(channel) == 0

    def is_tilted(self, channel=1):
        """ Returns True if the handle is set to tilted. """
        return self.get_state(channel) == 1

class Smoke(HMBinarySensor, HelperBinaryState):
    """
    HM-Sec-SD, HM-Sec-SD-Generic
    Smoke alarm
    """
    def is_smoke(self, channel=1):
        """ Return True if smoke is detected """
        return bool(self.get_state(channel))


class SmokeV2(Smoke, HelperLowBat):
    """
    HM-Sec-SD-2, HM-Sec-SD-2-Generic
    Smoke alarm
    """
    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.ATTRIBUTENODE.update({"ERROR_ALARM_TEST": 'c',
                                   "ERROR_ALARM_TEST": 'c'})

class Remote(HMBinarySensor):
    """
    BRC-H, HM-RC-2-PBU-FM, HM-RC-Dis-H-x-EU, HM-RC-4, HM-RC-4-B, HM-RC-4-2,
    HM-RC-4-3, HM-RC-4-3-D, HM-RC-8, HM-RC-12, HM-RC-12-B, HM-RC-12-SW,
    HM-RC-19, HM-RC-19-B, HM-RC-19-SW, HM-RC-Key3, HM-RC-Key3-B, HM-RC-Key4-2,
    HM-RC-Key4-3, HM-RC-Sec3, HM-RC-Sec3-B, HM-RC-Sec4-2, HM-RC-Sec4-3,
    HM-RC-P1, HM-RC-SB-X, HM-RC-X, HM-PB-2-WM, HM-PB-4-WM, HM-PB-6-WM55,
    HM-PB-2-WM55-2, HM-PB-2-WM55, ZEL STG RM WT 2, 263 135
    Remote handle buttons
    """
    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        self.BINARYNODE.update({"PRESS_SHORT": 'c', "PRESS_LONG": 'c'})

    @property
    def ELEMENT(self):
        if "RC-2" in self.TYPE or "PB-2" in self.TYPE:
            return 2
        if "Sec3" in self.TYPE or "Key3" in self.TYPE:
            return 3
        if "RC-4" in self.TYPE or "PB-4" in self.TYPE:
            return 4
        if "Sec4" in self.TYPE or "Key4" in self.TYPE:
            return 4
        if "PB-6" in self.TYPE:
            return 6
        if "RC-8" in self.TYPE:
            return 8
        if "RC-12" in self.TYPE:
            return 12
        if "RC-19" in self.TYPE:
            return 19
        return 1


class Motion(HMBinarySensor, HMSensor):
    """
    HM-Sen-MDIR-SM, HM-Sen-MDIR-O, HM-MD, HM-Sen-MDIR-O-2
    """
    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION": 'c'})
        self.SENSORNODE.update({"BRIGHTNESS": 'c'})

    def is_motion(self, channel=1):
        """ Return True if motion is detected """
        return bool(self.getBinaryData("MOTION", channel))

    def get_brightness(self, channel=1):
        """ Return brightness from 0 (dark ) to 255 (bright) """
        return int(self.getSensorData("BRIGHTNESS", channel))


class MotionV2(Motion, HelperSabotage):
    """
    HM-Sec-MDIR-3, HM-Sec-MDIR-2, HM-Sec-MDIR, 263 162, HM-Sec-MD
    """
    pass


class RemoteMotion(Remote, Motion):
    """
    HM-Sen-MDIR-WM55
    """
    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.BINARYNODE.update({"MOTION": 3,
                                "PRESS_SHORT": 'c',
                                "PRESS_LONG": 'c'})
        self.SENSORNODE.update({"BRIGHTNESS": 3})

    @property
    def ELEMENT(self):
        return 2


class AreaThermostat(HMSensor):
    """
    ASH550I, ASH550, HM-WDS10-TH-O, 263 158, HM-WDS20-TH-O, HM-WDS40-TH-I,
    263 157, IS-WDS-TH-OD-S-R3
    """
    def __init__(self, device_description, proxy, resolveparamsets=False):
        super().__init__(device_description, proxy, resolveparamsets)

        # init metadata
        self.SENSORNODE.update({"TEMPERATURE": 'c', "HUMIDITY": 'c'})

    def get_temperature(self, channel=1):
        return float(self.getSensorData("TEMPERATURE", channel))

    def get_humidity(self, channel=1):
        return int(self.getSensorData("HUMIDITY", channel))


DEVICETYPES = {
    "HM-Sec-SC": ShutterContact,
    "HM-Sec-SC-2": ShutterContact,
    "HM-Sec-SCo": ShutterContact,
    "ZEL STG RM FFK": ShutterContact,
    "HM-Sec-RHS": RotaryHandleSensor,
    "ZEL STG RM FDK": RotaryHandleSensor,
    "HM-Sec-RHS-2": RotaryHandleSensor,
    "HM-Sec-xx": RotaryHandleSensor,
    "HM-Sec-SD": Smoke,
    "HM-Sec-SD-Generic": Smoke,
    "HM-Sec-SD-2": SmokeV2,
    "HM-Sec-SD-2-Generic": SmokeV2,
    "BRC-H": Remote,
    "HM-RC-2-PBU-FM": Remote,
    "HM-RC-Dis-H-x-EU": Remote,
    "HM-RC-4": Remote,
    "HM-RC-4-B": Remote,
    "HM-RC-4-2": Remote,
    "HM-RC-4-3": Remote,
    "HM-RC-4-3-D": Remote,
    "HM-RC-8": Remote,
    "HM-RC-12": Remote,
    "HM-RC-12-B": Remote,
    "HM-RC-12-SW": Remote,
    "HM-RC-19": Remote,
    "HM-RC-19-B": Remote,
    "HM-RC-19-SW": Remote,
    "HM-RC-Key3": Remote,
    "HM-RC-Key3-B": Remote,
    "HM-RC-Key4-2": Remote,
    "HM-RC-Key4-3": Remote,
    "HM-RC-Sec3": Remote,
    "HM-RC-Sec3-B": Remote,
    "HM-RC-Sec4-2": Remote,
    "HM-RC-Sec4-3": Remote,
    "HM-RC-P1": Remote,
    "HM-RC-SB-X": Remote,
    "HM-RC-X": Remote,
    "HM-PB-2-WM": Remote,
    "HM-PB-4-WM": Remote,
    "HM-PB-6-WM55": Remote,
    "RC-H": Remote,
    "atent": Remote,
    "ZEL STG RM HS 4": Remote,
    "HM-PB-2-WM55-2": Remote,
    "HM-PB-2-WM55": Remote,
    "ZEL STG RM WT 2": Remote,
    "263 135": Remote,
    "HM-Sen-MDIR-WM55": RemoteMotion,
    "HM-Sen-MDIR-SM": Motion,
    "HM-Sen-MDIR-O": Motion,
    "HM-MD": Motion,
    "HM-Sen-MDIR-O-2": Motion,
    "HM-Sec-MDIR-3": MotionV2,
    "HM-Sec-MDIR-2": MotionV2,
    "HM-Sec-MDIR": MotionV2,
    "263 162": MotionV2,
    "HM-Sec-MD": MotionV2,
    "ASH550I": AreaThermostat,
    "ASH550": AreaThermostat,
    "HM-WDS10-TH-O": AreaThermostat,
    "263 158": AreaThermostat,
    "HM-WDS20-TH-O": AreaThermostat,
    "HM-WDS40-TH-I": AreaThermostat,
    "263 157": AreaThermostat,
    "IS-WDS-TH-OD-S-R3": AreaThermostat
}
