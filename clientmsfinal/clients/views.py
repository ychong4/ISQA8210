from django.contrib.auth.mixins import LoginRequiredMixin #New
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic import ListView, DetailView
from .models import models
from .models import Client, Comment
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

class ClientListView(LoginRequiredMixin,ListView):
    model = Client
    template_name = 'client_list.html'

class ClientDetailView(LoginRequiredMixin,DetailView):
    model = Client
    template_name = 'client_detail.html'
    login_url = 'login'

class ClientUpdateView(LoginRequiredMixin,UpdateView):
    model = Client
    fields = ('name', 'notes', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone', 'acct_number')
    template_name = 'client_edit.html'

class ClientDeleteView(LoginRequiredMixin,DeleteView):
    model = Client
    template_name = 'client_delete.html'
    success_url = reverse_lazy('client_list')

class ClientCreateView(LoginRequiredMixin,CreateView):
    model = Client
    template_name = 'client_new.html'
    fields = ('name', 'notes', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone', 'acct_number')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    template_name = 'comment_new.html'
    fields = ('client','comment', 'author')
    success_url = reverse_lazy('client_list')

    def add_comment_to_post(request, pk):
        post = get_object_or_404(Client, pk=pk)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('client_list', pk=Client.pk)
        else:
            form = CommentForm()
        return render(request, 'client_list', {'form': form})

