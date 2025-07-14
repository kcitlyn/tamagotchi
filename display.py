from RPLCD.i2c import CharLCD
import logging

#check screen address using i2cdetect -y 1
screen_address=0x27 # If piggy-back board is PCF8574AT chip, 0x3F; if PCF8574T, 0x27. 


class Display:
    def __init__(self):
        self.lcd = CharLCD(i2c_expander='PCF8574', address=screen_address, port=1,
                    cols=16, rows=2, #adjust according to what ur lcd screen supports
                    backlight_enabled=True) #changing this parameter will only work if the jumper for the backlight on the LCD is also on
        self.lcd.clear()
        self.load_character()
        self.lcd.cursor_pos = (0, 0)          
        self.lcd.write_string('\x00\x01\x02')    # writes top row of the face
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string('\x03\x04\x05')    # writes bottom row of the face

    def display_stats(self, hunger, sleep, joy):
        # Row 0: Hunger 'h:x s:y j:z'
        self.lcd.cursor_pos = (1, 4)
        self.lcd.write_string(f"h:{round(hunger)} s:{round(sleep)} j:{round(joy)}")

    def screen_change(self, state):
        # clears emoticon and 'state' message but not character
        self.lcd.cursor_pos = (0, 5)
        self.lcd.write_string(" " * 11)

        self.mode = state
        #defines the emoticon and emotion pet is feeling on lcd
        if state == "starting":
            self.screen_message("hey!!", "tim")
        elif state == "joy":
            self.screen_message("(^‿^)", "joy")
        elif state == "angry":
            self.screen_message("(>_<)", "mad")
        elif state == "sleep":
            self.screen_message("(-.-)", "Zzz")
        elif state == "dead":
            self.screen_message("(x_x)", "dead")
        elif state == "neutral":
            self.screen_message("('_')", "meh")
        else:
            logging.error("error in screen_change method")

    def screen_message(self, emoticon, state):
        #actually writes out information on lcd
        if state=="dead":
            self.lcd.clear()
            state_start_column = 10
            self.lcd.cursor_pos = (0, state_start_column)
            self.lcd.write_string(state)
            face_start_column = 4
            self.lcd.cursor_pos = (0, face_start_column)
            self.lcd.write_string(emoticon)
            self.lcd.cursor_pos= (1,0)
            self.lcd.write_string("holdred2restart")
        else:
            face_start_column = 4
            self.lcd.cursor_pos = (0, face_start_column)
            self.lcd.write_string(emoticon)

            # Centers the state of the pet text (row 3)
            state_start_column = 10
            self.lcd.cursor_pos = (0, state_start_column)
            self.lcd.write_string(state)

    def load_character(self):
        # top left of character
        char_0 = [
            0b00000,
            0b00100,
            0b01010,
            0b01001,
            0b01000,
            0b00000,
            0b00000,
            0b11010
        ]

        # top middle of character
        char_1 = [
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b11111,
            0b01010,
            0b01010,
            0b00000
        ]

        # top right of character
        char_2 = [
            0b00000,
            0b00100,
            0b01010,
            0b10010,
            0b00010,
            0b00000,
            0b00000,
            0b01011
        ]

        # bottom left of character
        char_3 = [
            0b11000,
            0b00000,
            0b00100,
            0b00011,
            0b01000,
            0b01101,
            0b00110,
            0b00010
        ]
        # bottom middle of character
        char_4 = [
            0b00100,
            0b01010,
            0b00000,
            0b11111,
            0b01010,
            0b10001,
            0b00101,
            0b10101
        ]
        # bottom right of character
        char_5 = [
            0b00011,
            0b00000,
            0b00100,
            0b11000,
            0b00000,
            0b00000,
            0b00000,
            0b00000
        ]

        self.lcd.create_char(0, char_0)
        self.lcd.create_char(1, char_1)
        self.lcd.create_char(2, char_2)
        self.lcd.create_char(3, char_3)
