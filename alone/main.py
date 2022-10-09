from PIL import Image, ImageDraw
import click
import random
import numpy as np

from alone.human import color_human, overlap

# @click.pass_context
def cli(width: int = 1920, height: int = 1080):
    # click.echo("Hello, World!")
    print("yo")

    # Create a new image
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))

    # Load human
    human = color_human(ctx={"body": (255, 0, 0), "shadow": (155, 0, 0)})
    # human.show()

    # Add humans
    humans = []
    human_count = random.randint(100, 1000)
    while len(humans) < human_count:
        x = random.randint(0, width)
        y = random.randint(0, height)
        # if overlap(humans, (human.width, human.height), (x, y)):
        #     continue

        # Save new human position
        humans.append((x, y))

        img.paste(human, (x, y), human)

    # Save the image
    img.save("alone.png")
    img.show()


if __name__ == "__main__":
    cli()
