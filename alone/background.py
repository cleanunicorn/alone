#   //xPeriod and yPeriod together define the angle of the lines
#   //xPeriod and yPeriod both 0 ==> it becomes a normal clouds or turbulence pattern
#   double xPeriod = 5.0; //defines repetition of marble lines in x direction
#   double yPeriod = 10.0; //defines repetition of marble lines in y direction
#   //turbPower = 0 ==> it becomes a normal sine pattern
#   double turbPower = 5.0; //makes twists
#   double turbSize = 32.0; //initial size of the turbulence

#   for(int y = 0; y < h; y++)
#   for(int x = 0; x < w; x++)
#   {
#     double xyValue = x * xPeriod / noiseWidth + y * yPeriod / noiseHeight + turbPower * turbulence(x, y, turbSize) / 256.0;
#     double sineValue = 256 * fabs(sin(xyValue * 3.14159));
#     color.r = color.g = color.b = Uint8(sineValue);
#     pset(x, y, color);
#   }

from PIL import Image
import math
import random

# void generateNoise()
# {
# for (int y = 0; y < noiseHeight; y++)
# for (int x = 0; x < noiseWidth; x++)
# {
#     noise[y][x] = (rand() % 32768) / 32768.0;
# }
# }

def generate_noise(width, height):
    noise = []
    for y in range(height):
        noise.append([])
        for x in range(width):
            noise[y].append(random.randint(0, 32768) / 32768.0)
    return noise

# double smoothNoise(double x, double y)
# {
#    //get fractional part of x and y
#    double fractX = x - int(x);
#    double fractY = y - int(y);

#    //wrap around
#    int x1 = (int(x) + noiseWidth) % noiseWidth;
#    int y1 = (int(y) + noiseHeight) % noiseHeight;

#    //neighbor values
#    int x2 = (x1 + noiseWidth - 1) % noiseWidth;
#    int y2 = (y1 + noiseHeight - 1) % noiseHeight;

#    //smooth the noise with bilinear interpolation
#    double value = 0.0;
#    value += fractX     * fractY     * noise[y1][x1];
#    value += (1 - fractX) * fractY     * noise[y1][x2];
#    value += fractX     * (1 - fractY) * noise[y2][x1];
#    value += (1 - fractX) * (1 - fractY) * noise[y2][x2];

#    return value;
# }

def smooth_noise(x, y, width, height):
    # Get fractional part of x and y
    fract_x = x - int(x)
    fract_y = y - int(y)

    # Wrap around
    x1 = (int(x) + width) % width
    y1 = (int(y) + height) % height

    # Neighbor values
    x2 = (x1 + width - 1) % width
    y2 = (y1 + height - 1) % height

    # Smooth the noise with bilinear interpolation
    value = 0.0
    value += fract_x * fract_y * noise[y1][x1]
    value += (1 - fract_x) * fract_y * noise[y1][x2]
    value += fract_x * (1 - fract_y) * noise[y2][x1]
    value += (1 - fract_x) * (1 - fract_y) * noise[y2][x2]

    return value

# double turbulence(double x, double y, double z, double size)
# {
#   double value = 0.0, initialSize = size;

#   while(size >= 1)
#   {
#     value += smoothNoise(x / size, y / size, z / size) * size;
#     size /= 2.0;
#   }

#   return(128.0 * value / initialSize);
# }

def turbulence(x, y, size):
    value = 0.0
    initial_size = size

    while size >= 1:
        value += smooth_noise(x / size, y / size, size, size) * size
        size /= 2.0

    return 128.0 * value / initial_size

def background(ctx):
    # Get width and height
    width = ctx.get("width")
    height = ctx.get("height")

    # Get background color
    background_color = ctx.get("background_color")

    # Create background
    background_image = Image.new("RGBA", (width, height), background_color)

    # Repetitions in x and y direction
    x_period = 5
    y_period = 10

    # Turbulence power
    turb_power = 5 # makes twists
    turb_size = 32 # initial size of the turbulence

    for x in range(width):
        for y in range(height):
            xy_value = x * x_period / width + y * y_period / height + turb_power * turbulence(x, y, turb_size) / 256.0
            sine_value = 256 * abs(math.sin(xy_value * math.pi))
            background_image.putpixel((x, y), (sine_value, sine_value, sine_value, 255))



    # Return background
    return background_image