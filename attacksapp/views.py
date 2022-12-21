from django.http import JsonResponse
from django.shortcuts import render
from django import forms
from django.views.decorators.csrf import csrf_exempt

from .models import Attack, STATUS_CHOICES


def list_attacks(request):
    context = {
    }

    print(request.POST)
    if request.method == 'POST':
        list_data = request.POST
        attack_id = list_data.get('attack_id')

        if attack_id:
            attack = Attack.objects.get(pk=attack_id)
            attack.status = STATUS_CHOICES.STOPPED
            attack.save()
            context['attacks_updated'] = [attack]
        else:
            attacks_str_ids = list_data.getlist('attacks')
            attacks_ids = [int(id) for id in attacks_str_ids]
            attacks_to_updated = Attack.objects.filter(id__in=attacks_ids)
            attacks_to_updated.update(status=STATUS_CHOICES.STOPPED)
            context['attacks_updated'] = attacks_to_updated

    attacks = Attack.objects.all()
    context = {
        'attacks': attacks,
    }
    return render(request, 'list_attacks.html', context)


class CreateAttackForm(forms.Form):
    name = forms.CharField(max_length=256)
    command = forms.CharField(widget=forms.Textarea)


def create_attack(request):
    context = {
        'form': CreateAttackForm()
    }

    if request.method == 'POST':
        create_data = request.POST
        attack = Attack.objects.create(name=create_data['name'], command=create_data['command'])
        context['attack'] = attack

    return render(request, 'create_attack.html', context)


@csrf_exempt
def attacks_api(request):
    if request.method == 'POST':
        request_data = request.POST
        attack_id = request_data.get('attack_id')
        new_status = request_data.get('status')
        try:
            attack = Attack.objects.get(pk=int(attack_id))
            attack.status = new_status
            attack.save()
            return JsonResponse({'success': True, 'attack': attack.to_json()}, status=204)
        except Attack.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Attack does not exist'}, status=404)

    get = request.GET
    print(f'get:{get}')
    attack_id = get.get('attack_id')
    attack = None

    if attack_id:
        try:
            attack = Attack.objects.get(pk=int(attack_id))
        except Attack.DoesNotExist:
            pass
    else:
        print(f'getting oldest attack')
        attack = Attack.objects.filter(status=STATUS_CHOICES.NEW).order_by('-created_at').first()

    if not attack:
        print("no attacks to run...")
        return JsonResponse({'success': False, 'error': 'No attacks available'}, status=404)

    return JsonResponse(attack.to_json(), status=200)
