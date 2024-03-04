import time
import sys
import RPi.GPIO as GPIO

morse = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",

}
def morse_code():
    GPIO.setmode(GPIO.BCM) #code that Ryan and I used for Lab 2 D1 to have the RPi flash in Morse
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(18, GPIO.OUT)
    pwm = GPIO.PWM(18, 1000)
    pwm.start(0)
    t = 2
    inpt = sys.argv[2] #after typing 'morse' into the command line you can type your name
    while True:
        if GPIO.input(16):
            for n in inpt: #for loops through the input given
                n = n.lower() # sets every character to lowercase (since morse doesn't have case)
                if n == " ": #accounts for spaces
                    time.sleep(0.2*t)
                else:
                    for m in morse[n]: #loops through dictionary for actual characters
                        if m == "-": #dashes are 0.4 seconds
                            pwm.ChangeDutyCycle(1)
                            time.sleep(0.2*t)
                            pwm.ChangeDutyCycle(0)
                        elif m == ".": #dots are 0.2 seconds
                            pwm.ChangeDutyCycle(1)
                            time.sleep(0.1*t)
                            pwm.ChangeDutyCycle(0)
                        time.sleep(0.1*t) #spacing between characters
                    time.sleep(0.1*t) #spacing between words


if __name__ == "__main__":
    print("To use the morse program type 'morse', then type what you want to be translated") #prompt
    if sys.argv[1] == "morse" #if you type morse then the function runs
        morse_code()