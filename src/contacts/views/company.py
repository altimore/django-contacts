from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404, HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from contacts.models import Company
from contacts.forms import CompanyCreateForm, CompanyUpdateForm, PhoneNumberFormSet, EmailAddressFormSet, WebSiteFormSet, StreetAddressFormSet
from django.contrib import messages

def list(request, page=1, template='contacts/company/list.html'):
    """List of all the companies.

    :param template: Add a custom template.
    """

    company_list = Company.objects.all()
    paginator = Paginator(company_list, 20)

    try:
        companies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        companies = paginator.page(paginator.num_pages)

    kwvars = {
        'object_list': companies.object_list,
        'has_next': companies.has_next(),
        'has_previous': companies.has_previous(),
        'has_other_pages': companies.has_other_pages(),
        'start_index': companies.start_index(),
        'end_index': companies.end_index(),
    }

    try:
        kwvars['previous_page_number'] = companies.previous_page_number()
    except (EmptyPage, InvalidPage):
        kwvars['previous_page_number'] = None
    try:
        kwvars['next_page_number'] = companies.next_page_number()
    except (EmptyPage, InvalidPage):
        kwvars['next_page_number'] = None

    return render_to_response(template, kwvars, RequestContext(request))

def detail(request, pk, slug=None, template='contacts/company/detail.html'):
    """Detail of a company.

    :param template: Add a custom template.
    """

    try:
        company = Company.objects.get(pk__iexact=pk)
    except Company.DoesNotExist:
        raise Http404

    kwvars = {
        'object': company,
    }

    return render_to_response(template, kwvars, RequestContext(request))

def create(request, template='contacts/company/create.html'):
    """Create a company.

    :param template: A custom template.
    :param form: A custom form.
    """

    user = request.user
    if not user.has_perm('contacts.add_company'):
        return HttpResponseForbidden()

    if request.method == 'POST':
        company_form = CompanyCreateForm(request.POST)
        if company_form.is_valid():
            c = company_form.save()
            msg = 'Company added'
            messages.success(request, msg)
            return HttpResponseRedirect(c.get_absolute_url())
        else:
            return HttpResponseServerError

    kwvars = {
        'form': CompanyCreateForm()
    }

    return render_to_response(template, kwvars, RequestContext(request))

def update(request, pk, slug=None, template='contacts/company/update.html'):
    """Update a company.

    :param template: A custom template.
    :param form: A custom form.
    """

    user = request.user
    if not user.has_perm('contacts.change_company'):
        return HttpResponseForbidden()

    try:
        company = Company.objects.get(pk__iexact=pk)
    except Company.DoesNotExist:
        raise Http404

    
    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST, instance=company)
        phone_formset = PhoneNumberFormSet(request.POST, instance=company)
        email_formset = EmailAddressFormSet(request.POST, instance=company)
        website_formset = WebSiteFormSet(request.POST, instance=company)
        address_formset = StreetAddressFormSet(request.POST, instance=company)

        if form.is_valid() and phone_formset.is_valid() and \
            email_formset.is_valid() and \
            website_formset.is_valid() and address_formset.is_valid():
            form.save()
            phone_formset.save()
            email_formset.save()
            website_formset.save()
            address_formset.save()
            msg = 'Company updated'
            messages.success(request, msg)

            return HttpResponseRedirect(company.get_absolute_url())
        
    else:
        
        form = CompanyUpdateForm(instance=company)
        phone_formset = PhoneNumberFormSet(instance=company)
        email_formset = EmailAddressFormSet(instance=company)
        website_formset = WebSiteFormSet(instance=company)
        address_formset = StreetAddressFormSet(instance=company)
        
    kwvars = {
        'form': form,
        'phone_formset': phone_formset,
        'email_formset': email_formset,
        'website_formset': website_formset,
        'address_formset': address_formset,
        'object': company,
    }

    return render_to_response(template, RequestContext(request, kwvars))

def delete(request, pk, slug=None, template='contacts/company/delete.html'):
    """Update a company.

    :param template: A custom template.
    """

    user = request.user
    if not user.has_perm('contacts.delete_company'):
        return HttpResponseForbidden()

    try:
        company = Company.objects.get(pk__iexact=pk)
    except Company.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        new_data = request.POST.copy()
        if new_data['delete_company'] == 'Yes':
            company.delete()
            msg = 'Company deleted'
            messages.success(request, msg)

            return HttpResponseRedirect(reverse('contacts_company_list'))
        else:
            return HttpResponseRedirect(company.get_absolute_url())

    kwvars = {
        'object': company,
    }

    return render_to_response(template, kwvars, RequestContext(request))