from django.core.mail import send_mail
from django.conf import settings

def send_movie_created_email(movie):
    """
    Sends an email notification to the user who created the movie.

    Parameters:
    movie (Movie): The movie instance containing information about the created movie,
                   including the user who created it and the movie title.

    Returns:
    None
    """
    user_email = movie.created_by.email  
    subject = f"The Movie Created: {movie.title}"
    message = f"'{movie.title}' movie created."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]  

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
