from PIL import Image


def refactor_image(image_name):
    """"""
    image = Image.open(image_name)
    pixels = image.load()
    x, y = image.size
    center = x // 2, y // 2
    x, y = x if x <= y else y, x if x <= y else y

    x0 = center[0] - x // 2
    y0 = center[1] - y // 2
    x1 = center[0] + x // 2
    y1 = center[1] + y // 2

    print(x0, y0, x1, y1)
