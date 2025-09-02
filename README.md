# Raspberry Pi Tamagotchi Project 🐱🎮

**An innovative, hardware-software integrated virtual pet experience designed for the Raspberry Pi 5 Model B — combining real-world sensor data, embedded programming, and custom UI to deliver a uniquely immersive interactive game.**

## Project Overview

This project showcases a sophisticated Tamagotchi-style virtual pet system that transcends traditional software boundaries by leveraging physical sensors and buttons to create a rich, tactile gaming experience. Designed for the Raspberry Pi 5 Model B, it integrates analog and digital inputs — including a photoresistor, capacitive touch sensor, and multiple push buttons — alongside an I2C-connected 16x2 LCD screen displaying a custom-crafted cat character.

By orchestrating seamless communication between hardware components and Python-driven software logic, this project exemplifies embedded systems programming, real-time sensor data processing, and user experience design, culminating in a responsive and engaging digital pet simulation.

## Key Technical Highlights

- **Multi-modal hardware integration:** Utilizes GPIO inputs, I2C communication with ADC (ADS7830) for analog sensors, and a character LCD for output. Demonstrates mastery of low-level hardware interfacing and protocol management.  
- **Event-driven architecture:** Implements responsive button press and hold detection with debouncing via interrupt callbacks, ensuring efficient real-time input handling.  
- **Robust sensor fusion:** Combines ambient light detection via photoresistor with capacitive touch sensing and physical button inputs to dynamically modulate pet behavior and UI feedback.  
- **Custom character design:** Features hand-designed custom characters on a 16x2 LCD using RPLCD to provide expressive visual feedback and enhance user engagement.  
- **Graceful system control:** Includes safe program reboot triggered by sustained button hold, exemplifying thoughtful system lifecycle management.  
- **Modular, maintainable codebase:** Clean separation of concerns across display, input handling, pet logic, and stat tracking modules, facilitating extensibility and unit testing.  

## Comprehensive Hardware Bill of Materials

| Component                      | Quantity | Purpose / Notes                                 |
|-------------------------------|----------|------------------------------------------------|
| Raspberry Pi 5 Model B         | 1        | Core processing platform                        |
| 10k Ohm Resistors              | ≥1       | Voltage divider for photoresistor analog input |
| Push Buttons                  | 3        | User input controls for hunger, sleep, and start/reboot |
| 220 Ohm Resistors              | As needed| Current limiting for LEDs or LCD backlight (optional) |
| Capacitive Touch Sensor        | 1        | Detects petting interactions                    |
| ADC Module (ADS7830)           | 1        | Analog-to-digital conversion for sensors       |
| 16x2 I2C LCD Display (1602I2C)| 1        | Visual output for pet states and stats          |
| Jumper Wires, Breadboard       | As needed| Prototyping and secure connections              |

Power supplied via Pi’s onboard 3.3V and 5V rails ensures streamlined component integration.

## Wiring and Setup

- Utilizes **4 GPIO pins** for buttons and sensor inputs.  
- Employs **I2C communication** bus for both ADC module and LCD screen, showcasing multi-device bus management.

> **Schematic:** Refer to [`docs/wiring_schematic.png`](docs/tamagotchi_pet_schematic.jpg) for detailed circuit diagrams and connection layout. 

---

## Software Dependencies and Environment Setup

### Install the following Python libraries on your Raspberry Pi environment:
- **pip install RPLCD smbus2 RPi.GPIO**
- Note: Raspberry Pi 5 have different GPIO pin configurations than older versions. For alternate GPIO libraries (rpi-lgpio), ensure only one GPIO library is installed to avoid conflicts; codebase import statements remain unchanged for seamless switching.

## Execution Instructions
- Clone or download the full repository onto the Raspberry Pi.
- Confirm that all source files (main.py, display.py, input_handler.py, pet.py, stats.py) reside in the same directory.
- Launch the program with: **python3 main.py**
- Engage with your virtual pet using the dedicated buttons and sensors for a fully interactive experience.

## User Interaction Guide
### Buttons:
- Hunger button: Feed the pet, increasing hunger stat.
- Sleep button: Initiate sleep state (conditioned on ambient light sensor for night detection).
- Start button: Hold for 5 seconds to trigger a safe reboot of the system.
- Capacitive touch sensor: Simulates petting, increasing the pet’s joy stat.
- Photoresistor sensor: Determines day/night cycle affecting pet behavior (e.g., sleep).
- LCD display: Visualizes the pet’s emotional state and real-time hunger, joy, and sleep metrics through custom character animations.

## Future Development Opportunities
- Expand pet behaviors with machine learning-based mood prediction.
- Integrate audio output for enhanced user feedback and interaction.
- Implement wireless remote control interfaces via Bluetooth or Wi-Fi.
- Incorporate data persistence for long-term pet stat tracking and analytics.

## License
- **Distributed under the GNU-GPL 2.**

## Contact and Collaboration
- Questions, feature requests, or contributions are welcome! Please open an issue or submit a pull request.
