from __future__ import unicode_literals
from django.utils.timezone import now
from datetime import timedelta
from django.db import models

# Create your models here.

class User(models.Model):
	user_type_options = (('0', 'Estudante'), ('1', 'Educador'), ('2', 'Ambos'))
	education_options = (
		('0', 'Nao frequentou'), 
		('1', 'Fundamental cursando'),
		('2', 'Fundamental concluido'),
		('3', 'Medio cursando'),
		('4', 'Medio concluido'), 
		('5', 'Superior cursando'),
		('6', 'Superior concluido'),
		('7', 'Pos cursando'),
		('8', 'Pos concluido')
		)

	name = models.CharField(max_length=300)
	email = models.EmailField(max_length = 255, primary_key = True)
	password = models.CharField(max_length = 30, default="&0k4f")
	level_of_education = models.CharField(max_length = 1, choices = education_options, default = '3')
	user_type = models.CharField(max_length = 1, choices = user_type_options)
	date_of_birth = models.DateField(auto_now=False, auto_now_add=False, default=now)
	speed = models.DecimalField(max_digits=6, decimal_places=3)

	def __unicode__(self):
		return "User: {0}".format(self.name)


class Topic(models.Model):
	name = models.CharField(max_length=100, primary_key=True)

	def __unicode__(self):
		return "Topic: {0}".format(self.name)


class Ticket(models.Model):
	#a primary key is automatically generated
	name = models.CharField(max_length=140)
	estimated_time = models.DurationField(default=timedelta(hours=8))
	importance = models.SmallIntegerField(default=50)
	description = models.TextField(max_length=500)
	topic = models.ForeignKey(
		'Topic',
		on_delete = models.CASCADE,
		null=True,
		)

	def __unicode__(self):
		return "Ticket: {0}".format(self.name)


class Career(models.Model):
	visibility_choices = (
		(0, 'Privada'),
		(1, 'Publica')
		)
	author = models.ForeignKey(
		'User',
		null=True
	)
	name = models.CharField(max_length=140)
	description = description = models.TextField(max_length=500)
	public = models.BooleanField(choices = visibility_choices, default=1)
	rate = models.SmallIntegerField(blank = True, null = True);
	estimated_time = models.DurationField(default=timedelta(hours=400))
	number_of_students = models.SmallIntegerField(default=0);
	tickets = models.ManyToManyField('Ticket')

	def __unicode__(self):
		return "Carreira: {0}".format(self.name)


class Enrollment(models.Model):
	student = models.ForeignKey(
		'User',
		on_delete = models.CASCADE
		)
	career = models.ForeignKey(
		'Career',
		on_delete = models.CASCADE
		)
	sprints = models.ManyToManyField('Sprint')

class TicketInsideSprint(models.Model):
	ticket = models.ForeignKey(
		'User',
		null=True
	)
# 	sprint
#	progress

class Sprint(models.Model):
	tickets = models.ManyToManyField('TicketInsideSprint')
	beginning = models.DateTimeField(blank = True, null = True, default=now, editable=False)

	def __unicode__(self):
		return "Sprint: {0}".format(self.name)