import logging
from celery import Task
from celery import shared_task
from django.contrib.auth import get_user_model
from celery.exceptions import MaxRetriesExceededError

logger = logging.getLogger(__name__)

@shared_task()
def send_email_notifications(**kwargs):
    print("..............")

class SendUserCredentialsEmail(Task):
    # You can specify retry configuration for retries
    name = 'Send User Credentials Email'

    # timeout for task so that if the task takes too long,it will be automatically canceled.
    time_limit = 300  # 5 minutes
    soft_time_limit = 240  # 4 minutes (to handle gracefully)
    # timeout for task so that if the task takes too long,it will be automatically canceled.

    max_retries = 3  # Maximum number of retries
    default_retry_delay = 60  # Delay in seconds before retrying

    def run(self, user_id, password):
        try:
            User = get_user_model()
            user = User.objects.get(id=user_id)
            
            subject = 'Welcome to Our Platform'
            message = f'Hello {user.get_full_name()},\n\nYour account has been created successfully.\nYour login credentials are:\nUsername: {user.username}\nPassword: {password}\n\nPlease log in to your account.'

            logger.info(f"Sending email to {user.email} with subject: {subject}")
            logger.info(f"Message: {message}")

            # Send the email using Django's send_mail
            # from_email = settings.DEFAULT_FROM_EMAIL
            # send_mail(subject, message, from_email, [user.email])
            
            logger.info(f"Email sent successfully to {user.email}")
        
        except User.DoesNotExist:
            logger.error(f"User with ID {user_id} does not exist.")
        except Exception as e:
            logger.error(f"Error sending email to user {user_id}: {str(e)}")
            try:
                self.retry(exc=e)
            except MaxRetriesExceededError:
                logger.error(f"Max retries exceeded for sending email to user {user_id}.")