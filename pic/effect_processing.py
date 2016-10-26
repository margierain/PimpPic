from img_effects import *
import json

class ImageProcessor:

    def __init__(self, photo):
        self.image = photo.image
        self.img_effects = ImageEffects(photo.image.path)

    def process(self, effect_obj):
        effect_obj = json.loads(effect_obj)
        for effect_type in effect_obj:
            effect_type = str(effect_type)
            effect_data = effect_obj[effect_type]
            if ("enhance" or "effect" in effect_type):
                editor_method = getattr(self, effect_type)
                if editor_method:
                       editor_method(effect_data)
            effect_data = str(effect_data)
            if(effect_data) and ("enhance" not in effect_type):
                try:
                    editor_method = getattr(self, effect_type)
                    if editor_method:
                       editor_method(effect_data)
                except:
                    pass

    def preview(self):
        return self.img_effects.preview()

    def applied_effects(self):
        return self.img_effects.effect_applied

    def save(self):
        self.img_effects.save()
        return self.image.url.replace('original', 'edited')

    def enhance(self, effect_data):
        effect = str(effect_data[0])
        self.img_effects.enhance(
            effect, float(str(effect_data[1])))


    def filter(self, effect_data):
        self.img_effects.filter(effect_data)

    def transform(self, effect_data):
        effect = getattr(self.img_effects, effect_data)
        if effect:
            effect()

    def effect(self, effect_data):
        effect = str(effect_data[0])
        print(effect)
        apply = getattr(self.img_effects, effect)
        apply(float(str(effect_data[1])))