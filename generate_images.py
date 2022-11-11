import os
import math
import random
from PIL import Image, ImageDraw
from io import BytesIO

backgrounds = [Image.open(f"./empty_pics/{x}") for x in os.listdir("./empty_pics")]
#print(backgrounds)

dice = os.listdir("./dice_pics")
dice = {"1":[x for x in dice if x.split("_")[0] == "1"],
    "2":[x for x in dice if x.split("_")[0] == "2"],
    "3":[x for x in dice if x.split("_")[0] == "3"],
    "4":[x for x in dice if x.split("_")[0] == "4"],
    "5":[x for x in dice if x.split("_")[0] == "5"],
    "6":[x for x in dice if x.split("_")[0] == "6"]}
#print(dice)
#print(*[len(x) for x in dice])

dice_images = {str(i):[Image.open(f"./dice_pics/{x}") for x in dice[str(i)]] for i in range(1, 6+1)}
#print(dice_images)

if not os.path.exists("training_data"):
    os.makedirs("training_data")
for i in range(6, 36+1):
    if not os.path.exists(f"./training_data/{i}"):
            os.makedirs(f"./training_data/{i}")

for n in range(10000):
    random_bg = random.choice(backgrounds).copy()
    random_angles = random.sample([45*i for i in range(8)], k=6)
    random_dice = random.choices(["1", "2", "3", "4", "5", "6"], k=6)
    dice_sum = sum([int(i) for i in random_dice])
    for d in range(6):
        random_value = random_dice[d]
        random_fg = random.choice(dice_images[random_value]).copy().rotate(random.randrange(360))
        axis_rotation = random_angles[d]
        random_bg.paste(random_fg, 
            (int(50-15 + 35*math.cos(math.radians(axis_rotation))), 
                int(50-15 + 35*math.sin(math.radians(axis_rotation)))), random_fg)
    random_bg.convert("L").save(f"./training_data/{dice_sum}/{n}.jpg", quality=85)

