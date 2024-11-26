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
        # Pasar request y apartment al formulario
        form = ReviewForm(request.POST, request=request, apartment=apartment)
        if form.is_valid():
            # Crear la reseña si el formulario es válido
            review = form.save(commit=False)
            review.user = request.user
            review.apartment = apartment
            review.save()
            messages.success(request, "Gracias por dejar tu valoración.")
            return redirect('customer_menu')  # Ajusta esta redirección según sea necesario
        else:
            messages.error(request, "Solo puedes dejar una valoracion y debe ser despues de tu haber estancia.")
    else:
        # Crear un formulario vacío
        form = ReviewForm(request=request, apartment=apartment)

    return render(request, 'customer/review_form.html', {'form': form, 'apartment': apartment})


@login_required
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
