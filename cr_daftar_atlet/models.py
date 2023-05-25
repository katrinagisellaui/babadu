from django.db import models


class BarangWishlist(models.Model):
    nama_barang = models.CharField(max_length=50)
    harga_barang = models.IntegerField()
    deskripsi = models.TextField()

class AtletKualif(models.Model):
    nama = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    negara_asal = models.CharField(max_length=50)
    play_right = models.BooleanField()
    height = models.IntegerField()
    world_rank = models.IntegerField()
    world_tour_rank = models.IntegerField()
    jenis_kelamin = models.CharField(max_length=50)
    total_point = models.IntegerField()

class AtletNonKualif(models.Model):
    nama = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    negara_asal = models.CharField(max_length=50)
    play_right = models.BooleanField()
    height = models.IntegerField()
    world_rank = models.IntegerField()
    jenis_kelamin = models.CharField(max_length=50)
    total_point = models.IntegerField()

class AtletGanda(models.Model):
    id_atlet_ganda = models.UUIDField()
    nama_1 = models.CharField(max_length=50)
    nama_2 = models.CharField(max_length=50)
    total_point = models.IntegerField()


