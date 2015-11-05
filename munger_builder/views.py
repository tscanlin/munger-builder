from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserForm

def home_page(request):
    return HttpResponseRedirect('/app_index/')

@login_required
def app_index(request):
    template = loader.get_template('app_index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def register(request):
    context = RequestContext(request)

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            return HttpResponseRedirect('/script_builder/munger_builder_index/')

        else:
            input_dict = request.POST.dict()
            for key in input_dict:
                if not input_dict[key]:
                    messages.error(request, 'Please enter: {0}'.format(key))
            return HttpResponseRedirect('/register/')

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
            'registration/register.html',
            {'user_form': user_form},
            context)
