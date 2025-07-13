from display import Display

class Stats:
    def __init__(self):
        self.happiness = 5
        self.hunger=5
        self.sleep=5
    def happinessChange(self, reason):
        if self.happiness>0 and self.happiness<10:
            if reason=="petting":
                self.happiness+=1
            elif reason== "no petting":
                self.happiness-=.2
        else:
            print("shes already so happy!")
    def hungerChange(self, reason):
        if self.hunger>0 and self.hunger<10:
            if reason =="eat":
                hunger+=1
            if reason=="no eat":
                hunger-=.2
            if reason=="sleep":
                hunger-=.5
        else:
            print("shes not hungry!")
    def sleepChange(self, reason, state):
        if self.sleep>0 and self.sleep<10:
            if reason=="eating":
                sleep-=.5
            if reason=="sleep":
                sleep+=1
            if reason=="no sleep":
                sleep-=.1
        else:
            print("shes not sleepy")

class Appearance:
    def __init__(self, stats, display):
        self.pet = stats
        self.display = display

    def changeFace(self):
        if self.pet.hunger == 0 or self.pet.happiness==0 or self.pet.sleep==0:
            self.Display.screenChange("dead")
        elif self.pet.hunger>7 and self.pet.happiness>7 and self.pet.sleep>7:
            self.Display.screenChange("happy")
        elif self.pet.hunger<4 or self.pet.happiness<4 or self.pet.sleep<4:
            self.Display.screenChange("angry")
    
        