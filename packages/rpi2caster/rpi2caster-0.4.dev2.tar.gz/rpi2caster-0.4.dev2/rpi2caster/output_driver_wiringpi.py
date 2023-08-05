# -*- coding: utf-8 -*-
"""output_driver_wiringpi - wiringPi2-based output driver for MCP23017"""

# WiringPi2 Python bindings: essential for controlling the MCP23017!
try:
    import wiringpi
except ImportError:
    print('You must install wiringpi!')

# Import mockup output driver from monotype
from .monotype import SimulationOutput, SIGNALS
from .exceptions import WrongConfiguration
from .global_settings import MCP0, MCP1


class Singleton(type):
    """Make only one object"""
    instance = None

    def __call__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class WiringPiOutputDriver(SimulationOutput):
    """A 32-channel control interface based on two MCP23017 chips"""
    pin_base = 65
    __metaclass__ = Singleton

    def __init__(self, mcp0_address=MCP0, mcp1_address=MCP1, sig_arr=SIGNALS):
        super().__init__(sig_arr=sig_arr)
        self.name = 'MCP23017 driver using wiringPi2-Python library'
        # Set up an output interface on two MCP23017 chips
        pin_base = WiringPiOutputDriver.pin_base
        wiringpi.mcp23017Setup(pin_base, mcp0_address)
        wiringpi.mcp23017Setup(pin_base + 16, mcp1_address)
        pins = [x for x in range(pin_base, pin_base+32)]
        # Update the pin base for next instances
        WiringPiOutputDriver.pin_base += 32
        self.pin_numbers = dict(zip(self.signals_arrangement, pins))
        # Set all I/O lines on MCP23017s as outputs - mode=1
        for pin in self.pin_numbers.values():
            wiringpi.pinMode(pin, 1)

    def one_on(self, sig):
        """Looks a signal up in arrangement and turns it on"""
        try:
            wiringpi.digitalWrite(self.pin_numbers[sig], 1)
        except KeyError:
            msg = ('Signal %s not defined! Signals arrangement: %s\n'
                   % (sig, self.signals_arrangement))
            raise WrongConfiguration(msg)

    def one_off(self, sig):
        """Looks a signal up in arrangement and turns it off"""
        try:
            wiringpi.digitalWrite(self.pin_numbers[sig], 0)
        except KeyError:
            msg = ('Signal %s not defined! Signals arrangement: %s\n'
                   % (sig, self.signals_arrangement))
            raise WrongConfiguration(msg)
