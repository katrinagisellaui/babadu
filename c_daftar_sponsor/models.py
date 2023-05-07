from django.db import models

# Create your models here.


class Sponsor(models.Model):
    id_sponsor = models.UUIDField()
    nama_brand = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    cp_name = models.CharField(max_length=50)
    cp_email = models.CharField(max_length=50)


# class AtletSponsor(models.Model):
#     id_atlet = models.ForeignKey(Atlet, on_delete=models.CASCADE)
#     id_sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
#     tgl_mulai = models.DateField()
#     tgl_selesai = models.DateField()
