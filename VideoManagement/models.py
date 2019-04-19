from django.db import models

class VideoInfo(models.Model):
    title = models.CharField(max_length=100)
    performer = models.CharField(max_length=50)
    description = models.TextField()

    filename = models.CharField(max_length=50)
    #filetype = models.CharField(max_length=5)
    embed_link = models.CharField(max_length=350, default="Enter embed link here")

    view_count = models.IntegerField(default=0, editable=False)
    is_disabled = models.BooleanField(default=False)

    def increment_view_count(self, *args, **kwargs):
        self.view_count = self.view_count + 1

        super(VideoInfo, self).save(*args, **kwargs)

    def publish(self):
        self.save()

    def __str__(self):
        return "%s(%s) - %s" % (self.title, self.performer, self.filename)
