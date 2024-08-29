from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm


urlpatterns = [
    path('',views.home),
    path('category/<slug:val>', views.CategoryView.as_view(),name="category"),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),    
    path('ByCategory/', views.ByCategory,name="ByCategory"),
    path('ByMeaning/', views.ByMeaning,name="ByMeaning"),
    path('ByColour/', views.ByColour,name="ByColour"),
    path('ByCrystals/', views.ByCrystals,name="ByCrystals"),
    path('Choose/', views.Choose,name="Choose"),
    path('Cleanse/', views.Cleanse,name="Cleanse"),
    path('Customize/', views.Customize,name="Customize"),
    path('about/', views.about,name="about"),
    path('contact/', views.contact,name="contact"),
    path('feedback/', views.feedback,name="feedback"),
    path('profile/', views.ProfileView.as_view(),name="profile"),
    path('address/', views.address, name="address"),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name="updateAddress"),
    path('feedback/',views.feedback,name="feedback"),
    path('add-to-cart/',views.add_to_cart,name="add-to-cart"),
    path('cart/', views.show_cart, name="showcart"),
    path('wishlist/', views.show_wishlist, name="wishlist"),

    path('checkout/', views.checkout.as_view(), name="checkout"),
    path('paymentdone/', views.payment_done, name="paymentdone"),
    path('orders/', views.orders, name="orders"),
    path('search/', views.search, name="search"),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart, name='minus-cart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('pluswishlist/',views.plus_wishlist),
    path('minuswishlist/',views.minus_wishlist),


    #new urls
    path('menu/', views.menu, name='menu'),
    path('recommend/', views.recommended_ui, name='recommend'),
    path('recommend_foods/', views.recommend_foods, name='recommend_foods'),
 

#login authentication
    path('registration/', views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name="login"),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'),name="passwordchange"),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name="passwordchangedone"),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'),name="logout"),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Sfit Food Adda"
admin.site.site_title = "Smart Canteen"
admin.site.site_index_title = "Welcome to Sfit Food Adda"