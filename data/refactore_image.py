from PIL import Image


def refactor_image(image_name):
    """"""
    image = Image.open(image_name)
    x, y = image.size
    center = x // 2, y // 2
    x, y = x if x <= y else y, x if x <= y else y
    area = center[0] - x // 2, center[1] - y // 2, center[0] + x // 2, center[1] + y // 2
    image = image.crop(area)
    image.save(image_name)
