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

	name = models.CharField(max_length=300, null=True)
	email = models.EmailField(max_length = 255, unique = True)
	password = models.CharField(max_length = 30, null=True)
	level_of_education = models.SmallIntegerField(choices = education_options, null = True)
	user_type = models.SmallIntegerField(default=0, choices = user_type_options)
	date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=True)
	speed = models.DecimalField(max_digits=6, decimal_places=3, default=1, editable=False)

	def __unicode__(self):
		return "ID: {0} User: {1}".format(self.id, self.email)


class Topic(models.Model):
	name = models.CharField(max_length=100, primary_key=True)

	def __unicode__(self):
		return "Topic: {0}".format(self.name)


class Ticket(models.Model):
	#a primary key is automatically generated
	name = models.CharField(max_length=140)
	estimated_time = models.SmallIntegerField(default=4)
	importance = models.SmallIntegerField(default=50)
	description = models.TextField(max_length=500)
	author = models.ForeignKey(
		'User',
		null=True
	)
	topic = models.ForeignKey(
		'Topic',
		on_delete = models.CASCADE,
		null=True,
	)
	dependencies = models.ManyToManyField(
		'Ticket',
		blank=True
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
	description = models.TextField(max_length=500)
	public = models.BooleanField(choices = visibility_choices, default=1)
	rate = models.SmallIntegerField(blank = True, null = True, default=0, editable=False);
	estimated_time = models.SmallIntegerField(null=True, editable=False)
	number_of_students = models.SmallIntegerField(default=0, editable=False);
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
	sprints = models.ManyToManyField('Sprint', blank=True)
	daily_hours_commitment = models.SmallIntegerField(default=4)

	def __unicode__(self):
		return "Student {0} in {1}".format(self.student.id, self.career.name)

class TicketInsideSprint(models.Model):
	progress_choices = (
		(0, 'A fazer'),
		(1, 'Em estudos'),
		(2, 'Fazendo exercicios'),
		(3, 'Em revisao'),
		(4, 'Concluido'),
	)
	ticket = models.ForeignKey(
		'Ticket',
	)
	progress = models.SmallIntegerField(default=0, choices=progress_choices)

	def __unicode__(self):
		return "{0}: {1}".format(self.id, self.ticket.name)

class Sprint(models.Model):
	tickets = models.ManyToManyField('TicketInsideSprint', blank=True)
	beginning = models.DateTimeField(default=now, editable=False)

	def __unicode__(self):
		return "Sprint: {0}".format(self.id)