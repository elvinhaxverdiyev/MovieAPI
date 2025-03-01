from django.core.mail import send_mail
from django.conf import settings

def send_movie_created_email(movie):
    user_email = movie.created_by.email  
    subject = f"The Movie Created: {movie.title}"
    message = f"'{movie.title}' movie created."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]  

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
