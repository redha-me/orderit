import geocoder
from django.db import models



class Day(models.Model):
	day=models.CharField(max_length=20,blank=False)

	def __str__(self):
		return self.day
		
class Hour(models.Model):
	hour=models.CharField(max_length=6,blank=False)

	def __str__(self):
		return f'{self.hour}:00'


class Wilaya(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Commune(models.Model):
    name = models.CharField(max_length=128)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, related_name='commune')
    def __str__(self):
        return self.name

# mapbox_access_token = 'pk.eyJ1IjoiYXltYW4wMTIzIiwiYSI6ImNsMWt1dzd2cjA0aTgzZWtxaGY3ZmJ6NGYifQ.yC9B1GbILU2Bn6D_YDUlfA'

class Address(models.Model):
	address = models.TextField()
	wilaya = models.TextField(blank=True, null=True)
	commune = models.TextField(blank=True, null=True)
	def __str__(self):
		return f'{self.wilaya},{self.commune}'
	# def save(self, *args, **kwargs):
	# 	g = geocoder.mapbox(self.address, key=mapbox_access_token)
	# 	g = g.latlng  
	# 	self.lat = g[0]
	# 	self.long = g[1]
	# 	return super(Address, self).save(*args, **kwargs)

	
	