from django import forms



class CartAddForm(forms.Form):

    quantity = forms.IntegerField(min_value=1, max_value=9)


class CouponForm(forms.Form):

    code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'style': 'max-width: 300px;',
        }),
        label="Coupon Code"
    )