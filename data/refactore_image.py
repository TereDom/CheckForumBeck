from PIL import Image


def refactor_image(image_name):
    """"""
    image = Image.open(image_name)
    pixels = image.load()
    x, y = image.size
    center = x // 2, y // 2
    x, y = x if x <= y else y, x if x <= y else y
    new_image = Image.new("RGB", (x, y), (0, 0, 0))
    new_pixels = new_image.load()

    x0 = center[0] - x // 2
    y0 = center[1] - y // 2
    x1 = center[0] + x // 2
    y1 = center[1] + y // 2

    for i in range(x0, x1 + 1):
        for j in range(y0, y1 + 1):
            new_pixels[i - x0 + 1, j - y0 + 1] = pixels[i, j]

    new_image.save(image_name)
