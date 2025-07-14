from RPLCD.i2c import CharLCD
import logging
screenAddress=0x27 # If piggy-back board is PCF8574AT chip, 0x3F; if PCF8574T, 0x27

class Display:
    def __init__(self):
        self.lcd = CharLCD(i2c_expander='PCF8574', address=screenAddress, port=1,
                    cols=16, rows=2, #adjust according to what ur lcd screen supports
                    backlight_enabled=True) #changing this parameter will only work if the jumper for the backlight on the LCD is also on
        self.lcd.clear()
        self.loadChar()
        self.lcd.cursor_pos = (0, 0)          # Row 1, column 1
        self.lcd.write_string('\x00\x01')    # Top row of the face
        self.lcd.cursor_pos = (1, 0)          # Row 2, column 2
        self.lcd.write_string('\x02\x03')    # Bottom row of the face

    def display_stats(self, hunger, sleep, joy):
        # Row 0: Hunger 'h: x'
        self.lcd.cursor_pos = (1, 5)
        self.lcd.write_string(f"h:{round(hunger)} s:{round(sleep)} j:{round(joy)}")

    def screenChange(self, state):
        # clears emoticon and 'state' message but not character
        self.lcd.cursor_pos = (0, 5)
        self.lcd.write_string(" " * 11)

        self.mode = state

        if state == "starting":
            self.screenMessage("hey!!", "tim")
        elif state == "joy":
            self.screenMessage("(^‿^)", "joy")
        elif state == "angry":
            self.screenMessage("(>_<)", "mad")
        elif state == "sleep":
            self.screenMessage("(-.-)", "Zzz")
        elif state == "dead":
            self.screenMessage("(x_x)", "dead")
        elif state == "neutral":
            self.screenMessage("(・_・)", "meh")
        else:
            logging.error("error in screenChange method")

    def screenMessage(self, emoticon, state):
        if state=="dead":
            self.lcd.clear()
            stateStartCol = 10
            self.lcd.cursor_pos = (0, stateStartCol)
            self.lcd.write_string(state)
            faceStartCol = 4
            self.lcd.cursor_pos = (0, faceStartCol)
            self.lcd.write_string(emoticon)
            self.lcd.cursor_pos(1,0)
            self.lcd.write_string("holdred2restart")
        else:
            faceStartCol = 4
            self.lcd.cursor_pos = (0, faceStartCol)
            self.lcd.write_string(emoticon)

            # Centers the state of the pet text (row 3)
            stateStartCol = 10
            self.lcd.cursor_pos = (0, stateStartCol)
            self.lcd.write_string(state)

    def loadChar(self):
        # Top left of pet
        char_0 = [
            0b11111, 0b11011, 0b10101, 0b10101,
            0b10110, 0b10111, 0b10111, 0b11101
        ]

        # Top right of pet
        char_1 = [
            0b11111, 0b11011, 0b10101, 0b10101,
            0b01101, 0b11101, 0b11101, 0b10111
        ]

        # Bottom left of pet
        char_2 = [
            0b10110, 0b11100, 0b11100, 0b10110,
            0b11011,0b11011, 0b11100, 0b11111
        ]

        # Bottom right of pet
        char_3 = [
            0b11101, 0b10111, 0b10111, 0b01101,
            0b11011, 0b11011, 0b00111, 0b11111
        ]

        self.lcd.create_char(0, char_0)
        self.lcd.create_char(1, char_1)
        self.lcd.create_char(2, char_2)
        self.lcd.create_char(3, char_3)