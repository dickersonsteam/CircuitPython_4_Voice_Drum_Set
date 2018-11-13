import time
import audioio
import board
import digitalio

# list all samples here
samples = [audioio.WaveFile(open("kick.wav", "rb")),
           audioio.WaveFile(open("snare.wav", "rb")),
           audioio.WaveFile(open("hihat.wav", "rb")),
           audioio.WaveFile(open("crash.wav", "rb"))]

# list all input buttons here
buttons = [digitalio.DigitalInOut(board.D3),
           digitalio.DigitalInOut(board.D6), 
           digitalio.DigitalInOut(board.D5),
           digitalio.DigitalInOut(board.D4)]

# initialize speaker output pin
audio_pin = audioio.AudioOut(board.A0)
   
# initialize all buttons in the list   
for i in buttons:
    i.switch_to_input(pull=digitalio.Pull.UP)

# test all buttons
print("Test Buttons")

for index, button in enumerate(buttons):
    print("Push Button " + str(index))
    while button.value:
        pass
    print(str(i))
    print("Button " + str(index) + " works.")
    
print("All buttons work.")

# create mixer object with the number of voices required
mixer = audioio.Mixer(voice_count=5,
                      sample_rate=22050,
                      channel_count=1,
                      bits_per_sample=16,
                      samples_signed=True)

# start outputing the mixer to the DAC
audio_pin.play(mixer)

was_released = []
for i in buttons:
    was_released.append(True)


pad_length = 8.00
start_time = time.monotonic()
mixer.play(audioio.WaveFile(open("pad2mini.wav", "rb")), voice=4)

# main body loop
# check buttons and play sample in mixer
while True:
    if time.monotonic() > (start_time + pad_length):
        start_time = time.monotonic()
        mixer.play(audioio.WaveFile(open("pad2mini.wav", "rb")), voice=4) 
       
    for index, button in enumerate(buttons):
        if not button.value and was_released[index]:
            was_released[index] = False
            mixer.play(samples[index], voice=index)
            print("Playing sample " + str(index) + ".")
        elif button.value:
            was_released[index] = True
        
    # debounce delay
    time.sleep(0.01)
    