class LEDController:
    """Class to manage all LED functionalities of APC40MK2."""

    def __init__(self, midiout):
        self.midiout = midiout
        self.color_map = {
            "black": 0, "dark gray": 1, "gray": 2, "white": 3, "red": 5, 
            "orange": 9, "yellow": 13, "green": 21, "cyan": 37, "blue": 45, 
            "purple": 49, "magenta": 53, "pink": 57
        }
        self.color_codes = [
            (0, "#000000"), (1, "#1E1E1E"), (2, "#7F7F7F"), (3, "#FFFFFF"),
            (4, "#FF4C4C"), (5, "#FF0000"), (6, "#590000"), (7, "#190000"),
            (8, "#FFBD6C"), (9, "#FF5400"), (10, "#591D00"), (11, "#271B00"),
            (12, "#FFFF4C"), (13, "#FFFF00"), (14, "#595900"), (15, "#191900"),
            (16, "#88FF4C"), (17, "#54FF00"), (18, "#1D5900"), (19, "#142B00"),
            (20, "#4CFF4C"), (21, "#00FF00"), (22, "#005900"), (23, "#001900"),
            (24, "#4CFF5E"), (25, "#00FF19"), (26, "#00590D"), (27, "#001902"),
            (28, "#4CFF88"), (29, "#00FF55"), (30, "#00591D"), (31, "#001F12"),
            (32, "#4CFFB7"), (33, "#00FF99"), (34, "#005935"), (35, "#001912"),
            (36, "#4CC3FF"), (37, "#00A9FF"), (38, "#004152"), (39, "#001019"),
            (40, "#4C88FF"), (41, "#0055FF"), (42, "#001D59"), (43, "#000819"),
            (44, "#4C4CFF"), (45, "#0000FF"), (46, "#000059"), (47, "#000019"),
            (48, "#874CFF"), (49, "#5400FF"), (50, "#190064"), (51, "#0F0030"),
            (52, "#FF4CFF"), (53, "#FF00FF"), (54, "#590059"), (55, "#190019"),
            (56, "#FF4C87"), (57, "#FF0054"), (58, "#59001D"), (59, "#220013"),
            (60, "#FF1500"), (61, "#993500"), (62, "#795100"), (63, "#436400"),
            (64, "#033900"), (65, "#005735"), (66, "#00547F"), (67, "#0000FF"),
            (68, "#00454F"), (69, "#2500CC"), (70, "#7F7F7F"), (71, "#202020"),
            (72, "#FF0000"), (73, "#BDFF2D"), (74, "#AFED06"), (75, "#64FF09"),
            (76, "#108B00"), (77, "#00FF87"), (78, "#00A9FF"), (79, "#002AFF"),
            (80, "#3F00FF"), (81, "#7A00FF"), (82, "#B21A7D"), (83, "#402100"),
            (84, "#FF4A00"), (85, "#88E106"), (86, "#72FF15"), (87, "#00FF00"),
            (88, "#3BFF26"), (89, "#59FF71"), (90, "#38FFCC"), (91, "#5B8AFF"),
            (92, "#3151C6"), (93, "#877FE9"), (94, "#D31DFF"), (95, "#FF005D"),
            (96, "#FF7F00"), (97, "#B9B000"), (98, "#90FF00"), (99, "#835D07"),
            (100, "#392b00"), (101, "#144C10"), (102, "#0D5038"), (103, "#15152A"),
            (104, "#16205A"), (105, "#693C1C"), (106, "#A8000A"), (107, "#DE513D"),
            (108, "#D86A1C"), (109, "#FFE126"), (110, "#9EE12F"), (111, "#67B50F"),
            (112, "#1E1E30"), (113, "#DCFF6B"), (114, "#80FFBD"), (115, "#9A99FF"),
            (116, "#8E66FF"), (117, "#404040"), (118, "#757575"), (119, "#E0FFFF"),
            (120, "#A00000"), (121, "#350000"), (122, "#1AD000"), (123, "#074200"),
            (124, "#B9B000"), (125, "#3F3100"), (126, "#B35F00"), (127, "#4B1502")
        ]
    
    def _find_closest_color(self, hex_color):
        """
        Find the closest color value to the given hex color.

        Args:
            hex_color (str): The hex color code (e.g., "#FF0000").

        Returns:
            int: The index of the closest color (0-127).
        """
        def hex_to_rgb(hex_code):
            hex_code = hex_code.lstrip("#")
            return [int(hex_code[i:i+2], 16) for i in (0, 2, 4)]
        
        target_rgb = hex_to_rgb(hex_color)
        closest_index = None
        closest_distance = float("inf")

        for index, code in self.color_codes:
            current_rgb = hex_to_rgb(code)
            distance = sum((t - c) ** 2 for t, c in zip(target_rgb, current_rgb))
            if distance < closest_distance:
                closest_distance = distance
                closest_index = index
        
        return closest_index

    def set_clip_launch_led(self, row, column, color, led_type):
        """
        Set the color of a clip launch button.

        Args:
            row (int): The row index of the clip launch button (1-5).
            column (int): The column index of the clip launch button (1-8).
            color (str|int): The color name, hex code, or index (0-127).
                - Color names available: black, dark gray, gray, white, red, orange,
                  yellow, green, cyan, blue, purple, magenta, pink.
                - Hex codes: Any valid hexadecimal color code (e.g., "#FF0000").
                - Index: Integer values between 0-127.
            led_type (int): LED Type (0-15).
                - 0: Primary Color
                - 1: Secondary Color (Oneshot 1/24)
                - 2: Secondary Color (Oneshot 1/16)
                - 3: Secondary Color (Oneshot 1/8)
                - 4: Secondary Color (Oneshot 1/4)
                - 5: Secondary Color (Oneshot 1/2)
                - 6: Secondary Color (Pulsing 1/24)
                - 7: Secondary Color (Pulsing 1/16)
                - 8: Secondary Color (Pulsing 1/8)
                - 9: Secondary Color (Pulsing 1/4)
                - 10: Secondary Color (Pulsing 1/2)
                - 11: Secondary Color (Blinking 1/24)
                - 12: Secondary Color (Blinking 1/16)
                - 13: Secondary Color (Blinking 1/8)
                - 14: Secondary Color (Blinking 1/4)
                - 15: Secondary Color (Blinking 1/2)

        Returns:
            None

        Raises:
            ValueError: If the channel, row, column, or color values are out of their valid ranges.
        """
        if led_type not in range(16):
            raise ValueError(f"Invalid channel: {led_type}. Must be 0-15.")
        if row not in range(1, 6):
            raise ValueError(f"Invalid row: {row}. Must be 1-5.")
        if column not in range(1, 9):
            raise ValueError(f"Invalid column: {column}. Must be 1-8.")
        
        if isinstance(color, str):
            if color.startswith("#"):
                color = self._find_closest_color(color)
            else:
                color = self.color_map.get(color.lower())
                if color is None:
                    raise ValueError(
                        f"Unknown color name: {color}. Use a valid name like 'red' or a hex code like '#FF0000'."
                    )
        if not isinstance(color, int) or color not in range(128):
            raise ValueError(
                f"Invalid color: {color}. Must be an index (0-127), a hex code, or a valid color name."
            )

        self.midiout.sendNoteOn(led_type + 1, (5 - row) * 8 + column, color / 127)
    
    def set_record_arm_led(self, track, state):
        """
        Set the state of the record arm LED.

        Args:
            track (int): The track index (1-8).
            state (bool): The state of the record arm LED.
                - True: On
                - False: Off

        Returns:
            None

        Raises:
            ValueError: If the track index is not in the range 1-8.
        """
        if track not in range(1, 9):
            raise ValueError(f"Invalid track: {track}. Must be 1-8.")
        
        self.midiout.sendNoteOn(track, 0x30 + 1, 1 if state else 0)

    def set_solo_led(self, track, state):
        """
        Set the state of the solo LED.

        Args:
            track (int): The track index (1-8).
            state (bool): The state of the solo LED.
                - True: On
                - False: Off

        Returns:
            None

        Raises:
            ValueError: If the track index is not in the range 1-8.
        """
        if track not in range(1, 9):
            raise ValueError(f"Invalid track: {track}. Must be 1-8.")
        
        self.midiout.sendNoteOn(track, 0x31 + 1, 1 if state else 0)
    
    def set_activator_led(self, track, state):
        """
        Set the state of the activator LED.

        Args:
            track (int): The track index (1-8).
            state (bool): The state of the activator LED.
                - True: On
                - False: Off

        Returns:
            None

        Raises:
            ValueError: If the track index is not in the range 1-8.
        """
        if track not in range(1, 9):
            raise ValueError(f"Invalid track: {track}. Must be 1-8.")
        
        self.midiout.sendNoteOn(track, 0x32 + 1, 1 if state else 0)
    
    def set_track_select_led(self, track, state):
        """
        Set the state of the track select LED.

        Args:
            track (int): The track index (1-8).
            state (bool): The state of the track select LED.
                - True: On
                - False: Off

        Returns:
            None

        Raises:
            ValueError: If the track index is not in the range 1-8.
        """
        if track not in range(1, 9):
            raise ValueError(f"Invalid track: {track}. Must be 1-8.")
        
        self.midiout.sendNoteOn(track, 0x33 + 1, 1 if state else 0)
    
    def set_clip_stop_led(self, track, state):
        """
        Set the state of the track stop LED.

        Args:
            track (int): The track index (1-8).
            state (int): The state of the track stop LED.
                - 0: Off
                - 1: On
                - 2: Blink (sync to tempo at 1/8 rate)

        Returns:
            None

        Raises:
            ValueError: If the track index is not in the range 1-8.
            ValueError: If the state is not in the range 0-2.
        """
        if track not in range(1, 9):
            raise ValueError(f"Invalid track: {track}. Must be 1-8.")
        
        if state not in range(3):
            raise ValueError(f"Invalid state: {state}. Must be 0-2.")

        self.midiout.sendNoteOn(track, 0x34 + 1, state / 127)
    
    def set_device_ctrl_button_led(self, index, state):
        """
        Set the state of the device control button LED.

        Args:
            index (int): The index of the device control button (1-8).
            state (bool): The state of the device control button LED.
                - True: On
                - False: Off

        Returns:
            None

        Raises:
            ValueError: If the index is not in the range 1-8.
        """
        if index not in range(1, 9):
            raise ValueError(f"Invalid index: {index}. Must be 1-8.")
        
        self.midiout.sendNoteOn(1, 0x3A + index, 1 if state else 0)
        
    def set_crossfader_assign_led(self, track, state):
        """
        Set the state of the crossfader assign LED.
        
        Args:
            track (int): The track index (1-8).
            state (int): The state of the crossfader assign LED (0-2).
                - 0: Off
                - 1: A
                - 2: B
        
        Returns:
            None
        
        Raises:
            ValueError: If the track index is not in the range 1-8.
            ValueError: If the state is not in the range 0-2.
        """
        if track not in range(1, 9):
            raise ValueError(f"Invalid track: {track}. Must be 1-8.")
        if state not in range(3):
            raise ValueError(f"Invalid state: {state}. Must be 0-2.")

        self.midiout.sendNoteOn(track, 0x42 + 1, state / 127)
    
    def set_master_track_led(self, state):
        """
        Set the state of the master track LED.

        Args:
            state (bool): The state of the master track LED.
                - True: On
                - False: Off

        Returns:
            None
        """
        self.midiout.sendNoteOn(1, 0x50 + 1, 1 if state else 0)
    
    def set_scene_launch_led(self, scene, color, led_type):
        """
        Set the LED of a track scene launch button.
        
        Args:
            scene (int): Scene index (1-5).
            color (str|int): The color name, hex code, or index (0-127).
                - Color names available: black, dark gray, gray, white, red, orange,
                  yellow, green, cyan, blue, purple, magenta, pink.
                - Hex codes: Any valid hexadecimal color code (e.g., "#FF0000").
                - Index: Integer values between 0-127.
            led_type (int): LED Type (0-15).
                - 0: Primary Color
                - 1: Secondary Color (Oneshot 1/24)
                - 2: Secondary Color (Oneshot 1/16)
                - 3: Secondary Color (Oneshot 1/8)
                - 4: Secondary Color (Oneshot 1/4)
                - 5: Secondary Color (Oneshot 1/2)
                - 6: Secondary Color (Pulsing 1/24)
                - 7: Secondary Color (Pulsing 1/16)
                - 8: Secondary Color (Pulsing 1/8)
                - 9: Secondary Color (Pulsing 1/4)
                - 10: Secondary Color (Pulsing 1/2)
                - 11: Secondary Color (Blinking 1/24)
                - 12: Secondary Color (Blinking 1/16)
                - 13: Secondary Color (Blinking 1/8)
                - 14: Secondary Color (Blinking 1/4)
                - 15: Secondary Color (Blinking 1/2)
                
        Returns:
            None
        
        Raises:
            ValueError: If the scene or color values are out of their valid ranges.
        """
        if led_type not in range(16):
            raise ValueError(f"Invalid channel: {led_type}. Must be 0-15.")
        if scene not in range(1, 6):
            raise ValueError(f"Invalid scene: {scene}. Must be 1-5.")
        
        if isinstance(color, str):
            if color.startswith("#"):
                color = self._find_closest_color(color)
            else:
                color = self.color_map.get(color.lower())
                if color is None:
                    raise ValueError(
                        f"Unknown color name: {color}. Use a valid name like 'red' or a hex code like '#FF0000'."
                    )
        if not isinstance(color, int) or color not in range(128):
            raise ValueError(
                f"Invalid color: {color}. Must be an index (0-127), a hex code, or a valid color name."
            )

        self.midiout.sendNoteOn(led_type + 1, 0x52 + scene, color / 127)

    def set_pan_button_led(self, state):
        """
        Set the state of the pan button LED.

        Args:
            state (bool): The state of the pan button LED.
                - True: On
                - False: Off

        Returns:
            None
        """
        self.midiout.sendNoteOn(1, 0x57 + 1, 1 if state else 0)

    def set_sends_button_led(self, state):
        """
        Set the state of the sends button LED.

        Args:
            state (bool): The state of the sends button LED.
                - True: On
                - False: Off

        Returns:
            None
        """
        self.midiout.sendNoteOn(1, 0x58 + 1, 1 if state else 0)
    
    def set_user_button_led(self, state):
        """
        Set the state of the user button LED.

        Args:
            state (bool): The state of the user button LED.
                - True: On
                - False: Off

        Returns:
            None
        """
        self.midiout.sendNoteOn(1, 0x59 + 1, 1 if state else 0)
    
    def set_metronome_button_led(self, state):
        """
        Set the state of the metronome button LED.

        Args:
            state (bool): The state of the metronome button LED.
                - True: On
                - False: Off

        Returns:
            None
        """
        self.midiout.sendNoteOn(1, 0x5A + 1, 1 if state else 0)
    
    def set_play_button_led(self, state):
        """
        Set the state of the play button LED.

        Args:
            state (bool): The state of the play button LED.
                - True: On
                - False: Off

        Returns:
            None
        """
        self.midiout.sendNoteOn(1, 0x5B + 1, 1 if state else 0)
    
    def set_record_button_led(self, state):
        """
        Set the state of the record button LED.

        Args:
            state (bool): The state of the record button LED.
                - True: On
                - False: Off

        Returns:
            None
        """
        self.midiout.sendNoteOn(1, 0x5D + 1, 1 if state else 0)
    
    def set_session_button_led(self, state):
        """
        Set the state of the session button LED.
        
        Args:
            state (bool): The state of the session button LED.
                - True: On
                - False: Off

        Returns:
            None
        """
        self.midiout.sendNoteOn(1, 0x66 + 1, 1 if state else 0)
        
    def set_bank_button_led(self, state):
        """
        Set the state of the bank button LED.
        
        Args:
            state (bool): The state of the bank button LED.
                - True: On
                - False: Off

        Returns:
            None
        """
        self.midiout.sendNoteOn(1, 0x67 + 1, 1 if state else 0)
        
