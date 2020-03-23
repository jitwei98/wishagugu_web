from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Event, Gift


def test(request):
    return render(request, 'app/test.html', context={})


class EventList(ListView):
    model = Event

class EventDetail(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['is_participant'] = self.object.is_participant(user_id)
        return context

# def gift_list(request, event_id):
#     event = get_object_or_404(Event, pk=event_id)
#     gifts = Gift.objects.filter(event_id=event_id)
#
#     context = {
#         'event': event,
#         'gifts': gifts
#     }
#     return render(request, 'app/gift_list.html', context=context)

class GiftList(ListView):
    model = Gift

    def get_queryset(self):
        return Gift.objects.filter(event_id=self.kwargs['event_id'])


class GiftDetail(DetailView):
    model = Gift

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gift = self.object
        number_of_contributors = gift.contributors.count()
        if number_of_contributors == 0:
            context['price_per_pax'] = gift.amount
        else:
            context['price_per_pax'] = gift.amount / number_of_contributors

        context['is_contributor'] = self.object.is_contributor(self.request.user.id)
        return context


class GiftCreate(CreateView):
    model = Gift
    fields = ['event', 'name', 'amount', 'contributors']

    def get_initial(self):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return {
            'event': event
        }

    def get_success_url(self):
        event_id = self.get_initial().get('event').pk
        return reverse('event-detail', args=[event_id])

class GiftUpdate(UpdateView):
    model = Gift
    fields = ['amount']

    def get_success_url(self):
        event_id = self.kwargs['event_id']
        gift_id = self.kwargs['pk']
        return reverse('gift-detail', args=[event_id, gift_id])


class GiftDelete(DeleteView):
    model = Gift

    def get_success_url(self):
        event_id = self.kwargs['event_id']
        return reverse_lazy('event-detail', args=[event_id])



def withdraw(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.participants.remove(request.user)
    for gift in Gift.objects.filter(event_id=event_id):
        gift.contributors.remove(request.user)
    return redirect(reverse_lazy('event-detail', args=[event_id]))

def participate(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.participants.add(request.user)
    return redirect(reverse_lazy('event-detail', args=[event_id]))

def count_me_in(request, gift_id):
    gift = get_object_or_404(Gift, pk=gift_id)
    gift.contributors.add(request.user)
    return redirect(reverse_lazy('gift-detail', args=[gift.event.pk, gift_id]))

def count_me_out(request, gift_id):
    gift = get_object_or_404(Gift, pk=gift_id)
    gift.contributors.remove(request.user)
    return redirect(reverse_lazy('gift-detail', args=[gift.event.pk, gift_id]))
