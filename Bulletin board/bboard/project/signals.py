from django.dispatch import receiver
from django.core.mail import  send_mail
from .models import Comment, User,Author
from django.db.models.signals import pre_save, post_save
from django.conf import settings

@receiver(post_save, sender=User)
def otp_mail(sender, instance, **kwargs):
    if not instance.is_active:
        author = Author.objects.create(author=instance)
        otp = author.generate_code()[:7]
        print(otp)
        print(instance.email)
        send_mail(
            subject='Your account verification email',
            message=f'Your otp is {otp}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )



@receiver(pre_save, sender=Comment)
def notify_comment(sender, instance, **kwargs):
    if instance.active is False:
        post_name = instance.post.title
        mail = instance.post.author.email
        send_mail(
            subject=f"Added a new comment to the post {post_name}'!",
            message=instance.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mail],
            fail_silently=False,

        )
        print('Уведомление отослано:' 'на почту', mail, ' на тему ', instance.body)


