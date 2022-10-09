from PIL import Image, ImageDraw
import numpy as np
import os


def color_human(ctx):
    # Get path to human
    maindir = os.path.dirname(__file__)
    human_path = os.path.join(maindir, "../assets/human_pre.png")

    # Load human template
    human = Image.open(human_path).convert("RGBA")
    data_original = np.array(human)

    # Build human body
    data = data_original.copy()
    red, green, blue, _ = data.T
    human_body_selector = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][human_body_selector.T] = ctx.get("body")
    # Remove shadow
    human_shadow_selector = (red == 0) & (blue == 0) & (green == 0)
    data[...][human_shadow_selector.T] = (0, 0, 0, 0)

    # Create human body
    human_body = Image.fromarray(data)

    # Build human shadow
    data = data_original.copy()
    red, green, blue, _ = data.T
    human_shadow_shadow = (red == 0) & (blue == 0) & (green == 0)
    data[..., :-1][human_shadow_shadow.T] = ctx.get("shadow")
    # Remove body
    human_body_selector = (red == 255) & (blue == 255) & (green == 255)
    data[...][human_body_selector.T] = (0, 0, 0, 0)

    # Create human shadow
    human_shadow = Image.fromarray(data)

    # Return body and shadow
    return (human_body, human_shadow)
