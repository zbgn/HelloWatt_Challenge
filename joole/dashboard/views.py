from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import ClientForm
from .models import Conso_eur, Conso_watt


class ClientFormView(View):
    def get(self, request):
        return render(request, 'dashboard/accueil.html')

    def post(self, request):
        form = ClientForm(request.POST)

        if form.is_valid():
            client_id = form.cleaned_data['client']
            return redirect('dashboard:results', client_id=client_id)


def results(request, client_id):
    conso_euro = []
    conso_watt = []
    annual_costs = [0, 0]
    is_elec_heating = True
    dysfunction_detected = False

    for euro in list(Conso_eur.objects.filter(client_id=client_id).values()):
        x = [euro['janvier'], euro['fevrier'], euro['mars'], euro['avril'], euro['mai'], euro['juin'],
             euro['juillet'], euro['aout'], euro['septembre'], euro['octobre'], euro['novembre'], euro['decembre']]
        conso_euro.extend(x)
    for watt in list(Conso_watt.objects.filter(client_id=client_id).values()):
        x = [watt['janvier'], watt['fevrier'], watt['mars'], watt['avril'], watt['mai'], watt['juin'],
             watt['juillet'], watt['aout'], watt['septembre'], watt['octobre'], watt['novembre'], watt['decembre']]
        conso_watt.extend(x)
    annual_costs = [sum(conso_euro[:12]), sum(conso_euro[12:])]
    winter = (conso_watt[0] + conso_watt[1] + conso_watt[11] +
              conso_watt[12] + conso_watt[13] + conso_watt[-1]) / 6
    summer = (sum(conso_watt[2:11]) + sum(conso_watt[14:23])) / 18
    is_elec_heating = (winter / summer > 1.5)
    dysfunction_detected = (
        annual_costs[0] / annual_costs[1] > 1.5) or (annual_costs[1] / annual_costs[0] > 1.5)
    if dysfunction_detected:
        messages.add_message(
            request, messages.WARNING, 'Un dysfonctionnement sur votre installation éléctrique a été détecté.')
    context = {
        "conso_euro": conso_euro,
        "conso_watt": conso_watt,
        "annual_costs": annual_costs,
        "is_elec_heating": is_elec_heating,
        "dysfunction_detected": dysfunction_detected
    }
    return render(request, 'dashboard/results.html', context)
