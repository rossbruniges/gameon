from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from gameon.users.forms import ProfileForm, ProfileCreateForm
from gameon.users.models import Profile


def signout(request):
    """Sign the user out, destroying their session."""
    auth.logout(request)
    return redirect('static_site.home')


def profile(request, username):
    """Display profile page for user specified by ``username``."""
    user = get_object_or_404(auth.models.User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'users/profile.html', {
        'profile': profile,
    })


@login_required
def edit(request):
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
            return redirect(profile)
    else:
        form = form_class(instance=profile)
    return render(request, 'users/profile_edit.html', {
        'form': form,
        'profile': profile,
        'page_mode': mode,
    })
