from django.db import models

class sys_hcb_diagram_tableposition(models.Model):
  to_app = models.CharField(max_length=255)
  to_model = models.CharField(max_length=255)
  xt = models.IntegerField()
  yt = models.IntegerField()
  def __str__(self):
    return '{}->{}: {}x{}"'.format(self.to_app, self.to_model, self.xt, self.yt)
  class Meta:
    ordering = ('to_app', 'to_model', 'xt', 'yt')
