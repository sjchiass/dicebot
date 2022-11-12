import os
import math
from PIL import Image
import itertools

backgrounds = [Image.open(f"./empty_pics/{x}") for x in os.listdir("./empty_pics")]
#print(backgrounds)

dice = os.listdir("./dice_pics")
dice = {"0":[],
    "1":[x for x in dice if x.split("_")[0] == "1"],
    "2":[x for x in dice if x.split("_")[0] == "2"],
    "3":[x for x in dice if x.split("_")[0] == "3"],
    "4":[x for x in dice if x.split("_")[0] == "4"],
    "5":[x for x in dice if x.split("_")[0] == "5"],
    "6":[x for x in dice if x.split("_")[0] == "6"]}
#print(dice)
#print(*[len(x) for x in dice])

dice_images = [[Image.open(f"./dice_pics/{x}") for x in dice[str(i)]] for i in range(0, 6+1)]
#print(dice_images)

if not os.path.exists("training_data"):
    os.makedirs("training_data")
for i in range(6, 36+1):
    if not os.path.exists(f"./training_data/{i}"):
            os.makedirs(f"./training_data/{i}")

class ImageGenerator:
    def __init__(self):
        # Global counter
        self.counter = 0
        # Possible dice
        possible_dice_values = [1, 2, 3, 4, 5, 6]
        self.dice = [[] for x in range(36+1)]
        for a in possible_dice_values:
            for b in possible_dice_values:
                for c in possible_dice_values:
                    for d in possible_dice_values:
                        for e in possible_dice_values:
                            for f in possible_dice_values:
                              s = sum([a, b, c, d, e, f])
                              self.dice[s].append([a, b, c, d, e, f])
        self.dice_counter = [0 for x in range(36+1)]
        self.dice_len = [len(x) for x in self.dice]
        # Possible backgrounds
        self.backgrounds = backgrounds.copy()
        self.backgrounds_counter = 0
        self.backgrounds_len = len(self.backgrounds)
        # Possible angles
        raw_angles = list(itertools.combinations([45*i for i in range(8)], 6))
        self.angles = []
        for noise in range(45):
            for raw in raw_angles:
                self.angles.append([x+noise for x in raw])
        self.angles_counter = 0
        self.angles_len = len(self.angles)
        # Dice images
        self.dice_images = dice_images.copy()
        self.dice_images_counter = [0 for x in range(36+1)]
        self.dice_images_len = [len(x) for x in self.dice_images]
    def get_possible_combinations(self, total_value):
        return self.dice_len[total_value]
    def get_dice(self, dvalue):
        dice = self.dice[dvalue][self.dice_counter[dvalue] % self.dice_len[dvalue]]
        self.dice_counter[dvalue] += 1
        return dice
    def get_background(self):
        background = self.backgrounds[self.backgrounds_counter % self.backgrounds_len]
        self.backgrounds_counter += 1
        return background
    def get_angles(self):
        angles = self.angles[self.angles_counter % self.angles_len]
        self.angles_counter += 1
        return angles
    def get_dice_image(self, dvalue):
        dice_image = self.dice_images[dvalue][self.dice_images_counter[dvalue] % self.dice_images_len[dvalue]]
        self.dice_images_counter[dvalue] += 1
        return dice_image
    def generate(self, dvalue):
        # Pull in necessary values, which increases their internal counters
        dice = self.get_dice(dvalue)
        background = self.get_background()
        angles = self.get_angles()
        dice_images = [self.get_dice_image(x) for x in dice]
        # Build the image
        output = background.copy()
        for image, angle in zip(dice_images, angles):
            output.paste(image,
                (int(50-15 + 35*math.cos(math.radians(angle))),
                int(50-15 + 35*math.sin(math.radians(angle)))), image)
        output.convert("L").save(f"./training_data/{sum(dice)}/d{self.counter}.jpg", quality=85)
        self.counter += 1

image_gen = ImageGenerator()
for total_value in range(6, 36+1):
    # Generate 1x the amount of combinations for a particular value, or
    # generate at least 1000 because some total values have very few
    # combinations. If you want more data, increase these amounts.
    draws = max(1000, 1*image_gen.get_possible_combinations(total_value))
    for i in range(draws):
        image_gen.generate(total_value)
