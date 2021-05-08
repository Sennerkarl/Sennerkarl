from pathlib import Path
from .models import WorldBorder, SBPRI, Data
import web_project
import pandas as pd

ctycsv = Path(web_project.__file__).resolve().parent / 'data' / 'country_csv.csv'
SBPRIcsv = Path(web_project.__file__).resolve().parent / 'data' / 'Overview_2006_sd.csv'

def saveSBPRI(verbose=True):
    SBPRI.objects.all().delete()

    df = pd.read_csv('Overview_2006_sd.csv')
    SBPRI.objects.bulk_create(SBPRI(**vals) for vals in df.to_dict('records'))

def saveWorld(verbose=True):
    WorldBorder.objects.all().delete()

    df = pd.read_csv('country_csv.csv')
    WorldBorder.objects.bulk_create(WorldBorder(**vals) for vals in df.to_dict('records'))


def update_SBPRI():
    SBPRI.objects.all().delete()

    df = pd.read_csv('SBPRI-2021-01.csv') #as set now
    df.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
    df['id'] = range(1, 1+len(df))
    SBPRI.objects.bulk_create(SBPRI(**vals) for vals in df.to_dict('records'))

def update_Data(csv):
    Data.objects.all().delete()

    df = pd.read_csv(csv) #as set now
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df.set_index('date', inplace=True)
    
    for country in df:
        for row in df.index:
            Data.objects.create(date=row, country=country, category='SBPRI', value=df[country][row])

def update_Category(csv, category):
    df = pd.read_csv(csv) #as set now
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df.set_index('date', inplace=True)
    
    for country in df:
        for row in df.index:
            Data.objects.create(date=row, country=country, category=category, value=df[country][row])