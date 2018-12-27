#Discord bot that tells you what acronyms stand for.
#(It's always about the library books)

from key import key

import discord
import re
import itertools
from random import *
import math

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

from io import BytesIO

client = discord.Client()

sentences = [
    "Turns their library books in on time",
    "Respects all people regardless of socioeconomic status",
    "Does their homework thouroughly every day",
    "Always says thank you to the lunch lady",
    "Thinks bullying is super not cool",
    "Values diversity as part of a healthy community",
    "Secretly thinks this bot is hilarious",
    "Posts epic gamer moments on Snapchat"
]
for c, sentence in enumerate(sentences):
    sentences[c] = sentence.split()

test_regex = re.compile(r"(yeah|yes|yep)[,.!?;]? (\S+) .+ (\S+$)", re.I) #Finds (for example) "Yes I used Regex" w/o two whitespace at the end.

def do_acronym(message):
    # Returns a list with strings with 0, 1 or 2 words in the yes_book_message
    words = choice(sentences)
    zipped = itertools.zip_longest(message, words)
    output = ""
    for tup in zipped:
        char = tup[0]
        word = tup[1]
        
        if char is None:
            #no more letters, but still words
            output += "  : %s \n" % word
        elif word is None:
            #ran out of words, but still have acronym letters
            output += "%s:\n" % char
        else:
            output += "%s: %s\n" % tup
        
    if output[-1] == '\n': output = output[:-1]
    return output

def make_image(header, acronym):

    fs = 40 #font size
    text_img_width = len(header) * fs # 16 px per letter and 1 letter of padding per side
    text_img_height = (acronym.count('\n') + 2) * fs*2

    src_pad_x = math.floor(text_img_width/2.2)
    src_pad_y = math.floor(text_img_height/8.4)

    src_image = Image.open("sonic.png").resize((text_img_width, text_img_height))

    font = ImageFont.truetype("alba.ttf", fs)

    draw = ImageDraw.Draw(src_image)
    rand_color = (randint(0, 150), randint(50, 150), randint(0, 150))
    draw.text((src_pad_x, src_pad_y), header, font=font, fill=rand_color)
    rand_color = (randint(50, 150), randint(0, 150), randint(0, 150))
    draw.text((src_pad_x, src_pad_y + fs*3), acronym, font=font, fill=rand_color)

    fried_image = fry_image(src_image)

def fry_image(image):
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(20)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(50)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(50)
    for _ in range(20):
        image = image.filter(ImageFilter.SHARPEN)

    #image.convert('JPEG')
    image.save("fried.jpeg", 'JPEG', quality=3)



@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user: return #make sure we don't catch our own messages

    match = test_regex.search(message.content)
    if not match: return

    full_acronym = do_acronym(match[3].upper())

    #header last, b/c reasons
    header = match.string[:match.start(3)].capitalize() + match[3].upper()
    if match[2] == "i" or match[2] == "I":
        header = "%s%s%s" % (header[:match.start(2)], \
            message.author.name, header[match.end(2):])

    make_image(header, full_acronym)

    with open("fried.jpeg", 'rb') as fried:
        discord_fried = discord.File(fried)
        await message.channel.send(file=discord_fried)


client.run(key) #the super secret!