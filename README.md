# esp-onair
Small microcontroller setup to control On Air light when webcam is live with a Windows compatible python webcam status check.

## Components

`esp-onair.ino` - ArduioIDE project base for microcontroller app.

Presumes that a physical pushbutton is wired to D7. When pulled low, cycles the current state of the lights. To control lights, pulls D6 to low, simulating a button press.

On startup listens on poll for UDP multicast signal to group `239.0.82.66`. On receiving, parses the message body looking for a json `{signal: 2}` with value indicating off (`0`) on (`1`) or toggle (`2`) and updates the light state to match.

`server\cycle.py` - Command script to toggle light state for esp lights on the current network

`server\onair.py` - Service script, runs in background and checks Windows Registry for active Webcam and sets lights to on/off when status changes

## Usage

Make a copy of `secrets.template.h` to `secrets.h` and add your network login details.
