from django.shortcuts import render

def planning_overview(request):
    return render(request, 'planning/overview.html')