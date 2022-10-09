from PIL import Image, ImageDraw
import numpy as np


def color_human(ctx):
    human = Image.open("../static/human_pre.png").convert("RGBA")
    data = np.array(human)

    # Replace human shadow with color
    red, green, blue, alpha = data.T
    human_shadow = (red == 0) & (blue == 0) & (green == 0)
    data[..., :-1][human_shadow.T] = ctx.get("shadow")

    # Replace human body with color
    red, green, blue, alpha = data.T
    human_body = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][human_body.T] = ctx.get("body")

    human = Image.fromarray(data)
    return human


def inside(human, size, pos) -> bool:
    if (human[0] < pos[0] and pos[0] < human[0] + size[0]) and (
        human[1] < pos[1] and pos[1] < human[1] + size[1]
    ):
        return True

def isRectangleOverlap(R1, R2):
    if (R1[0]>=R2[2]) or (R1[2]<=R2[0]) or (R1[3]<=R2[1]) or (R1[1]>=R2[3]):
        return False

    return True

def overlap(humans, size, pos) -> bool:
    for human in humans:
        rect1 = [human[0], human[1], human[0] + size[0], human[1] + size[1]]
        rect2 = [pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]]

        if isRectangleOverlap(rect1, rect2):
            return True

    return False
