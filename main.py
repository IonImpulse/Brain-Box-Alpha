from inky import InkyWHAT
import time
import random
inky_display = InkyWHAT("red")
inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw
from font_source_serif_pro import SourceSerifProSemibold
from font_source_sans_pro import SourceSansProSemibold


# This function will take a quote as a string, a width to fit
# it into, and a font (one that's been loaded) and then reflow
# that quote with newlines to fit into the space required.


def reflow_quote(quote, width, font):
    words = quote.split(" ")
    reflowed = '"'
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n  " + word

    reflowed = reflowed.rstrip() + '"'

    return reflowed


# Set up the correct display and scaling factors
inky_display = InkyWHAT("black")
inky_display.set_border(inky_display.WHITE)
inky_display.set_rotation(0)

w = inky_display.WIDTH
h = inky_display.HEIGHT

# Create a new canvas to draw on

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# Load the fonts

font_size = 24

author_font = ImageFont.truetype(SourceSerifProSemibold, font_size)
quote_font = ImageFont.truetype(SourceSansProSemibold, font_size)

padding = 50
max_width = w - padding
max_height = h - padding - author_font.getsize("ABCD ")[1]

essay_data = []
with open("data/all_essays.txt", "r") as f :
    for line in f.readlines() :
        for sentence in line.split(".") :
            essay_data.append(sentence)

ai_data = []
with open("data/output_corrected.txt", "r") as f :
    for line in f.readlines() :
        for sentence in line.split(".") :
            ai_data.append(sentence)
        
while True :
    choice = random.randint(0,1)

    essay_x = (w - max_width) / 2
    essay_y = 20

    ai_x = (w - max_width) / 2
    ai_y = 160

    if choice == 1 :
        essay_y, ai_y = ai_y, essay_y

    essay = random.choice(essay_data)
    ai = random.choice(ai_data)

    print(f"Essay choice: {essay}\nAI choice: {ai}\nAI is {choice}")

    reflowed_essay = reflow_quote(essay, max_width, quote_font)
    draw.multiline_text((essay_x, essay_y), reflowed_essay, fill=inky_display.BLACK, font=quote_font, align="left")

    reflowed_ai = reflow_quote(ai, max_width, quote_font)
    draw.multiline_text((ai_x, ai_y), reflowed_ai, fill=inky_display.BLACK, font=quote_font, align="left")

    inky_display.set_image(img.rotate(270, expand=True))
    inky_display.show()

    time.sleep(5)
    
    draw.rectangle((padding / 4, padding / 4, w - (padding / 4), ai_y - (padding / 4)), fill=inky_display.RED)