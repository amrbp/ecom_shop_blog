from django.shortcuts import render, redirect
from .models import Post,Like
from users.models import Profile
from  .forms import PostModelForm, CommentModelForm
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import *



def post_comment_list_view(request):
    qs = Post.objects.all().order_by('-created')
    profile = Profile.objects.get(user=request.user)
    categories = Category.objects.all()
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_add =False
    profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST:
        print(request.user)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_add = True

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {
        'qs': qs,
        'profile':profile,
        'p_form':p_form,
        'c_form':c_form,
        'post_add':post_add,
        'items': items, 
        'order': order, 
        'cartItems': cartItems,
        'categories': categories,
    }

    return render(request,'blogs/view_blog.htm',context)


def post_comment_create_and_list_view(request,pk):
    qs = Post.objects.filter(id=pk)
    profile = Profile.objects.get(user=request.user)
    categories = Category.objects.all()
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_add =False
    profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST:
        print(request.user)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_add = True

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {
        'qs': qs,
        'profile':profile,
        'p_form':p_form,
        'c_form':c_form,
        'post_add':post_add,
        'items': items, 
        'order': order, 
        'cartItems': cartItems,
        'categories': categories,
    }

    return render(request,'blogs/blog_detail.htm',context)



def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()


    return redirect('blogs:main-detail')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blogs/confirm_del.htm'
    success_url = reverse_lazy('blogs:main-post-view')

    def get_object(self , *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'your need to be the author of the post in order to delete')
        return obj
    

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'blogs/update.htm'
    success_url = reverse_lazy('blogs:main-post-view')

    def form_valid(self,form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None,"You need to be the author of the post in order to update it")
            return super().form_invalid(form)

