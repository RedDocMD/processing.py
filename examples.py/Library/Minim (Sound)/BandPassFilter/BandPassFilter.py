"""
 * Band Pass Filter
 * by Damien Di Fede. (Adapted to Python by Jonathan Feinberg)
 *     
 * This sketch demonstrates how to use the BandPass effect.
 * Move the mouse left and right to change the frequency of the pass band.
 * Move the mouse up and down to change the band width of the pass band.
"""

from ddf.minim import Minim, AudioPlayer
from ddf.minim.effects import BandPass

def setup():
    size(512, 200, P2D)

    global minim, groove, bpf
    
    minim = Minim(this)
    
    groove = minim.loadFile("groove.mp3")
    groove.loop()
    # make a band pass filter with a center frequency of 440 Hz and a bandwidth of 20 Hz
    # the third argument is the sample rate of the audio that will be filtered
    # it is required to correctly compute values used by the filter
    bpf = BandPass(440, 20, groove.sampleRate())
    groove.addEffect(bpf)

def draw():
    background(0)
    stroke(255)
    # draw the waveforms
    # the values returned by left.get() and right.get() will be between -1 and 1,
    # so we need to scale them up to see the waveform
    for i in xrange(groove.right.size() - 1):
        x1 = map(i, 0, groove.bufferSize(), 0, width)
        x2 = map(i + 1, 0, groove.bufferSize(), 0, width)
        line(x1, height / 4 - groove.left.get(i) * 50, 
             x2, height / 4 - groove.left.get(i + 1) * 50)
        line(x1, 3 * height / 4 - groove.right.get(i) * 50, 
             x2, 3 * height / 4 - groove.right.get(i + 1) * 50)
    
    # draw a rectangle to represent the pass band
    noStroke()
    fill(255, 0, 0, 60)
    rect(mouseX - bpf.getBandWidth() / 20, 0, bpf.getBandWidth() / 10, height)

def mouseMoved():
    # map the mouse position to the range [100, 10000], an arbitrary range of passBand frequencies
    passBand = map(mouseX, 0, width, 100, 2000)
    bpf.setFreq(passBand)
    bandWidth = map(mouseY, 0, height, 50, 500)
    bpf.setBandWidth(bandWidth)
    # prints the new values of the coefficients in the console
    bpf.printCoeff()

def stop():
    # always close Minim audio classes when you finish with them
    groove.close()
    # always stop Minim before exiting
    minim.stop()

