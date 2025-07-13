from RPLCD.i2c import CharLCD#sudo pip3 install RPLCD

screenAddress=0x3F # If your piggy-back board holds PCF8574T chip, then the default is likely 0x27

class Display:
    def __init__(self):
        self.lcd = CharLCD(i2c_expander='PCF8574', address=screenAddress, port=1,
                    cols=20, rows=4, dotsize=8,
                    charmap='A02',
                    auto_linebreaks=False,
                    backlight_enabled=False) #changing this parameter will only work if the jumper for the backlight on the LCD is also on

    def screenChange(self, state):
        self.mode="start"
        self.lcd.clear()
        self.loadChar()
        if state == "starting":
            self.text_stuff("Welcome!", "This is Tim")
        elif state == "happy":
            self.mode="happy"
            self.text_stuff("(^‿^)", "happy")
        elif state == "angry":
            self.mode="angry"
            self.text_stuff("(>_<)", "angry")
        elif state == "sleep":
            self.mode="sleep"
            self.text_stuff("(-.-)Zzz", "sleep")
        elif state == "dead":
            self.mode="dead"
            self.text_stuff("x_x", "dead")
        elif state == "neutral":
            self.mode="neutral"
            self.text_stuff("(・_・)", "neutral")

    def text_stuff(self, emoticon, state):
        self.lcd.cursor_pos = (0, 2)
        self.lcd.write_string(emoticon)
        self.lcd.cursor_pos = (1, 2)
        self.lcd.write_string(state)
    def loadChar(self):
        # Top Left
        char_0 = [
            0b11111, 0b11011, 0b10101, 0b10101,
            0b10110, 0b10111, 0b10111, 0b11101
        ]

        # Top Right
        char_1 = [
            0b11111, 0b11011, 0b10101, 0b10101,
            0b01101, 0b11101, 0b11101, 0b10111
        ]

        # Bottom Left
        char_2 = [
            0b10110, 0b11100, 0b11100, 0b10110,
            0b11011,0b11011, 0b11100, 0b11111
        ]

        # Bottom Right
        char_3 = [
            0b11101, 0b10111, 0b10111, 0b01101,
            0b11011, 0b11011, 0b00111, 0b11111
        ]
        self.lcd.create_char(0, char_0)
        self.lcd.create_char(1, char_1)
        self.lcd.create_char(2, char_2)
        self.lcd.create_char(3, char_3)