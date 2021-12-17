def on_data_received():
    global isEnd
    isEnd = 0
serial.on_data_received("start", on_data_received)

def on_data_received2():
    basic.show_leds("""
        # # # # #
                # # # # #
                # # # # #
                # # # # #
                # # # # #
    """)
serial.on_data_received("warning", on_data_received2)

def on_data_received3():
    basic.clear_screen()
serial.on_data_received("stop", on_data_received3)

isEnd = 0
pins.set_pull(DigitalPin.P0, PinPullMode.PULL_DOWN)
pins.set_pull(DigitalPin.P1, PinPullMode.PULL_DOWN)
isEnd = 0
start_time = input.running_time()
serial.redirect(SerialPin.USB_TX, SerialPin.USB_RX, BaudRate.BAUD_RATE115200)

def on_forever():
    global isEnd
    if isEnd == 1:
        pass
    elif input.running_time() - start_time >= 20000:
        isEnd = 1
        serial.write_line("end")
basic.forever(on_forever)

def on_forever2():
    if isEnd == 1:
        pass
    elif pins.digital_read_pin(DigitalPin.P0) == 1:
        serial.write_line("in")
        pins.set_pull(DigitalPin.P0, PinPullMode.PULL_DOWN)
basic.forever(on_forever2)

def on_forever3():
    if isEnd == 1:
        pass
    elif pins.digital_read_pin(DigitalPin.P1) == 1:
        serial.write_line("out")
        pins.set_pull(DigitalPin.P1, PinPullMode.PULL_DOWN)
basic.forever(on_forever3)
