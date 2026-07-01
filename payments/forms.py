from django import forms
from payments.models import Discharge


class DischargeForm(forms.ModelForm):
    """Admission / discharge dates drive total_days (inclusive count of calendar days)."""

    class Meta:
        model = Discharge
        fields = '__all__'
        widgets = {
            'date_of_addm': forms.DateInput(
                attrs={'type': 'date', 'class': 'cf-date-admit'},
            ),
            'date_of_discharge': forms.DateInput(
                attrs={'type': 'date', 'class': 'cf-date-discharge'},
            ),
            'total_days': forms.NumberInput(
                attrs={
                    'readonly': 'readonly',
                    'class': 'cf-total-days',
                    'min': '1',
                },
            ),
        }
        help_texts = {
            'total_days': 'Computed automatically from admission and discharge (inclusive of both dates).',
        }

    def clean(self):
        cleaned_data = super().clean()
        adm = cleaned_data.get('date_of_addm')
        dis = cleaned_data.get('date_of_discharge')
        if adm and dis:
            if dis < adm:
                self.add_error(
                    'date_of_discharge',
                    'Discharge date cannot be before admission.',
                )
            else:
                # Inclusive billing: same calendar day counts as one day.
                cleaned_data['total_days'] = (dis - adm).days + 1
        return cleaned_data
