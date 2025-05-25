from microbit import *
import time

smoothing_len = 10
value_thresh = 3
ts_thresh = 0.1
ts_deltas = []
deltas_minlen = 5

smoothing = [0] * smoothing_len
lastval = 0
lastts = -1 - ts_thresh

notes = (
    Image("00900:09900:90990:00999:00999"),
    Image("00900:00990:09909:99900:99900")
)
curr_note = 0
count = 5

def show (img):
    display.show (img, delay = 250, wait = False, clear = True)

pin1.write_analog(round(1023 * 0.12))

while True:
    while not button_a.is_pressed ():
        show (count)
        if button_b.is_pressed ():
            count = (count + 1) % 10
            show (count)
            display.show (count, wait = False, clear = True)
            while button_b.is_pressed ():
                pass
    while button_a.is_pressed ():
        pass
    while not button_b.is_pressed ():
        smoothing.append (microphone.sound_level ())
        del smoothing [0]
        currval = sum (smoothing) / len (smoothing)
        if currval > lastval + value_thresh:
            currts = time.ticks_ms () / 1000
            if currts > lastts + ts_thresh:
                ts_deltas.append (currts - lastts)
                if len (ts_deltas) > deltas_minlen:
                    ts_deltas.pop (0)
                show (notes [curr_note])
                curr_note = not curr_note
            lastts = currts
        lastval = currval
        if button_a.is_pressed ():
            while button_a.is_pressed ():
                pass
            break
    else:
        tempo = sum (ts_deltas) / deltas_minlen
        i = count
        pin2.write_analog(300)
        for i in range (i, 0, -1):
            show (i)
            time.sleep (tempo)
        pin1.write_analog(round(1023 * 0.05))
        sleep(1000)
        pin1.write_analog(round(1023 * 0.12))
