from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    category = models.CharField(max_length=50, default='22')
    keywords = models.TextField(null=True, blank=True)  # Bu yerda o'zgartirish qilindi
    privacy_status = models.CharField(max_length=50, choices=(('public', 'Public'), ('private', 'Private'), ('unlisted', 'Unlisted')), default='public')

    def __str__(self):
        return self.title
