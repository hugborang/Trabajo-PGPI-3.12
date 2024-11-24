from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import review, Apartment
from django.contrib.auth.decorators import login_required
from app.forms.review_form import ReviewForm
from django.shortcuts import render, get_object_or_404
from app.models.review import Review

@login_required
def create_reviews(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.user = request.user
                review.apartment = apartment
                review.save()
                messages.success(request, "Gracias por dejar tu valoración.")
                return redirect('customer_menu')
            except IntegrityError:
                messages.error(request, "Ya has dejado una valoración para este apartamento.")
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")

    else:
        form = ReviewForm()

    return render(request, 'customer/review_form.html', {'form': form, 'apartment': apartment})

@login_required
def apartment_review(request):
    
    apartments = Apartment.objects.filter(owner=request.user)  
    reviews = Review.objects.filter(apartment__in=apartments)
    
    return render(request, 'owner/review_list.html', {'reviews': reviews})
