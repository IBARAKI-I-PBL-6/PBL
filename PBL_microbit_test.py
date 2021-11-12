def on_button_pressed_a():
    basic.show_icon(IconNames.HAPPY)
    serial.write_line("microbit")
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_forever():
    if serial.read_line() == "raspberry":
        basic.show_icon(IconNames.HEART)
basic.forever(on_forever)