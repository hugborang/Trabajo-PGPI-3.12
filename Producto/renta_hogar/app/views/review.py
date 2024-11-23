from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from app.models import Apartment, Reservation
from app.forms.review_form import ReviewForm
from app.models.review import Review


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "customer/review_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario tiene una reserva para el apartamento
        self.apartment = Apartment.objects.get(pk=kwargs['apartment_id'])
        self.reservation = Reservation.objects.filter(
            apartment=self.apartment,
            cust=request.user
        ).last()  # Obtén la última reserva del usuario para este apartamento

        if not self.reservation:
            return redirect('access_denied')  # Redirige si no hay reservas válidas

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Verificar si la reserva ha finalizado
        if self.reservation.end_date > timezone.now().date():
            messages.error(self.request, "La reserva debe haber finalizado para dejar una valoración.")
            return self.form_invalid(form)  # Mantener al usuario en la misma página
        
        if Review.objects.filter(user=self.request.user, apartment=self.apartment).exists():
            messages.error(self.request, "Ya has dejado una valoración para este apartamento.")  # Agregar mensaje de error
            return self.form_invalid(form)  

        # Asociar la valoración al usuario y al apartamento
        form.instance.user = self.request.user
        form.instance.apartment = self.apartment
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al home del usuario después de crear la valoración
        return reverse_lazy('customer_menu')