class KnobController:
    """Class to manage all knob functionalities of APC40MK2."""
    
    def __init__(self, midiout):
        self.midiout = midiout
    
    def set_track_knob_type(self, index, type):
        """
        Set the type of the track knob.

        Args:
            index (int): The index of the track knob (1-8).
            type (int): The type of the track knob.
                - 0: Off
                - 1: Single
                - 2: Volume style
                - 3: Pan style
                - 4-127: Custom values (treated as Single)

        Returns:
            None

        Raises:
            ValueError: If the index is not in the range 1-8 or type is not in the range 0-127.
        """
        
        if index not in range(1, 9):
            raise ValueError(f"Invalid index: {index}. The index must be in the range 1-8.")
        
        if type not in range(128):
            raise ValueError(f"Invalid type: {type}. The type must be in the range 0-127.")
        
        self.midiout.send(0xB0, 0x38 + index - 1, type)
        
    def set_track_knob_value(self, index, value):
        """
        Set the value of a track knob.

        Args:
            index (int): The index of the track knob (1-8).
            value (int): The value of the track knob (0-127).

        Returns:
            None

        Raises:
            ValueError: If the index is not in the range 1-8 or value is not in the range 0-127.
        """
        if index not in range(1, 9):
            raise ValueError(f"Invalid index: {index}. The index must be in the range 1-8.")
        
        if value not in range(128):
            raise ValueError(f"Invalid value: {value}. The value must be in the range 0-127.")
        
        self.midiout.send(0xB0, 0x30 + index - 1, value)

    def set_device_ctrl_knob_type(self, channel, index, knob_type):
        """
        Configure the LED ring type for a device knob.

        Args:
            channel (int): MIDI channel (1-9).
                - 1-8: Tracks 1-8
                - 9: Master
                - Note: Set to 1 for modes 1 (Ableton Live Mode) and 2 (Alternate Ableton Live Mode).
            index (int): Knob index (1-8).
            knob_type (int): LED ring style.
                - 0: Off
                - 1: Single
                - 2: Volume Style
                - 3: Pan Style

        Returns:
            None

        Raises:
            ValueError: If the channel is not in the range 1-9, index is not in the range 1-8, or knob_type is not in the range 0-127.
        """
        if channel not in range(1, 10):
            raise ValueError(f"Invalid channel: {channel}. The channel must be in the range 1-9.")
        
        if index not in range(1, 9):
            raise ValueError(f"Invalid index: {index}. The index must be in the range 1-8.")
        
        if knob_type not in range(4):
            raise ValueError(f"Invalid knob_type: {knob_type}. The knob_type must be in the range 0-3.")
        
        self.midiout.send(0xB0 + channel - 1, 0x18 + index - 1, knob_type)
    
    def set_device_ctrl_knob_value(self, channel, index, value):
        """
        Set the value of a device knob.

        Args:
            channel (int): MIDI channel (1-9).
                - 1-8: Tracks 1-8
                - 9: Master
                - Note: Set to 1 for modes 1 (Ableton Live Mode) and 2 (Alternate Ableton Live Mode).
            index (int): Knob index (1-8).
            value (int): The value of the device knob (0-127).
            
        Returns:
            None
        
        Raises:
            ValueError: If the channel is not in the range 1-9, index is not in the range 1-8, or value is not in the range 0-127.
        """
        if channel not in range(1, 10):
            raise ValueError(f"Invalid channel: {channel}. The channel must be in the range 1-9.")
        
        if index not in range(1, 9):
            raise ValueError(f"Invalid index: {index}. The index must be in the range 1-8.")
        
        if value not in range(128):
            raise ValueError(f"Invalid value: {value}. The value must be in the range 0-127.")
        
        self.midiout.send(0xB0 + channel - 1, 0x10 + index - 1, value)

class DeviceModeController:
    """Handles device mode settings for APC40MK2."""
    
    def __init__(self, midiout):
        self.midiout = midiout
    
    def set_device_mode(self, mode):
        """
        Set the device mode.

        Args:
            mode (int): The device mode.
                - 0: Generic Mode
                - 1: Ableton Live Mode
                - 2: Alternate Ableton Live Mode

        Returns:
            None

        Raises:
            ValueError: If the mode is not 0, 1, or 2.
        """
        if mode not in [0, 1, 2]:
            raise ValueError(f"Invalid mode: {mode}. Valid modes are 0 (Generic Mode), 1 (Ableton Live Mode), and 2 (Alternate Ableton Live Mode).")
        
        self.midiout.sendExclusive(0x47, 0x7F, 0x29, 0x60, 0x00, 0x04, 0x40 + mode, 0x01, 0x00, 0x00)

class APC40MK2:
    """Main class to manage all functionalities of APC40MK2."""

    def __init__(self, midiout):
        self.midiout = midiout
        self.led = LEDController(midiout)
        self.knob = KnobController(midiout)
        self.mode = DeviceModeController(midiout)
    