from django import forms

class AnalysisForm(forms.Form):
    startdate = forms.DateField(label='시작기간')
    enddate = forms.DateField(label='종료기간')
    analysis_type = forms.CharField(label='분석타입', max_length=8)