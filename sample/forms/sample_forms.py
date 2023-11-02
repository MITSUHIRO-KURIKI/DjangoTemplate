from django import forms

class SampleForm(forms.Form):
    
    sample_choices = tuple()
    selections = {
        0: 'item1', 1: 'item2', 2: 'item3',
    }
    for k, v in selections.items():
        sample_choices += ((k, str(v)),)
    single_checkbox_form = forms.BooleanField(
                    label     = 'single_checkbox_form',
                    help_text = 'サンプル help_text',
                    required  = False,
                    widget    = forms.widgets.CheckboxInput(
                        attrs = {
                            'sample_attrs': 'サンプル sample_attrs',
                        }),)
    multiple_checkbox_select_form = forms.MultipleChoiceField(
                    label     = 'multiple_checkbox_select_form',
                    help_text = 'サンプル help_text',
                    required  = False,
                    widget    = forms.widgets.CheckboxSelectMultiple(
                        attrs = {
                            'sample_attrs': 'サンプル sample_attrs',
                        }),
                    choices  = sample_choices,)
    single_select_form = forms.ChoiceField(
                    label     = 'single_select_form',
                    help_text = 'サンプル help_text',
                    required  = False,
                    widget    = forms.widgets.Select(
                        attrs = {
                            'sample_attrs': 'サンプル sample_attrs',
                        }),
                    choices  = sample_choices,)
    multiple_select_form = forms.MultipleChoiceField(
                    label     = 'multiple_select_form',
                    help_text = 'サンプル help_text',
                    required  = False,
                    widget    = forms.widgets.CheckboxSelectMultiple(
                        attrs = {
                            'sample_attrs': 'サンプル sample_attrs',
                        }),
                    choices  = sample_choices,)
    date_form = forms.DateField(
                    label     = 'date_form',
                    help_text = 'サンプル help_text',
                    required  = False,
                    widget    = forms.DateInput(
                        attrs = {
                            'sample_attrs': 'サンプル sample_attrs',
                        }),
                    input_formats = ["%Y-%m-%d"],)
    time_form = forms.TimeField(
                    label     = 'time_form',
                    help_text = 'サンプル help_text',
                    required  = False,
                    widget    = forms.TimeInput(
                        attrs = {
                            'sample_attrs': 'サンプル sample_attrs',
                        }),
                    input_formats = ["%H:%M:%S", "%H:%M:%S.%f", "%H:%M"],)
    date_time_form = forms.DateTimeField(
                    label     = 'date_time_form',
                    help_text = 'サンプル help_text',
                    required  = False,
                    widget    = forms.DateTimeInput(
                        attrs = {
                            'sample_attrs': 'サンプル sample_attrs',
                        }),
                    input_formats=[
                        "%Y-%m-%d %H:%M:%S",
                        "%Y-%m-%d %H:%M:%S.%f",
                        "%Y-%m-%d %H:%M",
                        "%Y-%m-%d",
                    ],)