# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime
from datetime import date,datetime

from django.db import models

class Grp(models.Model):
    kod = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60L)
    adres = models.CharField(max_length=60L)
    nameb = models.CharField(max_length=40L)
    schet = models.CharField(max_length=20L)
    mfo = models.CharField(max_length=9L)
    adrb = models.CharField(max_length=40L)
    strana = models.IntegerField()
    unp = models.CharField(max_length=15L)
    kpp = models.CharField(max_length=15L)
    desc = models.CharField(max_length=255L)
    class Meta:
        db_table = 'grp'
        managed = False
        ordering = ['name']
    def __unicode__(self):
        return u'%s (%d)' % (self.name, self.kod)    
    
class Naimceh(models.Model):
    name = models.CharField(max_length=60L, blank=True)
    ceh = models.IntegerField(null=True, blank=True)
    uch = models.IntegerField(null=True, blank=True)
    cehuch = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'naimceh'
        managed = False
class Naimprof(models.Model):
    kod = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40L, blank=True)
    class Meta:
        db_table = 'naimprof'
        managed = False
class Prof(models.Model):
    kod = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40L, blank=True)
    short_name = models.CharField(max_length=40L, blank=True)
    class Meta:
        db_table = 'prof'
        managed = False
class Tncehfio(models.Model):
    tn = models.IntegerField(primary_key=True)
    ceh = models.IntegerField(null=True, blank=True)
    fm = models.CharField(max_length=20L, blank=True)
    im = models.CharField(max_length=15L, blank=True)
    ot = models.CharField(max_length=15L, blank=True)
    uch = models.IntegerField(null=True, blank=True)
    brg = models.IntegerField(null=True, blank=True)
    datar = models.CharField(max_length=10L, blank=True)
    kodprof = models.ForeignKey(Prof, to_field="kod", db_column="kodprof") #models.IntegerField(null=True, blank=True)
    raz = models.IntegerField(null=True, blank=True)
    p_ser = models.CharField(max_length=10L, blank=True)
    p_nom = models.IntegerField(null=True, blank=True)
    vidan = models.CharField(max_length=30L, blank=True)
    datav = models.CharField(max_length=10L, blank=True)

    class Meta:
        db_table = 'tncehfio'
        managed = False
        
    @property
    def date_dr(self):
        s_date = self.datar.split('/')
        dr_date = date(int(s_date[2]), int(s_date[1]), int(s_date[0]))
        return dr_date
    
    @property
    def day_to_dr(self):
        s_date = self.datar.split('/')
        today = date.today()
        dr_date = date(today.year, int(s_date[1]), int(s_date[0]))
        return (dr_date-today).days
    
    def __unicode__(self):
        return u'%s' % (self.fm)    
    

    
    
