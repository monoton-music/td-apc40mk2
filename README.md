# td-apc40mk2

A Python module for integrating the **Akai APC40 MK2** MIDI controller with **TouchDesigner**. Control the LED lights, knobs, and more with intuitive Python commands.

このモジュールについて扱った記事があります：[TouchDesignerでAPC40 MK2のLEDを操る (Japanese)](https://qiita.com/monoton/private/137cb287ac836535a81b)

## Environment

This module was developed and tested using

- TouchDesigner 2023.11600 Commercial
- Akai APC40 MK2
- MacBook Pro (M2 Pro, macOS Ventura 13.6.3)

## Installation

1. Drag and drop `/src/apc40mk2.py` into your Network Editor (it will appear as a Text DAT).
2. Import the module in your Python script and designate a **MIDI Out CHOP** to send MIDI messages to the APC40 MK2.

## Example Project

An example project is included in the `/example/example.toe` file. Open it in TouchDesigner to see the module in action.

## Quick Start

Here's an example of how to get started:

1. Place the `apc40mk2.py` file in your project and add a **MIDI Out CHOP** to your network.  
   - **Note**: Keep the default settings of the MIDI Out CHOP unchanged.

2. Ensure the APC40 MK2 is connected to your computer and recognized by the **MIDI Device Mapper**.  
   - Set the **APC40 MK2's ID** in the MIDI Out CHOP.

3. Initialize the module with the following Python code:

```python
import apc40mk2

# Initialize APC40 MK2 with the MIDI Out CHOP
apc = apc40mk2.APC40MK2(op('midiout1'))

# Set the top-left Clip Launch button to red
apc.led.set_clip_launch(row=1, column=1, color="red", led_type=0)
```

## Key Functionalities

For a full list of functions and their parameters, refer to the DocStrings in the `apc40mk2.py` file.

### 1. Device Mode Management

- Switch between Generic, Ableton Live, or Alternate Ableton Live modes.
- Alternate Ableton Live Mode is required for full LED customization and advanced MIDI control.

Example:

```python
# Set the device to Alternate Ableton Live Mode
apc.mode.set_device_mode(mode=2)
```

### 2. **Control LED Colors**

- Set Clip Launch, Scene Launch, or other button LEDs to any color and LED type.

Example:

```python
# Set the second column, first row Clip Launch LED to cyan
apc.led.set_clip_launch(row=1, column=2, color="cyan", led_type=0)
```

### 3. Knob Control

- Adjust knob values or set LED ring styles for device controls.

Example:

```python
# Set the value of the first track knob
apc.knob.set_track_knob_value(index=1, value=64)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

### monoton

A technical artist focused on music production, VJing, and hardware-driven spatial design.

Creates music, develops TouchDesigner-based VJ systems, and works on live events and exhibitions in both real and virtual spaces.

---

[LinkTree](https://linktr.ee/monoton)

[Instagram](https://www.instagram.com/monoton.music/)

[Twitter (X)](https://twitter.com/monoton_music/)
