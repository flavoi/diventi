from django import forms

from .models import DiventiAvatar

class DiventiAvatarSelect(forms.Select):
    
    # option_template_name = 'django/forms/widgets/select_option.html'
    # option_template_name = 'select_option.html'
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        option_attrs['data-img-alt'] = value
        if value and int(value) > 0:
            avatar = DiventiAvatar.objects.get(id=int(value))
            option_attrs['data-img-src'] = avatar.image.url             
            option_attrs['data-img-class'] = 'img-responsive' 
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)                
        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
        }