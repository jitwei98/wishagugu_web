from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import RecipientModelForm
from .models import Event, Gift, Recipient, SuggestedGift, Permalink


def test(request):
    return render(request, 'app/test.html', context={})

def home(request):
    url = reverse('recipient-list')
    return HttpResponseRedirect(url)
    # return render(request, 'app/home.html')

# ML stub for generating gift-suggestions
def generate_gift_suggestions(recipient_id):
    gifts = SuggestedGift.objects.all()
    pk_list = [g.pk for g in gifts]

    import random
    from datetime import datetime
    random.seed(datetime.now())

    filtered_pk_list = []
    for i in range(3):
        num = random.randint(0, len(pk_list)-1)
        filtered_pk_list.append(pk_list[num])

    # duplicate and save gifts
    gifts = gifts.filter(pk__in=filtered_pk_list)
    for gift in gifts:
        gift.pk = None
        gift.recipient_id = recipient_id
        gift.save()

    return gifts


def recipient_create(request):
    if request.method == 'POST':
        form = RecipientModelForm(request.POST)
        if form.is_valid():
            new_recipient = form.save()

            # ML stub for generating gift-suggestions
            generate_gift_suggestions(new_recipient.pk)


            url = reverse('gift-suggestions', kwargs={'id': new_recipient.pk})
            return HttpResponseRedirect(url)
    else:
        form = RecipientModelForm()
    context = {
        'form': form
    }
    return render(request, 'app/recipient_form.html', context=context)

class RecipientList(ListView):
    model = Recipient

def gift_suggestions(request, id):
    recipient = get_object_or_404(Recipient, pk=id)

    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        suggestion = get_object_or_404(SuggestedGift, pk=choice_id)
        suggestion.votes = suggestion.votes + 1
        suggestion.save()
        # TODO: redirect to the vote result screen

        url = reverse('voting-result', kwargs={'id': recipient.pk})
        return HttpResponseRedirect(url)

    # gift_stub = {
    #     'name': 'Mango',
    #     'price': 60,
    #     'image_url': 'https://calories-info.com/site/assets/files/1173/mango.650x0.jpg'
    # }
    # gifts_stub = [gift_stub] * 3
    # TODO: let user add suggested gifts
    gifts = SuggestedGift.objects.filter(recipient_id=id)[:3]

    try:
        permalink = Permalink.objects.get(refers_to_id=id)
    except Permalink.DoesNotExist:
        pk = Permalink.generate_permalink_pk(recipient)
        permalink = Permalink(refers_to=recipient, key=pk)
        permalink.save()
    share_url = request.build_absolute_uri(reverse('permalink', args=[permalink.key]))

    context = {
        'recipient': recipient,
        'gifts': gifts,
        'share_url': share_url
    }
    return render(request, 'app/suggestion_list.html', context=context)

# def increase_vote(request, id):
#     return

def voting_result(request: object, id: object) -> object:
    recipient = get_object_or_404(Recipient, pk=id)
    gifts = SuggestedGift.objects\
                .filter(recipient_id=id)\
                .order_by('-votes')[:3]
    # TODO: Tie breaker if same number of votes

    # TODO: Refactor to models.py
    number_of_contributors = recipient.suggestedgift_set.count()
    price_per_pax = round(gifts[0].price / number_of_contributors, 2)

    context = {
        'recipient': recipient,
        'gifts': gifts,
        'number_of_contributors': number_of_contributors,
        'price_per_pax': price_per_pax
    }
    return render(request, 'app/voting_result.html', context=context)

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


GIFT_SUGGESTIONS_STUB = [
    {
        'name': 'Exploding Kittens',
        'amount': 15.99
    },
    {
        'name': 'Wyze Cam',
        'amount': 25.98
    },
    {
        'name': 'Bluetooth Turntable',
        'amount': 41.99
    },
]

class GiftCreate(CreateView):
    model = Gift
    fields = ['event', 'name', 'amount', 'contributors']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suggestions = GIFT_SUGGESTIONS_STUB
        context['suggestions'] = suggestions
        return context

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


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def redirect_permalink(request, permalink):
    permalink_obj = get_object_or_404(Permalink, key=permalink)
    recipient_id = permalink_obj.refers_to_id
    url = reverse('gift-suggestions', args=[recipient_id])
    return redirect(url)
