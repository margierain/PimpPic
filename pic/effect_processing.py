from img_effects import ImageEffects
import itertools
import json
applied = []
class ImageProcessor:

    def __init__(self, photo):
        self.image = photo.image
        try:
            photo.edited_image.path
            self.img_effects = ImageEffects(photo.edited_image.path)
        except ValueError:
            self.img_effects = ImageEffects(photo.image.path)

        

    def process(self, effect_obj):
        effect_obj = json.loads(effect_obj)
        for effect_type in effect_obj:
            effect_type = str(effect_type)
            effect_data = effect_obj[effect_type]
            self.applied_effects({effect_type:effect_data})
            for i in applied:
                if ("enhance" in effect_type or "effect" in effect_type):
                    editor_method = getattr(self, effect_type)
                    if editor_method:
                        editor_method(effect_data)
                else:        
                    effect_data = str(effect_data)
                    if(effect_data) and ("enhance" not in effect_type):
                        try:
                            editor_method = getattr(self, effect_type)
                            if editor_method:
                               editor_method(effect_data)
                        except:
                            pass
            self.img_effects.save()               

    def preview(self):
        return self.img_effects.preview()

    def applied_effects(self, effect_name):
        self.img_effects.save()
        if effect_name != applied:
            applied.append(effect_name)
        return self.img_effects.effects_applied

    def save(self):
        return self.image.url.replace('original', 'edited')

    def enhance(self, effect_data):
        list = []
        for i in effect_data: 
            list.append(str(i))
        enhancement = dict(itertools.izip_longest(*[iter(list)] * 2, fillvalue=""))
        for effect, values in enhancement.iteritems():
            self.img_effects.enhance(
                effect, float(values))
       


    def filter(self, effect_data):
        self.img_effects.filter(effect_data)

    def transform(self, effect_data):
        effect = getattr(self.img_effects, effect_data)
        if effect:
            effect()

    def effect(self, effect_data):
        effect = str(effect_data[0])
        apply = getattr(self.img_effects, effect)
        apply(float(str(effect_data[1])))