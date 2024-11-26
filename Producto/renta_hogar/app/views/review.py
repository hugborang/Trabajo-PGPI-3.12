from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import review, Apartment
from django.contrib.auth.decorators import login_required
from app.forms.review_form import ReviewForm
from django.shortcuts import render
from app.models.review import Review
from django.utils import timezone
from app.utils.decorator import requires_role

@login_required
def create_reviews(request, apartment_id):
    try:
        apartment = Apartment.objects.get(id=apartment_id)
    except Apartment.DoesNotExist:
        return render(request, '404.html', status=404)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request=request, apartment=apartment)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.apartment = apartment
            review.save()
            return redirect('customer_menu')

    else:
        form = ReviewForm(request=request)

    return render(request, 'customer/review_form.html', {'form': form, 'apartment': apartment})

@login_required
@requires_role('owner')
def apartment_review(request):
    apartments = Apartment.objects.filter(owner=request.user)
    
    apartment_reviews = [
        {
            'apartment': apartment,
            'reviews': Review.objects.filter(apartment=apartment)
        }
        for apartment in apartments
    ]
    
    return render(request, 'owner/review_list.html', {'apartment_reviews': apartment_reviews})
