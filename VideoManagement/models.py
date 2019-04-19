from django.db import models

class VideoInfo(models.Model):
    title = models.CharField(max_length=100)
    performer = models.CharField(max_length=50)
    description = models.TextField()

    filename = models.CharField(max_length=50)
    real_id = models.CharField(max_length=15, default="Enter ID here")
    embed_link = models.CharField(max_length=350, default="Enter embed link here")

    view_count = None

    is_disabled = models.BooleanField(default=False)

    def publish(self):
        self.save()

    def __str__(self):
        return "%s(%s) - %s" % (self.title, self.performer, self.filename)
