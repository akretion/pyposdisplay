# -*- coding: utf-8 -*-
###############################################################################
#
#   Python Point Of Sale Display Librarie
#   Copyright (C) 2014-2016 Akretion (http://www.akretion.com).
#   @author Alexis de Lattre <alexis.delattre@akretion.com>
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from unidecode import unidecode
from serial import Serial
import serial.tools.list_ports
import usb.core
import logging
_logger = logging.getLogger(__name__)


#    itersubclasses
#    Author: Joel Grand-Guillaume
#    Copyright 2011-2012 Camptocamp SA
#    Licence AGPL v3
def itersubclasses(cls, _seen=None):
    """
    itersubclasses(cls)

    Generator over all subclasses of a given class, in depth first order.

    >>> list(itersubclasses(int)) == [bool]
    True
    >>> class A(object): pass
    >>> class B(A): pass
    >>> class C(A): pass
    >>> class D(B,C): pass
    >>> class E(D): pass
    >>>
    >>> for cls in itersubclasses(A):
    ...     print(cls.__name__)
    B
    D
    E
    C
    >>> # get ALL (new-style) classes currently defined
    >>> [cls.__name__ for cls in itersubclasses(object)] #doctest: +ELLIPSIS
    ['type', ...'tuple', ...]
    """
    if not isinstance(cls, type):
        raise TypeError('itersubclasses must be called with '
                        'new-style classes, not %.100r' % cls)
    if _seen is None:
        _seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError:  # fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub in itersubclasses(sub, _seen):
                yield sub


class Driver(object):
    _default_driver = 'bixolon'

    def __init__(self, config=None, use_driver_name=None):
        self.driver = self._get_driver(
            config=config,
            use_driver_name=use_driver_name)
        super(Driver, self).__init__()

    def _get_driver(self, config=None, use_driver_name=None):
        if config is None:
            config = {}
        available_driver = []
        if use_driver_name:
            for cls in itersubclasses(AbstractDriver):
                if cls._name == use_driver_name:
                    return cls(config)
                else:
                    available_driver.append(cls._name)
        else:
            for hardware in usb.core.find(find_all=True):
                hardware_id = (hex(hardware.idVendor), hex(hardware.idProduct))
                for cls in itersubclasses(AbstractDriver):
                    if hardware_id in cls._vendor_id_product_id:
                        _logger.debug(
                            'Hardware found! Vendor id %s Product id %s '
                            'use driver %s' % (
                                hardware_id[0],
                                hardware_id[1],
                                cls._name))
                        return cls(config)
            _logger.debug('Not Driver found, use default driver %s'
                          % self._default_driver)
            return self._get_driver(
                config=config,
                use_driver_name=self._default_driver)
        raise ValueError(
            'The driver %s do not exist. Available driver : %s'
            % (use_driver_name, available_driver))

    def send_text(self, lines):
        assert isinstance(lines, list), 'lines should be a list'
        self.driver.send_text(lines)

    def get_status(self):
        status = "disconnected"
        messages = []
        connected_comports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        _logger.debug(connected_comports)
        ports = [p[0] for p in connected_comports]
        if self.driver.device_name in ports:
            status = "connected"
        else:
            devices = [p[1] for p in connected_comports]
            messages = ["Available device:"] + devices
        return {"status": status, "messages": messages}


