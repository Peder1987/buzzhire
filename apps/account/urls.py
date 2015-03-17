from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^signup/$", views.SignupView.as_view(), name="account_signup"),
    url(r"^login/$", views.LoginView.as_view(), name="account_login"),
    url(r"^logout/$", views.LogoutView.as_view(), name="account_logout"),

#     url(r"^password/change/$", views.password_change,
#         name="account_change_password"),
#     url(r"^password/set/$", views.password_set, name="account_set_password"),
#
#     url(r"^inactive/$", views.account_inactive, name="account_inactive"),
#
#     # E-mail
#     url(r"^email/$", views.email, name="account_email"),
#     url(r"^confirm-email/$", views.email_verification_sent,
#         name="account_email_verification_sent"),
#     url(r"^confirm-email/(?P<key>\w+)/$", views.confirm_email,
#         name="account_confirm_email"),
#
    # Password reset
    url(r"^password/reset/$", views.PasswordResetView.as_view(),
        name="account_reset_password"),
    url(r"^password/reset/done/$", views.PasswordResetDoneView.as_view(),
        name="account_reset_password_done"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.PasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key"),
    url(r"^password/reset/key/done/$",
        views.PasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done"),
]

