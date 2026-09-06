from django import forms
from django.utils.translation import gettext_lazy as _

class DiventiAvatarSelect(forms.Select):    
    image_map = {}

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        
        if value:
            val_id = str(value)
            # Recupera l'URL dalla mappa pre-caricata in memoria nel form
            img_src = self.image_map.get(val_id) or self.image_map.get(int(value) if str(value).isdigit() else None)
            if img_src:
                option['attrs']['data-img-src'] = img_src
                option['attrs']['data-img-class'] = 'avatar_image'
            
        option['attrs']['data-img-alt'] = value
        return option


class DiventiCoverSelect(forms.Select):    
    image_map = {}

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        
        if value:
            val_id = str(value)
            img_src = self.image_map.get(val_id) or self.image_map.get(int(value) if str(value).isdigit() else None)
            if img_src:
                option['attrs']['data-img-src'] = img_src
                option['attrs']['data-img-class'] = 'cover_image'
            
        option['attrs']['data-img-alt'] = value
        return option


class GroupedModelChoiceField(forms.ModelChoiceField):

    def set_optgroup_label(self, optgroup):
        return ""

    def get_queryset(self):
        queryset = []
        if self.queryset is not None:
            queryset = self.queryset        
        return queryset

    def optgroup_from_instance(self, obj):
        return ""

    def __choice_from_instance__(self, obj):
        return (obj.id, self.label_from_instance(obj))

    def _get_choices(self):
        if self.get_queryset():          
            all_choices = []
            if self.empty_label:
                current_optgroup = ""
                current_optgroup_choices = [("", self.empty_label)]
            else:
                current_optgroup = self.optgroup_from_instance(self.get_queryset()[0])
                current_optgroup_choices = []

            for item in self.get_queryset():
                optgroup_from_instance = self.optgroup_from_instance(item)
                optgroup_from_instance = self.set_optgroup_label(optgroup=optgroup_from_instance)
                if current_optgroup != optgroup_from_instance:
                    all_choices.append((current_optgroup, current_optgroup_choices))
                    current_optgroup_choices = []
                    current_optgroup = optgroup_from_instance
                current_optgroup_choices.append(self.__choice_from_instance__(item))

            all_choices.append((current_optgroup, current_optgroup_choices))
            return all_choices
        else:
            return []

    choices = property(_get_choices, forms.ChoiceField._set_choices)


class DiventiAvatarChoiceField(GroupedModelChoiceField):

    def optgroup_from_instance(self, obj):
        group = False
        if hasattr(obj, 'staff_only'):
            group = obj.staff_only
        return group

    def set_optgroup_label(self, optgroup):
        optgroup_name = _("User avatars")
        if optgroup: # Staff_only = True
            optgroup_name = _("Staff avatars")
        return optgroup_name


class DiventiCoverChoiceField(GroupedModelChoiceField):

    def optgroup_from_instance(self, obj):
        group = False
        if hasattr(obj, 'staff_only'):
            group = obj.staff_only
        return group

    def set_optgroup_label(self, optgroup):
        optgroup_name = _("User covers")        
        return optgroup_name