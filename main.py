from inky import InkyWHAT
import time
import random
import pathlib
inky_display = InkyWHAT("red")
inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw

# This function will take a quote as a string, a width to fit
# it into, and a font (one that's been loaded) and then reflow
# that quote with newlines to fit into the space required.


def reflow_quote(quote, width, font):
    words = quote.split(" ")
    reflowed = '"'
    line_length = 0
    num_lines = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n  " + word
            num_lines += 1

            if num_lines == 4 :
                return reflowed.rstrip() + '"'

    reflowed = reflowed.rstrip() + '"'

    return reflowed


# Set up the correct display and scaling factors
inky_display = InkyWHAT("black")
inky_display.set_border(inky_display.WHITE)

w = inky_display.WIDTH * 3
h = inky_display.HEIGHT * 3

# Create a new canvas to draw on



# Load the fonts

font_size = 70

font = ImageFont.truetype("/home/pi/Brain-Box-Alpha/Cambria.ttf", font_size)

padding = 150
max_width = w - padding
max_height = h - padding - font.getsize("ABCD ")[1]

essay_data = []
with open("/home/pi/Brain-Box-Alpha/data/all_essays.txt", "r") as f :
    for line in f.readlines() :
        for sentence in line.split(".") :
            if len(sentence.strip()) > 5 :
                essay_data.append(sentence.strip())

ai_data = []
with open("/home/pi/Brain-Box-Alpha/data/output_corrected.txt", "r") as f :
    for line in f.readlines() :
        for sentence in line.split(".") :
            if len(sentence.strip()) > 5 :
                ai_data.append(sentence.strip())
        
while True :
    img = Image.new("P", (inky_display.WIDTH * 3, inky_display.HEIGHT * 3))
    draw = ImageDraw.Draw(img)
    draw.fontmode = "L"
    choice = random.randint(0,1)

    essay_x = (w - max_width) / 2
    essay_y = 60

    ai_x = (w - max_width) / 2
    ai_y = 460

    if choice == 1 :
        essay_y = 460
        ai_y = 60

    essay = random.choice(essay_data)
    ai = random.choice(ai_data)

    print(f"Essay choice: {essay}\nAI choice: {ai}\nAI is {choice}")

    reflowed_essay = reflow_quote(essay.capitalize(), max_width, font)
    draw.multiline_text((essay_x, essay_y), reflowed_essay, fill=inky_display.BLACK, font=font, align="left")

    reflowed_ai = reflow_quote(ai.capitalize(), max_width, font)
    draw.multiline_text((ai_x, ai_y), reflowed_ai, fill=inky_display.BLACK, font=font, align="left")

    img_resized = img.resize((inky_display.WIDTH,inky_display.HEIGHT), Image.ANTIALIAS)
    inky_display.set_image(img_resized.rotate(0, expand=True))
    inky_display.show()

    time.sleep(5)
    
    print(f"Revealing that {choice} is the AI")
    img = Image.new("P", (inky_display.WIDTH*3, inky_display.HEIGHT*3))
    draw = ImageDraw.Draw(img)
    draw.fontmode = "1"
    draw.rectangle((padding / 4, ai_y, w - (padding / 4), ai_y + 430 - (padding / 4)), fill=inky_display.RED)
    draw.multiline_text((essay_x, essay_y), reflowed_essay, fill=inky_display.BLACK, font=font, align="left")
    draw.multiline_text((ai_x, ai_y), reflowed_ai, fill=inky_display.BLACK, font=font, align="left")
    img_resized = img.resize((inky_display.WIDTH,inky_display.HEIGHT), Image.ANTIALIAS)
    inky_display.set_image(img_resized.rotate(0, expand=True))
    inky_display.show()
    time.sleep(5)