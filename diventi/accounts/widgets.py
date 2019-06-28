from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import DiventiAvatar, DiventiCover


class DiventiAvatarSelect(forms.Select):    
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        option_attrs['data-img-alt'] = value
        if value and int(value) > 0:
            avatar = DiventiAvatar.objects.get(id=int(value))
            option_attrs['data-img-src'] = avatar.image
            option_attrs['data-img-class'] = ''
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


class DiventiCoverSelect(forms.Select):    
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        option_attrs['data-img-alt'] = value
        if value and int(value) > 0:
            avatar = DiventiCover.objects.get(id=int(value))
            option_attrs['data-img-src'] = avatar.image
            option_attrs['data-img-class'] = ''
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


class GroupedModelChoiceField(forms.ModelChoiceField):

    def set_optgroup_label(self, optgroup):
        return ""

    def get_queryset(self):
        queryset = []
        if self.queryset:
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
        if optgroup: # Staff_only = True
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