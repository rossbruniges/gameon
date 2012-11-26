from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse

from gameon.users.forms import ProfileForm, ProfileCreateForm
from gameon.users.models import Profile


def signout(request):
    """Sign the user out, destroying their session."""
    auth.logout(request)
    return redirect('static_site.home')


def profile(request, username, template='users/profile.html'):
    """Display profile page for user specified by ``username``."""
    user = get_object_or_404(auth.models.User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, template, {
        'profile': profile,
    })


@login_required
def edit(request, template='users/profile_edit.html'):
    """Edit the currently logged in users profile."""
    profile = request.user.get_profile()
    form_class = ProfileForm
    mode = 'edit'
    if not profile.has_chosen_identifier:
        mode = 'create'
        form_class = ProfileCreateForm
    if request.method == 'POST':
        form = form_class(data=request.POST,
                          files=request.FILES,
                          instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            if mode == 'edit':
                return redirect(profile)
            else:
                """
                The only reason anyone will want to create an account it to
                submit a game, so take them right there
                """
                return redirect(reverse('submissions.create_entry'))
    else:
        form = form_class(instance=profile)
    return render(request, template, {
        'form': form,
        'profile': profile,
        'page_mode': mode,
    })
