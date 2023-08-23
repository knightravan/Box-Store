from rest_framework import generics, permissions, status, filters
from rest_framework.permissions import IsAdminUser
from .models import box
from django.db.models import F
from .serializers import boxseria
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import signupform, Loginform,PostForm

# Custom permission to allow staff members only
class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

class BoxList(generics.ListAPIView):
    queryset = box.objects.all()
    serializer_class = boxseria
    permission_classes = [permissions.IsAuthenticated]



class BoxDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = box.objects.all()
    serializer_class = boxseria
    permission_classes = [IsStaffOrReadOnly,IsAdminUser]

class MyBoxList(generics.ListCreateAPIView):
    serializer_class = boxseria
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        queryset = box.objects.filter(creator=self.request.user)

        length_more_than = self.request.query_params.get('length_more_than')
        length_less_than = self.request.query_params.get('length_less_than')
        breadth_more_than = self.request.query_params.get('breadth_more_than')
        breadth_less_than = self.request.query_params.get('breadth_less_than')
        height_more_than = self.request.query_params.get('height_more_than')
        height_less_than = self.request.query_params.get('height_less_than')
        area_more_than = self.request.query_params.get('area_more_than')
        area_less_than = self.request.query_params.get('area_less_than')
        volume_more_than = self.request.query_params.get('volume_more_than')
        volume_less_than = self.request.query_params.get('volume_less_than')

        if length_more_than:
            queryset = queryset.filter(length__gt=length_more_than)
        if length_less_than:
            queryset = queryset.filter(length__lt=length_less_than)
        if breadth_more_than:
            queryset = queryset.filter(length__gt=breadth_more_than)
        if breadth_less_than:
            queryset = queryset.filter(length__lt=breadth_less_than)
        if height_more_than:
            queryset = queryset.filter(length__gt=height_more_than)
        if height_less_than:
            queryset = queryset.filter(length__lt=height_less_than)
        if area_more_than:
            queryset = queryset.annotate(area=F('length')*F('breadth')).filter(area__gt=area_more_than)
        if area_less_than:
            queryset = queryset.annotate(area=F('length')*F('breadth')).filter(area__lt=area_less_than)
        if volume_more_than:
            queryset = queryset.annotate(volume=F('length')*F('breadth')*F('height')).filter(volume__gt=volume_more_than)
        if volume_less_than:
            queryset = queryset.annotate(volume=F('length')*F('breadth')*F('height')).filter(volume__lt=volume_less_than)

        return queryset


def index(request):
    boxes = box.objects.all()
    return render(request, 'interface/index.html', {'boxes': boxes})

def dashboard(request): 
    if request.user.is_authenticated:
        username=request.user
        posts= box.objects.filter(creator=request.user)
        return render(request, 'interface/dashboard.html',{'posts':posts,'user':username })
    else:
        return HttpResponseRedirect('/login/')

def updatepost(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi=box.objects.get(pk=id)
            form=PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, "Data Updated !!!")
                return HttpResponseRedirect('/dashboard/')
        else:
            pi=box.objects.get(pk=id)
            form=PostForm(instance=pi)

        return render(request, 'interface/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def deletepost(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=box.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
        else:
            pass
    else:
        return HttpResponseRedirect('/login/')



def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.creator = request.user
                instance.save()
                form=PostForm()
        else:
            form = PostForm()

        return render(request, 'interface/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form = Loginform(request=request, data= request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request, "Logged in Successfully !!!")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=Loginform()
        return render(request, 'interface/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')


def signup(request):
    if request.method == "POST":
        form = signupform(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulation Auther !!")
            form.save()
    else:
        form=signupform()
    return render(request, 'interface/signup.html' , {'form':form} )

def user_logout(request):
    logout(request)
    messages.success(request, "Logout Successful !!!")
    return HttpResponseRedirect('/login/')