class SpisplFo(models.Model):
    id = models.IntegerField(primary_key=True)
    kodsl = models.IntegerField(db_column='KodSl', blank=True, null=True) # Field name made lowercase.
    kodpodr = models.IntegerField(db_column='Kodpodr', blank=True, null=True) # Field name made lowercase.
    nomzap = models.IntegerField(db_column='Nomzap', blank=True, null=True) # Field name made lowercase.
    datavod = models.DateTimeField(db_column='DataVod', blank=True, null=True) # Field name made lowercase.
    kodv = models.IntegerField(db_column='KodV', blank=True, null=True) # Field name made lowercase.
    kursv1 = models.FloatField(db_column='KursV1', blank=True, null=True) # Field name made lowercase.
    kodkl = models.IntegerField(db_column='KodKl', blank=True, null=True) # Field name made lowercase.
    namekl = models.CharField(db_column='NameKl', max_length=60, blank=True) # Field name made lowercase.
    kodopl = models.IntegerField(db_column='Kodopl', blank=True, null=True) # Field name made lowercase.
    sumv1 = models.FloatField(db_column='SumV1', blank=True, null=True) # Field name made lowercase.
    sumv2 = models.FloatField(db_column='SumV2', blank=True, null=True) # Field name made lowercase.
    kodv2 = models.IntegerField(db_column='KodV2', blank=True, null=True) # Field name made lowercase.
    kursv2 = models.FloatField(db_column='KursV2', blank=True, null=True) # Field name made lowercase.
    sumo1 = models.FloatField(db_column='SumO1', blank=True, null=True) # Field name made lowercase.
    sumo2 = models.FloatField(db_column='SumO2', blank=True, null=True) # Field name made lowercase.
    ostv1 = models.FloatField(db_column='OstV1', blank=True, null=True) # Field name made lowercase.
    ostv2 = models.FloatField(db_column='OstV2', blank=True, null=True) # Field name made lowercase.
    dataopl = models.DateTimeField(db_column='DataOpl', blank=True, null=True) # Field name made lowercase.
    datatov = models.DateTimeField(db_column='Datatov', blank=True, null=True) # Field name made lowercase.
    bank = models.CharField(db_column='Bank', max_length=10, blank=True) # Field name made lowercase.
    naznpl = models.CharField(db_column='Naznpl', max_length=50, blank=True) # Field name made lowercase.
    dopinf = models.CharField(db_column='DopInf', max_length=15, blank=True) # Field name made lowercase.
    prizsbr = models.TextField(db_column='PrizSbr', blank=True) # Field name made lowercase. This field type is a guess.
    prizomo = models.TextField(db_column='PrizOMO', blank=True) # Field name made lowercase. This field type is a guess.
    d_opldok = models.DateTimeField(db_column='D_opldok', blank=True, null=True) # Field name made lowercase.
    specif = models.CharField(db_column='Specif', max_length=50, blank=True) # Field name made lowercase.
    dogovor = models.CharField(db_column='Dogovor', max_length=50, blank=True) # Field name made lowercase.
    dataotgr = models.DateTimeField(db_column='Dataotgr', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Spispl_Fo'
    def city(self):
        return self.namekl.split(' ')[0]
    def client_name(self):
        try:
            return self.namekl.split("'")[1]
        except:
            return self.namekl
    def payment_age(self):
        now = datetime.now()
        try:
            value = self.d_opldok.replace(tzinfo=None)
            difference = now - value
        except:
            return -1
        return difference.days
    def payment_num(self):
        result = ''
        fin = Fin.objects.filter(kodkl=self.kodkl, datao=self.d_opldok, sumv_o=self.sumo1).first()
        if fin:
            result = fin.nomerp
        else:
            # TODO: собрать все оплаты по служебной
            # найти последнюю оплату            
            fin = Fin.objects.filter(kodkl=self.kodkl, datao=self.d_opldok).first()
            if fin:
                result = fin.nomerp
                test = SpisplFo.objects.filter(kodkl=fin.kodkl, d_opldok = fin.datao, sumo1 = fin.sumv_o)
                if test:
                    result = ''
        return result
        
        
class Fin(models.Model):
    id = models.IntegerField(primary_key=True)
    god = models.IntegerField(db_column='God', blank=True, null=True) # Field name made lowercase.
    mes = models.IntegerField(db_column='Mes', blank=True, null=True) # Field name made lowercase.
    kodgp = models.IntegerField(db_column='Kodgp', blank=True, null=True) # Field name made lowercase.
    kodkl = models.IntegerField(db_column='Kodkl', blank=True, null=True) # Field name made lowercase.
    kodpodr = models.IntegerField(db_column='Kodpodr', blank=True, null=True) # Field name made lowercase.
    priznop = models.CharField(db_column='PriznOp', max_length=50, blank=True) # Field name made lowercase.
    nomerp = models.IntegerField(db_column='Nomerp', blank=True, null=True) # Field name made lowercase.
    naznpl = models.CharField(db_column='Naznpl', max_length=500, blank=True) # Field name made lowercase.
    sumv_o = models.FloatField(db_column='SumV_O', blank=True, null=True) # Field name made lowercase.
    kodv = models.IntegerField(db_column='KodV', blank=True, null=True) # Field name made lowercase.
    schet = models.CharField(db_column='Schet', max_length=255, blank=True) # Field name made lowercase.
    nomdogr = models.CharField(db_column='Nomdogr', max_length=255, blank=True) # Field name made lowercase.
    datao = models.DateField(db_column='DataO', blank=True, null=True) # Field name made lowercase.
    kodzatr = models.IntegerField(db_column='Kodzatr', blank=True, null=True) # Field name made lowercase.
    namevidd = models.CharField(db_column='NameVidd', max_length=255, blank=True) # Field name made lowercase.
    viddok = models.IntegerField(db_column='Viddok', blank=True, null=True) # Field name made lowercase.
    data = models.DateField(db_column='Data', blank=True, null=True) # Field name made lowercase.
    datatov = models.DateField(db_column='Datatov', blank=True, null=True) # Field name made lowercase.
    datadog = models.DateField(db_column='Datadog', blank=True, null=True) # Field name made lowercase.
    specif = models.CharField(db_column='Specif', max_length=50, blank=True) # Field name made lowercase.
    priz_op = models.IntegerField(db_column='Priz_op', blank=True, null=True) # Field name made lowercase.
    schetkl = models.CharField(db_column='SchetKl', max_length=50, blank=True) # Field name made lowercase.
    mfo = models.CharField(db_column='MFO', max_length=9, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'fin'
