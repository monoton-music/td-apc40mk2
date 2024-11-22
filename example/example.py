import apc40mk2

apc = apc40mk2.APC40MK2(op('midiout1'))
apc.mode.set_device_mode(2)

for i in range(1, 9):
    apc.knob.set_track_knob_type(i, 1)
    apc.knob.set_track_knob_value(i, 64)
    apc.knob.set_device_knob_type(1, i, 1)
    apc.knob.set_device_knob_value(1, i, 64)

for i in range(1, 6):
    for j in range(1, 9):
        if j % 2 == 0:
            apc.led.set_clip_launch_led(0, i, j, "red")
        else:
            apc.led.set_clip_launch_led(0, i, j, "blue")

for i in range(1, 9):
    apc.led.set_record_arm_led(i, True)
    apc.led.set_solo_led(i, True)
    apc.led.set_activator_led(i, True)
    apc.led.set_track_select_led(i, True)
    apc.led.set_clip_stop_led(i, 2)