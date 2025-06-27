from django.urls import path

from . import views

urlpatterns = [path('', views.index, name='index'),path("index.html", views.index, name="index"),
	       path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),	     
	       path('DriverWaiting', views.DriverWaiting, name="DriverWaiting"),	
	       path('DriverLocation.html', views.DriverLocation, name="DriverLocation"),
	       path('DriverLocationAction', views.DriverLocationAction, name="DriverLocationAction"),
	       path('AcceptRide', views.AcceptRide, name="AcceptRide"),
	       path('StartRide', views.StartRide, name="StartRide"),
	       path('RideComplete', views.RideComplete, name="RideComplete"),
	       path('Ratings.html', views.Ratings, name="Ratings"),
	       path('RatingsAction', views.RatingsAction, name="RatingsAction"),
	       path('ShareLocation', views.ShareLocation, name="ShareLocation"),
	       path('ShareLocationAction', views.ShareLocationAction, name="ShareLocationAction"),
	       path('ViewDrivers', views.ViewDrivers, name="ViewDrivers"),
	       path('RideCompleteAction', views.RideCompleteAction, name="RideCompleteAction"),
	       path('CancelRide', views.CancelRide, name="CancelRide"),
	       path('CancelRideAction', views.CancelRideAction, name="CancelRideAction"),
	       path('ViewPastRides', views.ViewPastRides, name="ViewPastRides"),
]