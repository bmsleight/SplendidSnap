from django.shortcuts import render
from .models import Splendid
from .forms import SplendidForm
from django.shortcuts import redirect

# Create your views here.

def pack_list(request):
    packs = Splendid.objects.all()
    return render(request, 'appsplendid/pack_list.html', {'packs': packs})

def pack_new(request):
    if request.method == "POST":
        form = SplendidForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('appsplendid.views.pack_list')
    else:
        form = SplendidForm()
    return render(request, 'appsplendid/pack_edit.html', {'form': form})
