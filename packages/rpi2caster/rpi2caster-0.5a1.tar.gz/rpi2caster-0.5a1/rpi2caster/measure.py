# -*- coding: utf-8 -*-
"""Line length and character width module"""
from .global_settings import UI
from .cfg_parser import get_config
from .exceptions import NotConfigured, ConfigFileUnavailable
from .wedge_data import Wedge


class Measure(object):
    """Chooses and represents a line length"""
    symbols = ['Pt', 'pt', 'Pp', 'pp', 'cc', 'dd', 'cm', 'mm', 'in', '"']
    units = {'Pt': 12.0, 'pt': 1.0,
             'Pp': 12*0.166/0.1667, 'pp': 0.166/0.1667,
             'cc': 12*0.1776/0.1667, 'dd': 0.1776/0.1667,
             'cm': 0.3937*72, 'mm': 0.03937*72, '"': 72.0, 'in': 72.0}
    # Get the default line length from config
    try:
        default_value = get_config('Preferences', 'default_measure')
    except (NotConfigured, ConfigFileUnavailable):
        default_value = 25
    # Get the measurement unit
    try:
        default_unit = get_config('Preferences', 'measurement_unit')
    except (NotConfigured, ConfigFileUnavailable):
        default_unit = 'cc'

    def __init__(self, value=default_value, unit=default_unit, manual=True):
        try:
            if manual or not value:
                raise ValueError
            string = '%s%s' % (value, unit)
            self.points = parse_value(string)
        except (TypeError, ValueError, AttributeError):
            self.points = enter(value, unit)

    def __str__(self):
        return '%s%s' % (self.type_units, Measure.default_unit)

    @property
    def type_units(self):
        """Get a value in default units specified in configuration"""
        # Get the coefficient for calculation
        factor = 1 / Measure.units.get(Measure.default_unit, 1)
        return round(self.points * factor, 2)

    def ems(self, type_size=12):
        """Gets the number of ems of specified type size"""
        return round(self.points / type_size, 2)

    def monotype_units(self, wedge=Wedge()):
        """Calculates the line length in wedge's units"""
        return round(self.points / wedge.units_to_points_factor, 2)


def enter(value=0, unit=Measure.default_unit):
    """Enter the line length, choose measurement units
    (for e.g. British or European measurement system).
    Return length in DTP points."""
    def unit_help():
        """Display a help text about available units"""
        text = ('\n\nAvailable units:\n'
                '    dd - European Didot point,\n'
                '    cc - cicero (=12dd, .1776"),\n'
                '    pp - US printer\'s pica point,\n'
                '    Pp - US pica (=12pp, .1660"),\n'
                '    pt - DTP point = 1/72",\n'
                '    Pt - DTP pica (=12pt, .1667"),\n'
                '    ", in - inch;   '
                'mm - millimeter;   cm - centimeter\n\n')
        UI.display(text)

    prompt = 'Enter the length/width value and unit (or "?" for help)'
    value = value or Measure.default_value
    default_value = '%s%s' % (value, unit)
    while True:
        # If 0, use default
        raw_string = UI.enter_data_or_default(prompt, default_value)
        if '?' in raw_string:
            # Display help message and start again
            unit_help()
            continue
        try:
            return parse_value(raw_string)
        except (TypeError, ValueError):
            print('Incorrect value - enter again...')


def parse_value(raw_string):
    """Parse the entered value with units"""
    factor = 1
    string = raw_string.strip()
    for symbol in Measure.symbols:
        # End after first match
        if string.endswith(symbol):
            string = string.replace(symbol, '')
            # Default unit - 1pt
            factor = Measure.units.get(symbol, 1)
            break
    else:
        factor = Measure.units.get(Measure.default_unit, 1)
    # Filter the string
    num_string = ''.join(x for x in string if x.isdigit() or x is '.')
    # Convert the value with known unit to DTP points
    points = float(num_string) * factor
    return round(points, 2)
