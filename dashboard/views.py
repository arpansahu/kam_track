from django.shortcuts import render
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from lead.models import Lead
from interaction.models import Interaction

@login_required
def dashboard_view(request):
    user = request.user

    # Check if the logged-in user is a Key Account Manager (KAM)
    if user.role != 'kam':
        return render(request, 'dashboard/no_account.html', {'message': 'You are not assigned as a Key Account Manager.'})

    # Pending tasks for today or future (uncompleted)
    # pending_tasks = Task.objects.filter(
    #     lead__assigned_kam=user, completed=False, due_date__gte=now().date()
    # ).order_by('due_date')

    # Recent interactions from the past 7 days
    recent_interactions = Interaction.objects.filter(
        lead__assigned_kam=user, interaction_date__gte=now() - timedelta(days=7)
    ).order_by('-interaction_date')

    # Performance overview
    well_performing_leads = Lead.objects.filter(
        interactions__interaction_type='order', interactions__interaction_date__gte=now() - timedelta(days=30)
    ).distinct()

    underperforming_leads = Lead.objects.exclude(
        interactions__interaction_type='order', interactions__interaction_date__gte=now() - timedelta(days=30)
    ).distinct()

    context = {
        'pending_tasks': [],
        'recent_interactions': recent_interactions,
        'well_performing_leads': well_performing_leads,
        'underperforming_leads': underperforming_leads,
    }
    return render(request, 'dashboard/home.html', context)
