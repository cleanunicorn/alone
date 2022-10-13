from PIL import Image
import math
import random


def generate_noise(width, height):
    noise = []
    for y in range(height):
        noise.append([])
        for x in range(width):
            noise[y].append(random.randint(0, 32768) / 32768.0)
    return noise


def smooth_noise(noise, x, y, width, height):
    # Get fractional part of x and y
    fract_x = x - int(x)
    fract_y = y - int(y)

    # Wrap around
    x1 = int((int(x) + width) % width)
    y1 = int((int(y) + height) % height)

    # Neighbor values
    x2 = int((x1 + width - 1) % width)
    y2 = int((y1 + height - 1) % height)

    # Smooth the noise with bilinear interpolation
    value = 0.0
    value += fract_x * fract_y * noise[y1][x1]
    value += (1 - fract_x) * fract_y * noise[y1][x2]
    value += fract_x * (1 - fract_y) * noise[y2][x1]
    value += (1 - fract_x) * (1 - fract_y) * noise[y2][x2]

    return value


def turbulence(noise, x, y, size):
    value = 0.0
    initial_size = size

    while size >= 1:
        value += smooth_noise(noise, x / size, y / size, size, size) * size
        size /= 2.0

    return 128.0 * value / initial_size


def background(ctx):
    # Get width and height
    width = ctx.get("width")
    height = ctx.get("height")

    # Get background color
    background_color = ctx.get("background_color")

    # Create background
    background_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    # Repetitions in x and y direction
    x_period = 0
    y_period = 1

    # Turbulence power
    turb_power = 2  # makes twists
    turb_size = 128  # initial size of the turbulence

    noise = generate_noise(width, height)

    for x in range(width):
        for y in range(height):
            xy_value = (
                x * x_period / width
                + y * y_period / height
                + turb_power * turbulence(noise, x, y, turb_size) / 256.0
            )
            sine_value = int(256 * abs(math.sin(xy_value * math.pi)))
            background_image.putpixel(
                (x, y),
                (
                    sine_value & background_color[0],
                    sine_value & background_color[1],
                    sine_value & background_color[2],
                    64,
                ),
            )

    # Return background
    return background_image
