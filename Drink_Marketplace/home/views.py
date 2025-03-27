from django.shortcuts import render, get_object_or_404

# Create your views here.
def Get_home(request):
    return render(request,'home/home.html')  # Truyền vào template