import secrets

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from payments.forms import DischargeForm
from payments.models import Discharge

ROOM_RATE_LABELS = {
    'bed': 'Bed accommodation',
    'nursing': 'Nursing care',
    'doc': 'Physician services',
    'misc': 'Miscellaneous hospital charges',
}

room_rates = {
    'COMMON WARD': {'bed': 250, 'nursing': 300, 'doc': 250, 'misc': 100},
    'SEMI-PRIVATE': {'bed': 500, 'nursing': 400, 'doc': 350, 'misc': 150},
    'PRIVATE AC': {'bed': 1200, 'nursing': 600, 'doc': 500, 'misc': 200},
    'PRIVATE NON-AC': {'bed': 800, 'nursing': 500, 'doc': 450, 'misc': 150},
    'DELUXE': {'bed': 2500, 'nursing': 1000, 'doc': 800, 'misc': 500},
}

GST_PERCENT = 18

# Simulated UPI / wallet / card options (no real gateway).
PAYMENT_METHODS = {
    'gpay': {'label': 'Google Pay', 'icon': 'google'},
    'phonepe': {'label': 'PhonePe', 'icon': 'phone'},
    'paytm': {'label': 'Paytm', 'icon': 'wallet2'},
    'amazonpay': {'label': 'Amazon Pay', 'icon': 'bag-check'},
    'upi': {'label': 'Other UPI app', 'icon': 'qr-code'},
    'card': {'label': 'Credit / Debit card', 'icon': 'credit-card'},
    'netbanking': {'label': 'Net banking', 'icon': 'bank'},
}

def _payment_session_key(bill_id):
    return f'payment_receipt_{bill_id}'


def _billing_breakdown(bill):
    """Return line_items, subtotal, gst_amount, grand_total for a Discharge instance."""
    components = room_rates.get(bill.room_type) or {}
    days = bill.total_days
    line_items = []
    for key, rate_per_day in components.items():
        label = ROOM_RATE_LABELS.get(key, key.replace('_', ' ').title())
        line_total = rate_per_day * days
        line_items.append({
            'description': label,
            'rate_per_day': rate_per_day,
            'days': days,
            'line_total': line_total,
        })
    billing_subtotal = sum(row['line_total'] for row in line_items)
    gst_amount = round(billing_subtotal * GST_PERCENT / 100)
    grand_total = billing_subtotal + gst_amount
    return line_items, billing_subtotal, gst_amount, grand_total


def Discharges(request):
    if request.method == 'POST':
        forms = DischargeForm(request.POST)
        if forms.is_valid():
            obj = forms.save()
            return redirect('finalbill', id=obj.id)
    else:
        forms = DischargeForm()
    return render(request, 'payments/discharge.html', {'forms': forms})


def finalbill(request, id):
    bill = get_object_or_404(
        Discharge.objects.select_related('Patient_name', 'Patient_name__user', 'doctor_name', 'treatment_name'),
        id=id,
    )
    line_items, billing_subtotal, gst_amount, grand_total = _billing_breakdown(bill)
    return render(request, 'payments/finalbill.html', {
        'bill': bill,
        'line_items': line_items,
        'billing_subtotal': billing_subtotal,
        'gst_percent': GST_PERCENT,
        'gst_amount': gst_amount,
        'grand_total': grand_total,
        'total_price': grand_total,
    })


def payment_checkout(request, id):
    bill = get_object_or_404(
        Discharge.objects.select_related('Patient_name', 'Patient_name__user', 'doctor_name', 'treatment_name'),
        id=id,
    )
    line_items, billing_subtotal, gst_amount, grand_total = _billing_breakdown(bill)

    if request.method == 'POST':
        method_key = request.POST.get('payment_method', '').strip()
        if method_key not in PAYMENT_METHODS:
            return render(request, 'payments/payment_checkout.html', {
                'bill': bill,
                'line_items': line_items,
                'billing_subtotal': billing_subtotal,
                'gst_percent': GST_PERCENT,
                'gst_amount': gst_amount,
                'grand_total': grand_total,
                'payment_methods': PAYMENT_METHODS,
                'payment_error': 'Please choose a valid payment option.',
            })
        method_info = PAYMENT_METHODS[method_key]
        payment_id = f"CP-{secrets.token_hex(4).upper()}-{secrets.token_hex(3).upper()}"
        receipt = {
            'payment_id': payment_id,
            'method_key': method_key,
            'method_label': method_info['label'],
            'amount_paid': grand_total,
            'billing_subtotal': billing_subtotal,
            'gst_percent': GST_PERCENT,
            'gst_amount': gst_amount,
            'patient_username': bill.Patient_name.user.username,
            'patient_display': bill.Patient_name.user.get_full_name() or bill.Patient_name.user.username,
            'bill_id': bill.id,
            'doctor_name': bill.doctor_name.name,
            'treatment': bill.treatment_name.treatment_name,
            'room_type': bill.get_room_type_display(),
            'paid_at': timezone.now().isoformat(),
            'paid_at_display': timezone.localtime(timezone.now()).strftime('%d %b %Y, %I:%M %p'),
        }
        request.session[_payment_session_key(bill.id)] = receipt
        return redirect('payment_success', id=bill.id)

    return render(request, 'payments/payment_checkout.html', {
        'bill': bill,
        'line_items': line_items,
        'billing_subtotal': billing_subtotal,
        'gst_percent': GST_PERCENT,
        'gst_amount': gst_amount,
        'grand_total': grand_total,
        'payment_methods': PAYMENT_METHODS,
    })


def payment_success(request, id):
    key = _payment_session_key(id)
    receipt = request.session.pop(key, None)
    if not receipt:
        return redirect('payment_checkout', id=id)
    return render(request, 'payments/payment_success.html', {'receipt': receipt})
