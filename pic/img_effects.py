import base64
import cStringIO
import os

from PIL import (
    Image, ImageFilter,
    ImageOps, ImageEnhance, ImageDraw,
    ImageFont
)

class ImageEffects:
    filters = {
        'blur': ImageFilter.BLUR,
        'contour': ImageFilter.CONTOUR,
        'detail': ImageFilter.DETAIL,
        'edge_enhance': ImageFilter.EDGE_ENHANCE,
        'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE,
        'emboss': ImageFilter.EMBOSS,
        'find_edges': ImageFilter.FIND_EDGES,
        'smooth': ImageFilter.SMOOTH,
        'smooth_more': ImageFilter.SMOOTH_MORE,
        'sharpen': ImageFilter.SHARPEN,
    }
    enhancements = ['Brightness', 'Color', 'Contrast', 'Sharpness']
    image_format = 'JPEG'
    max_enhance = 2.0
    effects_applied = []

    def __init__(self, path):
        self.path = path
        self.font = None
        try:
            self.image = Image.open(path)
        except:
            raise ValueError('Image not found in this path')

    def effect_applied(self, effect_name):
        self.effects_applied.append(effect_name)

    def convert(self, mode="RGB"):
        self.image = self.image.convert(mode)

    def black_and_white(self):
        """ Applies black and white effect"""
        self.convert('L')
        self.effects_applied('black_and_white')

    def grayscale(self):
        """ Applies grayscale effect"""
        self.image = ImageOps.grayscale(self.image)
        self.effects_applied('grayscale')

    def invert(self):
        """ Negates the image. """
        self.convert()
        self.image = ImageOps.invert(self.image)
        self.effects_applied('invert')

    def equalize(self):
        """ Equalize the image histogram. """
        self.image = ImageOps.equalize(self.image)
        self.effects_applied('equalize')

    def filter(self, filter_type):
        """ Applies elected filters. """
        self.image = self.image.filter(self.filters[filter_type])
        self.effects_applied(self.filters[filter_type])

    def enhance(self, enhancement_type, value):
        """
        Used to enhance image brightness,
        color, contrast and sharpness.
        """
        enhancer = getattr(ImageEnhance, enhancement_type)
        if enhancer:
            enhance_value = (value / 100) * self.max_enhance
            enhanced = enhancer(self.image)
            self.image = enhanced.enhance(enhance_value)
            self.effects_applied(enhancement_type)

    def quantize(self, value=256):
        """
        Convert the image to 'P' mode with the
        specified number of colors.
        """
        actual_value = float(value) / 100 * 256
        self.image = self.image.quantize(int(actual_value))
        self.image = self.image.convert('RGB')
        self.effects_applied('quantize')

    def gaussian_blur(self, radius):
        """ Gaussian blur filter. """
        actual_value = float(radius)/100 * 20
        self.image = self.image.filter(
            ImageFilter.GaussianBlur(int(actual_value)))
        self.effects_applied('gaussian_blur')

    def contrast(self, cutoff=0):
        """ Normalize image contrast. """
        self.convert()
        actual_value = float(cutoff)/100 * 50
        self.image = ImageOps.autocontrast(self.image, int(actual_value))
        self.effects_applied('equalize')

    def posterize(self, bit=1):
        """ Reduce the number of bits for each color channel. """
        self.convert()
        actual_value = float(bit)/100 * 8
        self.image = ImageOps.posterize(self.image, int(actual_value))
        self.effects_applied('posterize')

    def unsharp_mask(self, radius):
        """ Unsharp mask filter. """
        self.image = self.image.filter(ImageFilter.UnsharpMask(int(radius)))
        self.effects_applied('unsharp_mask')

    def solarize(self, threshold=128):
        """ Invert all pixel values above a threshold """
        self.convert()
        actual_value = float(threshold) / 100 * 256
        self.image = ImageOps.solarize(self.image, int(actual_value))
        self.effects_applied('solarize')

    def remove_border(self, border_size=0):
        """ Remove image border. """
        actual_value = float(border_size) / 100 * 200
        self.image = ImageOps.crop(self.image, int(actual_value))
        self.effects_applied('zoom')

    def rotate(self, value):
        """ Rotates image in a given angle. """
        actual_value = float(value)/100 * 360
        self.image = self.image.rotate(int(actual_value))
        self.effects_applied('rotate')

    def colorize(self, black="#000", white="#fff"):
        """ applies colors to black and white image """
        self.black_and_white()
        self.image = ImageOps.colorize(self.image, black, white)
        self.effects_applied('colorize')

    def expand(self, border=10, fill="#ff0"):
        """ Add border to image """
        self.image = ImageOps.expand(self.image, border=border, fill=fill)
        self.effects_applied('border')

    def vertical_flip(self):
        """ Flip the image vertically (top to bottom). """
        self.image = ImageOps.flip(self.image)
        self.effects_applied('vertical_flip')

    def mirror(self):
        """ Flip image horizontally (left to right). """
        self.image = ImageOps.mirror(self.image)
        self.effects_applied('mirror')

    def crop(self, border=15):
        """ Reduces image size. """
        self.image = ImageOps.crop(self.image, border=border)
        self.effects_applied('crop')

    def set_font(self, font_size=100, font_name="TRIBTWO.ttf"):
        """ Sets the font to be used for text drawing """
        fonts_path = os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.dirname(__file__))), 'static/fonts')
        font_file =  fonts_path + '/' + font_name
        self.font = ImageFont.truetype(font_file, font_size)

    def text(self, text, x, y, fill=(255, 255, 255), font_size=100, font_name="TRIBTWO.ttf"):
        """ Write text on an image """
        draw = ImageDraw.Draw(self.image)
        if not self.font:
            self.set_font(font_size, font_name)
        draw.text((x, y), text, font=self.font, fill=fill)
        del draw
        self.effect_applied('text')

    def preview(self):
        """ Returns a base64 converted image """
        print('preview')
        buffered = cStringIO.StringIO()
        self.image.save(buffered, format=self.image_format)
        return base64.b64encode(buffered.getvalue())

    def save(self):
        """ Saves modified image """
        path = self.path.replace('main', 'edited')
        edit_path = os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.dirname(__file__))), 'media/edited')
        if not os.path.exists(edit_path):
            os.makedirs(edit_path)
        self.image.save(path, format=self.image_format)

    def download(self, title):
        response = HttpResponse(content_type="image/jpg")
        self.image.save(response, 'JPEG')
        response['Content-Disposition'] = 'attachment; filename="{}.jpg"'.format(title)
        return response