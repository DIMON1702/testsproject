from django import forms


class AddTest(forms.ModelForm):
    class Meta:
        #model = User
        fields = ('avatar', 'first_name', 'last_name',
                  'email', 'bio', 'birth_date')
