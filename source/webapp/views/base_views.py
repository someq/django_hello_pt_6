from django.db.models import Q
from django.views.generic import View, TemplateView, \
    ListView as DjangoListView
from django.shortcuts import render, redirect, get_object_or_404

from webapp.forms import SimpleSearchForm


class FormView(View):
    form_class = None
    template_name = None
    redirect_url = ''

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)

    def get_redirect_url(self):
        return self.redirect_url

    def get_context_data(self, **kwargs):
        return kwargs


class ListView(TemplateView):
    model = None
    context_key = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_key] = self.get_queryset()
        return context

    def get_queryset(self):
        return self.model.objects.all()


class DetailView(TemplateView):
    context_key = 'object'
    model = None
    key_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_key] = self.get_object()
        return context

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)


class CreateView(View):
    form_class = None
    template_name = None
    model = None
    redirect_url = None

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        context = {'form': form}
        return render(self.request, self.template_name, context)

    def get_redirect_url(self):
        return self.redirect_url


class SearchView(DjangoListView):
    search_form_class = SimpleSearchForm
    search_form_field = 'search'
    search_fields = []

    def get(self, request, *args, **kwargs):
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value(self.search_form)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = self.search_form
        context['search_value'] = self.search_value
        return context

    def get_queryset(self):
        data = super().get_queryset()
        query = self.get_query(self.search_value)
        data = data.filter(query)
        return data

    def get_search_form(self):
        return self.search_form_class(data=self.request.GET)

    def get_search_value(self, form):
        search_value = None
        if form.is_valid():
            search_value = form.cleaned_data.get(self.search_form_field, None)
        return search_value

    def get_query(self, search_value):
        query = Q()
        if search_value:
            for field in self.search_fields:
                kwargs = {field: search_value}
                query = query | Q(**kwargs)
        return query
