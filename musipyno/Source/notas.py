__author__ = '06226901'

class notas():

    def __init__(self):
        self.NOTE_B0 = 31
        self.NOTE_C1 = 33
        self.NOTE_CS1 = 35
        self.NOTE_D1  = 37
        self.NOTE_DS1 = 39
        self.NOTE_E1  = 41
        self.NOTE_F1  = 44
        self.NOTE_FS1 = 46
        self.NOTE_G1  = 49
        self.NOTE_GS1 = 52
        self.NOTE_A1  = 55
        self.NOTE_AS1 = 58
        self.NOTE_B1  = 62
        self.NOTE_C2  = 65
        self.NOTE_CS2 = 69
        self.NOTE_D2  = 73
        self.NOTE_DS2 = 78
        self.NOTE_E2  = 82
        self.NOTE_F2  = 87
        self.NOTE_FS2 = 93
        self.NOTE_G2  = 98
        self.NOTE_GS2 = 104
        self.NOTE_A2  = 110
        self.NOTE_AS2 = 117
        self.NOTE_B2  = 123
        self.NOTE_C3  = 131
        self.NOTE_CS3 = 139
        self.NOTE_D3  = 147
        self.NOTE_DS3 = 156
        self.NOTE_E3  = 165
        self.NOTE_F3  = 175
        self.NOTE_FS3 = 185
        self.NOTE_G3  = 196
        self.NOTE_GS3 = 208
        self.NOTE_A3  = 220
        self.NOTE_AS3 = 233
        self.NOTE_B3  = 247
        self.NOTE_C4  = 262
        self.NOTE_CS4 = 277
        self.NOTE_D4  = 294
        self.NOTE_DS4 = 311
        self.NOTE_E4  = 330
        self.NOTE_F4  = 349
        self.NOTE_FS4 = 370
        self.NOTE_G4  = 392
        self.NOTE_GS4 = 415
        self.NOTE_A4  = 440
        self.NOTE_AS4 = 466
        self.NOTE_B4  = 494
        self.NOTE_C5  = 523
        self.NOTE_CS5 = 554
        self.NOTE_D5  = 587
        self.NOTE_DS5 = 622
        self.NOTE_E5  = 659
        self.NOTE_F5  = 698
        self.NOTE_FS5 = 740
        self.NOTE_G5  = 784
        self.NOTE_GS5 = 831
        self.NOTE_A5  = 880
        self.NOTE_AS5 = 932
        self.NOTE_B5  = 988
        self.NOTE_C6  = 1047
        self.NOTE_CS6 = 1109
        self.NOTE_D6  = 1175
        self.NOTE_DS6 = 1245
        self.NOTE_E6  = 1319
        self.NOTE_F6  = 1397
        self.NOTE_FS6 = 1480
        self.NOTE_G6  = 1568
        self.NOTE_GS6 = 1661
        self.NOTE_A6  = 1760
        self.NOTE_AS6 = 1865
        self.NOTE_B6  = 1976
        self.NOTE_C7  = 2093
        self.NOTE_CS7 = 2217
        self.NOTE_D7  = 2349
        self.NOTE_DS7 = 2489
        self.NOTE_E7  = 2637
        self.NOTE_F7  = 2794
        self.NOTE_FS7 = 2960
        self.NOTE_G7  = 3136
        self.NOTE_GS7 = 3322
        self.NOTE_A7  = 3520
        self.NOTE_AS7 = 3729
        self.NOTE_B7  = 3951
        self.NOTE_C8  = 4186
        self.NOTE_CS8 = 4435
        self.NOTE_D8  = 4699
        self.NOTE_DS8 = 4978

        self.notas = [0,
                      self.NOTE_C4, self.NOTE_CS4, self.NOTE_D4, self.NOTE_DS4, self.NOTE_E4, self.NOTE_F4, self.NOTE_FS4, self.NOTE_G4, self.NOTE_GS4, self.NOTE_A4, self.NOTE_AS4, self.NOTE_B4,
                      self.NOTE_C5, self.NOTE_CS5, self.NOTE_D5, self.NOTE_DS5, self.NOTE_E5, self.NOTE_F5, self.NOTE_FS5, self.NOTE_G5, self.NOTE_GS5, self.NOTE_A5, self.NOTE_AS5, self.NOTE_B5,
                      self.NOTE_C6, self.NOTE_CS6, self.NOTE_D6, self.NOTE_DS6, self.NOTE_E6, self.NOTE_F6, self.NOTE_FS6, self.NOTE_G6, self.NOTE_GS6, self.NOTE_A6, self.NOTE_AS6, self.NOTE_B6,
                      self.NOTE_C7, self.NOTE_CS7, self.NOTE_D7, self.NOTE_DS7, self.NOTE_E7, self.NOTE_F7, self.NOTE_FS7, self.NOTE_G7, self.NOTE_GS7, self.NOTE_A7, self.NOTE_AS7, self.NOTE_B7]

    def gettono(self, a):
        return self.notas[a]
