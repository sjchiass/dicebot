import os
import math
import random
from PIL import Image
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

possible_dice_values = [1, 2, 3, 4, 5, 6]
for a in possible_dice_values:
    for b in possible_dice_values:
        for c in possible_dice_values:
            for d in possible_dice_values:
                for e in possible_dice_values:
                    for f in possible_dice_values:
                        random_bg = random.choice(backgrounds).copy()
                        angle_noise = random.randrange(45)
                        random_angles = random.sample([45*i+angle_noise for i in range(8)], k=6)
                        chosen_dice = [a, b, c, d, e, f]
                        dice_sum = sum(chosen_dice)
                        for i in range(6):
                            dice_value = chosen_dice[i]
                            random_fg = random.choice(dice_images[str(dice_value)]).copy().rotate(random.randrange(360))
                            axis_rotation = random_angles[i]
                            random_bg.paste(random_fg, 
                                (int(50-15 + 35*math.cos(math.radians(axis_rotation))), 
                                    int(50-15 + 35*math.sin(math.radians(axis_rotation)))), random_fg)
                        random_bg.convert("L").save(f"./training_data/{dice_sum}/d{a}{b}{c}{d}{e}{f}.jpg", quality=85)

