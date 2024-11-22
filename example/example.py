import apc40mk2

apc = apc40mk2.APC40MK2(op('midiout1'))
apc.mode.set_device_mode(2)

for i in range(1, 9):
    apc.knob.set_track_knob_type(i, 1)
    apc.knob.set_track_knob_value(i, 64)
    apc.knob.set_device_ctrl_knob_type(1, i, 1)
    apc.knob.set_device_ctrl_knob_value(1, i, 30)

for i in range(1, 6):
    for j in range(1, 9):
        if j % 2 == 0:
            apc.led.set_clip_launch_led(i, j, "red", 0)
        else:
            apc.led.set_clip_launch_led(i, j, "blue", 0)

for i in range(1, 9):
    apc.led.set_record_arm_led(i, True)
    apc.led.set_solo_led(i, True)
    apc.led.set_activator_led(i, True)
    apc.led.set_track_select_led(i, True)
    apc.led.set_clip_stop_led(i, 1)
    apc.led.set_device_ctrl_button_led(i, True)
    apc.led.set_crossfader_assign_led(i, 1)

for i in range(1, 6):
    apc.led.set_scene_launch_led(i, "red", 0)

apc.led.set_master_track_led(True)
apc.led.set_pan_button_led(True)
apc.led.set_sends_button_led(True)
apc.led.set_user_button_led(True)
apc.led.set_metronome_button_led(True)
apc.led.set_play_button_led(True)
apc.led.set_record_button_led(True)
apc.led.set_session_button_led(True)
apc.led.set_bank_button_led(True)