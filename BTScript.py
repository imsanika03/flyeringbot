
# Core Bluetooth module
import cb

# iOS UI module
import ui

# Time
import time


# Delegate handles all BLE events
class MyCentralManagerDelegate(object):
    def __init__(self):
        self.peripheral = None
        self.characteristic = None
        self.button = None

        # UI view
        self.view = ui.View()
        self.view.name = 'BLE Toggle'
        self.view.background_color = '#dddddd'
        print(self)
        print(self.view)

        # Our Toggle button
        self.button = ui.Button(title='**** LOADING ****')
        self.button.name = "button"
        self.button.border_width = 1
        self.button.bg_color = '#DDDDDD'
        self.button.font_color = 'black'
        self.button.enabled = False

        # Center the button in the view
        self.button.center = (self.view.width * 0.5, self.view.height * 0.5)

        # Flexible left, right, top and bottom margins are flexible
        self.button.flex = 'LRTB'

        # When clicked call this function
        # Tells the function the sender so
        # can use same for multiple buttons
        self.button.action = self.button_click

        # Add the button to the view
        self.view.add_subview(self.button)
        self.button = self.view['button']

        # Show the view
        # On the iPad could be Sheet, Popover or Fullscreen
        # iPhone only has fullscreen so ignores the parameter
        self.view.present('sheet')

    # If the button is pressed do this
    def button_click(self, sender):
        sender.title = 'Sending'
        self.send_string("*")
        time.sleep(0.10)
        sender.title = 'Toggle LED'

    # Device discovered
    def did_discover_peripheral(self, p):
        if p.name == 'HC-08' and not self.peripheral:
            print('Discovered ' + p.name)
            self.peripheral = p
            cb.connect_peripheral(self.peripheral)

    # Connected
    def did_connect_peripheral(self, p):
        print('Connected Peripheral ' + p.name)
        print('Looking for Service FFE0')
        p.discover_services()

    # Services discovered
    def did_discover_services(self, p, error):
        for s in p.services:
            if s.uuid == 'FFE0':
                print('Found Service ' + s.uuid)
                print('Looking for Characteristic FFE1')
                p.discover_characteristics(s)

    # Characteristics discovered
    def did_discover_characteristics(self, s, error):
        for c in s.characteristics:
            if c.uuid == 'FFE1':
                print('Found Characteristic ' + c.uuid)
                self.characteristic = c
                print(self.button)
                self.button.enabled = True
                self.button.title = "Toggle LED"
                self.send_string("*")
                time.sleep(0.10)
                self.send_string("*")
                time.sleep(0.10)
                self.send_string("*")

    # Send strings
    def send_string(self, string_to_send):
        self.peripheral.write_characteristic_value(self.characteristic, string_to_send, False)


# Initialize
cb.set_central_delegate(MyCentralManagerDelegate())
cb.scan_for_peripherals()