class AbstractDriver(object):
    """ The Abstract class is the base driver class for the display
    Every driver must inherit this class.

    You can define a new class by adding

    class MyNewDriver(AbstractDriver):
        _name = 'mynewdriver'

        def send_text(self, lines):
            #code to print the text on your device


    You can also add a new driver by creating a new one based on
    an existing one

    class Bixolon2000Driver(BixolonDriver):
        _name = 'bixolon2000'

        def send_text(self, lines):
            lines = ['I am Bixolon 2000', lines[0]]
            super(Bixolon2000Driver, self).send_text(lines)
    """

    def __init__(self, config):
        self.device_name = config.get(
            'customer_display_device_name', '/dev/ttyUSB0')
        self.device_rate = int(config.get(
            'customer_display_device_rate', 9600))
        self.device_timeout = float(config.get(
            'customer_display_device_timeout', 0.05))
        self.serial = False
        if self.device_name == "auto":
            self.device_name = self._find_auto_device_name()

    def _find_auto_device_name(self):
        connected_comports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        _logger.debug(connected_comports)
        for port in connected_comports:
            # Name of serial to USB main providers
            strings_to_find = ["Serial", "serial", "Prolific", "prolific", "FVDI", "USB Virtual COM"]
            if any(string in port[1] for string in strings_to_find):
                return port[0]

    def cmd_serial_write(self, command):
        '''If your LCD requires a prefix and/or suffix on all commands,
        you should inherit this function'''
        assert isinstance(command, bytes), 'command must be bytes'
        self.serial_write(command)

    def serial_write(self, text):
        assert isinstance(text, bytes), 'text must be bytes'
        self.serial.write(text)

    def clear_customer_display(self):
        '''If your LCD has different clearing instruction, you should inherit
        this function'''
        # Bixolon spec : 12. "Clear Display Screen and Clear String Mode"
        # This seems to be common to several displays, so I put it in the
        # abstract driver
        self.cmd_serial_write(b'\x0C')
        _logger.debug('Customer display cleared')

    def display_text(self, lines):
        _logger.debug(
            "Preparing to send the following lines to LCD: %s" % lines)
        # We don't check the number of rows/cols here, because it has already
        # been checked in the POS client in the JS code
        lines_ascii = []
        for line in lines:
            lines_ascii.append(unidecode(line))
        self.clear_customer_display()
        for i, dline in enumerate(lines_ascii):
            self.serial_write(dline.encode("ascii"))
            # Do not go to new line if this is the last one
            if i < len(lines_ascii) - 1:
                self.move_down(i+1)  # Line number starts at 1

    def send_text(self, lines):
        '''This function sends the data to the serial/usb port.
        We open and close the serial connection on every message display.
        Why ?
        1. Because it is not a problem for the customer display
        2. Because it is not a problem for performance, according to my tests
        3. Because it allows recovery on errors : you can unplug/replug the
        customer display and it will work again on the next message without
        problem
        '''
        try:
            _logger.debug(
                'Opening serial port %s for customer display with baudrate %d'
                % (self.device_name, self.device_rate))
            self.serial = Serial(
                self.device_name, self.device_rate,
                timeout=self.device_timeout)
            _logger.debug('serial.is_open = %s' % self.serial.isOpen())
            self.setup_customer_display()
            self.display_text(lines)
        except Exception as e:
            _logger.error('Exception in serial connection: %s' % str(e))
            raise
        finally:
            if self.serial:
                _logger.debug('Closing serial port for customer display')
                self.serial.close()

    def move_down(self, row):
        self.move_cursor(1, row + 1)

    def move_cursor(self, col, row):
        # Always use this function as it is stateless and depending on
        # The hardware the cursor behaviour can differ
        # Bixolon spec : 11. "Move Cursor to Specified Position"
        _logger.debug(f'Move cursor to column {col} and line {row}')
        self.cmd_serial_write(b'\x1F\x24' + (chr(col) + chr(row)).encode('ascii'))


class BixolonDriver(AbstractDriver):
    _name = 'bixolon'
    _vendor_id_product_id = [
        # (vendor_id, product_id)
        ('0x1504', '0x8c'),  # BCD-2000 in BCD-2000K config mode
        ('0x1504', '0x11'),  # BCD-1100
        ('0x0403', '0x6001'),  # BCD-1000
    ]

    def setup_customer_display(self):
        '''Set LCD cursor to off
        If your LCD has different setup instruction(s), you should
        inherit this function'''
        # Bixolon spec : 35. "Set Cursor On/Off"
        self.cmd_serial_write(b'\x1F\x43\x00')
        _logger.debug('LCD cursor set to off')


class LabauDriver(AbstractDriver):
    _name = 'labau'
    _vendor_id_product_id = [
        # (vendor_id, product_id)
        ('0x067b', '0x2303'),  # Labau LD240
    ]

    def setup_customer_display(self):
        '''Set LCD cursor to off
        If your LCD has different setup instruction(s), you should
        inherit this function'''
        # Overwrite mode ? (no documentation)
        self.cmd_serial_write(b'\x1F\x01')
        _logger.debug('Overwrite mode')

    def move_down(self, row):
        _logger.debug('Move One line down')
        self.cmd_serial_write(b'\x0A')
        self.cmd_serial_write(b'\x0D')


class EpsonDriver(AbstractDriver):
    _name = 'epson'
    _vendor_id_product_id = [
        ('0x1208', '0x0780'),  # Epson Seiko DM-D110
    ]

    def setup_customer_display(self):
        # Initialize display (spec page 67)
        # but no need to do it every time
        # self.cmd_serial_write(b'\x1B\x40')
        # Specifies the display mode for the current window (Function 3)
        # (spec page 152)
        # hexa : 1F 28 44 pl ph fn wno m1 m2 m3
        # pl = 0x04
        # ph = 0x00
        # fn = 0x03
        # m1 = 101 (0x65) : 20 col x 2 lines
        # m2 (window background): 1 (nontransparent)
        # m3 = 2
        # self.cmd_serial_write(b'\x1F\x28\x44\x04\x00\x03\x01\x65\x01\x02')
        # Note: Seems that, in the first version of the code using chr()
        # the command was wrong and was missing 'wmo'
        # same as previous: no need to do it every time
        # Turn cursor display mode off (spec page 99)
        self.cmd_serial_write(b'\x1F\x43\x00')
        _logger.debug('LCD cursor set to off')

    def serial_write(self, text):
        assert isinstance(text, bytes), 'text must be bytes'
        self.serial.write(text)
        self.serial.read()
