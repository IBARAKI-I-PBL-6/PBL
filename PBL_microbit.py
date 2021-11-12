system_start_time = input.running_time()
pins.set_pull(DigitalPin.P0, PinPullMode.PULL_DOWN)
pins.set_pull(DigitalPin.P1, PinPullMode.PULL_DOWN)
start_time = 0

def on_forever():
    global start_time
    while input.running_time() - system_start_time <= 60000:
        if pins.digital_read_pin(DigitalPin.P0) == 1:
            start_time = input.running_time()
            while input.running_time() - start_time <= 5000:
                if pins.digital_read_pin(DigitalPin.P1) == 1:
                    basic.show_number(1)
                    serial.write_number(1)
                    break
            basic.clear_screen()
            pins.set_pull(DigitalPin.P0, PinPullMode.PULL_DOWN)
            pins.set_pull(DigitalPin.P1, PinPullMode.PULL_DOWN)
        elif pins.digital_read_pin(DigitalPin.P1) == 1:
            start_time = input.running_time()
            while input.running_time() - start_time <= 5000:
                if pins.digital_read_pin(DigitalPin.P0) == 1:
                    basic.show_number(2)
                    serial.write_number(2)
                    break
            basic.clear_screen()
            pins.set_pull(DigitalPin.P0, PinPullMode.PULL_DOWN)
            pins.set_pull(DigitalPin.P1, PinPullMode.PULL_DOWN)
basic.forever(on_forever)

def on_in_background():
    if serial.read_line() == "warning":
        basic.show_leds("""
            # . . . #
                        . # . # .
                        . . # . .
                        . # . # .
                        # . . . #
        """)
control.in_background(on_in_background)
