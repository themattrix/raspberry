#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep


class GPIOContext(object):

    def __enter__(self):
        # turn off annoying warnings
        GPIO.setwarnings(False)

        # to use Raspberry Pi board pin numbers
        GPIO.setmode(GPIO.BOARD)

    def __exit__(self, type, value, traceback):
        # change (back?) to BCM GPIO numbering
        GPIO.setmode(GPIO.BCM)

        # reset every channel that has been set up by this program to INPUT
        # with no pullup/pulldown and no event detection.
        GPIO.cleanup()


def runway_lights(lights, orderer=lambda x: x, times=2, interval=0.05):
    for j in xrange(0, times):
        for toggle in (GPIO.HIGH, GPIO.LOW):
            for light in orderer(lights):
                GPIO.output(light, toggle)
                sleep(interval)


def blink_lights(lights, times=5, interval=0.25):
    for i in xrange(0, times):
        for toggle in (GPIO.LOW, GPIO.HIGH):
            for light in lights:
                GPIO.output(light, toggle)
                sleep(interval)


class TugOfWar(object):

    def __init__(self):
        # http://www.hobbytronics.co.uk/image/data/tutorial/raspberry-pi/gpio-pinout.jpg
        self.lights = (7, 11, 12, 13, 15)

        self.p1_button = 16
        self.p2_button = 18

        # Enable reading the state of the two player buttons
        GPIO.setup(self.p1_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.p2_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        for color in self.lights:
            # Enable output on this light
            GPIO.setup(color, GPIO.OUT)

            # Turn off this light
            GPIO.output(color, GPIO.LOW)

        # Enable middle light
        GPIO.output(self.lights[len(self.lights) / 2], GPIO.HIGH)

        # Number of clicks to advance to next light
        self.scaler = 4

    def play(self):
        print("Ready...TUG")
        winner = self._run()
        print("Player {0} wins!".format(winner))
        self._celebrate(winner)
        print("<press both buttons to start new game>")
        self._wait()

    def _wait(self):
        while True:
            if not GPIO.input(self.p1_button) and not GPIO.input(self.p2_button):
                return
            sleep(0.1)

    def _run(self):
        prev_balance = 0
        balance = 0

        p1_down = False
        p2_down = False

        while True:
            if not GPIO.input(self.p1_button):
                if not p1_down:
                    balance -= 1
                    p1_down = True
            else:
                p1_down = False

            if not GPIO.input(self.p2_button):
                if not p2_down:
                    balance += 1
                    p2_down = True
            else:
                p2_down = False

            if balance != prev_balance:

                lit = (balance + (self.scaler / 2)) / self.scaler + len(self.lights) / 2

                if lit < 0:
                    # Player 1 won!
                    return 1
                elif lit >= len(self.lights):
                    # Player 2 won!
                    return 2

                for i in xrange(0, len(self.lights)):
                    if i == lit:
                        GPIO.output(self.lights[i], GPIO.HIGH)
                    else:
                        GPIO.output(self.lights[i], GPIO.LOW)

                prev_balance = balance

    def _celebrate(self, winner):
        if winner == 1:
            runway_lights(self.lights, orderer=reversed)
            blink_lights((self.lights[0],))
        else: # winner == 2
            runway_lights(self.lights)
            blink_lights((self.lights[-1],))


def main():
    try:
        while True:
            with GPIOContext():
                TugOfWar().play()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
