from PIL import Image, ImageDraw
import click
import random
import numpy as np
import time

from alone.background import background
from alone.human import color_human


@click.command(help="Feel lonely")
@click.option(
    "--random-seed",
    help="random seed to generate the same image",
    default=(int(time.time())),
)
@click.option("--width", default=1920, help="width of generated image", type=int)
@click.option("--height", default=1080, help="height of generated image", type=int)
@click.option("--humans", default=-1, help="number of humans")
@click.pass_context
def cli(ctx, width, height, random_seed, humans):
    # Human count
    if humans == -1:
        human_count = random.randint(1, 1000)
    else:
        human_count = humans

    # Create a new image
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))

    random.seed(random_seed)

    # Pick human colors
    shadow_distance = random.randint(100, 150)
    human_body_color = (
        random.randint(shadow_distance, 255),
        random.randint(shadow_distance, 255),
        random.randint(shadow_distance, 255),
    )
    human_shadow_color = (
        max(0, human_body_color[0] - shadow_distance),
        max(0, human_body_color[1] - shadow_distance),
        max(0, human_body_color[2] - shadow_distance),
    )

    # Draw background
    background_image = background(
        ctx={
            "width": width,
            "height": height,
            "background_color": (
                int(human_body_color[0] ^ 0xff),
                int(human_body_color[1] ^ 0xff),
                int(human_body_color[2] ^ 0xff),
                255,
            ),
        }
    )
    img.paste(background_image, (0, 0), background_image)

    # Load human
    human_body, human_shadow = color_human(
        ctx={"body": human_body_color, "shadow": human_shadow_color}
    )

    # Choose random positions for people
    humans = []
    while len(humans) < human_count:
        # Save new human position
        x = random.randint(0, width)
        y = random.randint(0, height)
        humans.append((x, y))

    # Load lonely human
    human_lonely_body_color = (
        0xFF - human_body_color[0],
        0xFF - human_body_color[1],
        0xFF - human_body_color[2],
    )
    human_lonely_shadow_color = (
        # max(0, human_lonely_body_color[0] - shadow_distance),
        # max(0, human_lonely_body_color[1] - shadow_distance),
        # max(0, human_lonely_body_color[2] - shadow_distance),
        0xFF - human_shadow_color[0],
        0xFF - human_shadow_color[1],
        0xFF - human_shadow_color[2],
    )
    human_lonely_body, human_lonely_shadow = color_human(
        ctx={"body": human_lonely_body_color, "shadow": human_lonely_shadow_color}
    )

    # Pick lonely human position
    human_lonely_pos = (
        random.randint(width / 3, width * 2 / 3),
        random.randint(height / 2, height * 2 / 3),
    )

    # Draw shadows
    for human in humans:
        img.paste(human_shadow, human, human_shadow)

    img.paste(human_lonely_shadow, human_lonely_pos, human_lonely_shadow)

    # Draw bodies
    for human in humans:
        img.paste(human_body, human, human_body)

    img.paste(human_lonely_body, human_lonely_pos, human_lonely_body)

    # Save the image
    img.save("alone_{}.png".format(random_seed))
    img.show()


if __name__ == "__main__":
    cli()
