from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from greeva.users.models import User
from greeva.users.auth_helpers import custom_login_required, get_current_user


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


from .forms_profile import UserProfileForm

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/user_profile.html"
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        return reverse("users:profile")

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated
        return self.request.user

user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


@custom_login_required
def user_profile_view(request):
    current_user = get_current_user(request)
    if not current_user:
        return redirect('/auth/login/')

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        age = (request.POST.get("age") or "").strip()
        profile_image = (request.POST.get("profile_image") or "").strip()

        updated = False
        if name:
            current_user.Name = name
            updated = True
        if phone:
            current_user.Phone = phone
            updated = True
        if age:
            try:
                current_user.Age = int(age)
                updated = True
            except ValueError:
                pass
        if profile_image:
            current_user.profile_image = profile_image
            updated = True

        if updated:
            current_user.save()
            messages.success(request, "Profile updated successfully.")

        return redirect(f"{reverse('users:profile')}?updated=1")

    return render(request, "users/user_profile.html", {"current_user": current_user})



