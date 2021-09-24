import pandas as pd
from pytrends.request import TrendReq
import datetime
import random
import time

from .models import WorldBorder, SBPRI, Data

# Import Statsmodels
from statsmodels.tsa.seasonal import seasonal_decompose

def getgoogledata():
    
    languages = ['Eng', 'Ger', 'Esp']
    categories = ['Overview', 'Regulation', 'Sanctions', 'Situation'] 

    dictctry = {'Eng': {'Canada': "CA", 'Australia': "AU",'India': "IN", 'Pakistan': "PK", 'Ireland': "IE",'United States': "US",
            'New Zealand': "NZ",'South Africa': "ZA", 'Singapore': "SG", "Sierra Leone":"SL", "Liberia":"LR", "Ghana":"GH",
                    "Nigeria":"NG", "Cameroon":"CM" ,"Ethiopia":"ET", "Uganda":"UG", "Rwanda":"RW", "Kenya":"KE",
                    "Tanzania":"TZ", "Malawi":"MW", "Zambia":"ZM", "Zimbabwe":"ZW", "Botswana":"BW", "United Kingdom":"GB",
                    "Sudan":"SD", "South Sudan": "SS", "Nambia":"NA"}, #https://de.m.wikipedia.org/wiki/Datei:Official_languages_in_Africa.svg
            'Ger': {'Switzerland': "CH", 'Austria': "AT",'Germany': "DE"},
                'Esp': {'Bolivia': "BO", 'Uruguay': "UY",'Paraguay': "PY", 'Venezuela': "VE",
                        'Colombia': "CO",'Ecuador': "EC", 'Peru': "PE",'Chile': "CL", 'Argentina': "AR",
                        'Mexico': "MX", 'Spain':'ES'}
            }

    ctrylist = []
    for lang in languages:
        ctrylist += list(dictctry[lang])
        
    weights = {'Political Regulation':16, 'Political Sanctions':33, 'Political Situation':45}

    # create dictionary with relevant keywords
    kw_dict = {'Eng':{
            'Political Regulation': ["bureaucracy", "Environmental protection",  "Regulations",
                                        "taxes", "property rights", 'expropriation'],
            'Political Sanctions': ["exchange","foreign investment","quotas", 'restrictions', 'subsidies',
                                    'tariffs', "transferability", "sanctions"],
            'Political Situation': ["central bank","corruption","instability","judiciary","nationalization",
                    "protectionism","revolt", 'social conflict',
                    "strike","terrorism","war"],
            'Corruption': ['corruption']},
            
            'Ger':{
            'Political Regulation': ["Bürokratie", "Umweltschutz",  "Regulierung",
                                        "Steuern", "Urheberrecht", 'Enteignung'],
            'Political Sanctions': ["Transaktionen","foreign investment","Einfuhrzoll", 'Beschränkungen',
                                    'Subventionen',
                                    "Sanktionen"],
            'Political Situation': ["Zentralbank","Korruption","Instabilität","Justiz","Nationalismus",
                    "Protektionismus","Aufstände", 'Staatsgewalt',
                    "Streik","Terrorismus","Krieg"],
            'Corruption': ['Korruption']},
            
            'Esp':{
            'Political Regulation': ["burocracia", "protección del medio ambiente",  "reglamento",
                                        "impuesto", "regulaciones"],
            'Political Sanctions': ["sanciones", "restricciones", "convertibilidad",
                    "cuotas","subsidio","tarifas", 'cambiario', 'inversion extranjera', 'expropiación', "derecho de propiedad"],
            'Political Situation': ["judicial","situación política","corrupcion","conflicto social", "revuelta",
                    "inestabilidad","nacionalismo", 'gobierno militar',
                    "proteccionismo","huelga","terrorismo","guerra", "banco central"],
            'Corruption': ['corrupcion']}
            
            }

    # start pytrend and create DataFrame for all country data
    pytrends = TrendReq(hl='en-EN', tz=360, timeout=(100))

    #dryrun pytrend - with manually fixed first search term and geo
    pytrends.build_payload(['bureaucracy'], cat=0, timeframe=f'2006-01-01 {datetime.datetime.today().strftime("%Y-%m-%d")}', geo='CA', gprop='') #build data extraction references
    dry_df = pytrends.interest_over_time()
    filt = dry_df['isPartial'] == 'True' # create filter to get isPartial column
    dry_df.drop(index=dry_df[filt].index, inplace=True) # drop all indexes where values are inPartial = True
    dry_df.drop(columns=['isPartial'], inplace=True) # drop column isPartial

    all_ctys_df = pd.DataFrame(columns=[list(dictctry[languages[0]])[0]]) #grab first country name for first column
    weighted_sbpri_df = pd.DataFrame(columns=ctrylist) # create dataframe for weigthed values
    weighted_regulation_df = pd.DataFrame(columns=ctrylist) # create dataframe for weigthed values
    weighted_situation_df = pd.DataFrame(columns=ctrylist)
    weighted_sanctions_df = pd.DataFrame(columns=ctrylist)

    #map zero values to weighted sbpri - this ensure that we can add the weigthed values of each category
    weighted_sbpri_df[ctrylist[0]] = dry_df['bureaucracy']*0
    weighted_sbpri_df = weighted_sbpri_df.fillna(0)

    #first loop over Languages
    for lang in languages:   
        
        #Second loop over Categories and Respective Terms for that languages
        for tpc, terms in  kw_dict[lang].items():
            all_terms_df = pd.DataFrame(columns=[terms[0]])
            
            # Third run Pytrend per Country in that language with the respective categories and terms
            for country, abbreviation in dictctry[lang].items():  
                whole_df = pd.DataFrame(columns=[terms[0]]) # create empty dataframe
    #             if country not in ['New Zealand', 'Ireland', 'Bolivia', 'Uruguay', 'Paraguay']: #countries where search terms have no data

                for i in terms: #loop for data collection from google for each individual word in kw_list
                    try:
                        pytrends.build_payload([i], cat=0, timeframe=f'2006-01-01 {datetime.datetime.today().strftime("%Y-%m-%d")}', geo=abbreviation, gprop='') #build data extraction references
                        df = pytrends.interest_over_time() #create initial dataframe
    #                     filt = df['isPartial'] == 'True' # create filter to get isPartial column
    #                     df.drop(index=df[filt].index, inplace=True) # drop all indexes where values are inPartial = True
                        df.drop(columns=['isPartial'], inplace=True) # drop column isPartial
                        whole_df[i] = df[i] #add column to whole_df dataframe
                        time.sleep(random.uniform(2,5))

                        print(country + ' / ' + i)
                    except:
                        print("error " + country + ' / ' + i)
                        pass

        # After Thrid Loop Correct data Per Country
            
        # seasonal correction to each search term since words have different seasonality (trabjar) searched more beginning of year other words much less in the beginning 
            delta_df = whole_df
            delta_df.dropna(axis=1, inplace=True)
            delta_df.replace(0, 0.1, inplace=True)
            for i in delta_df.columns:
                result_mul = seasonal_decompose(delta_df[i], model='multiplicative', extrapolate_trend='freq')
                delta_df[i] = (delta_df[i] / result_mul.seasonal)

            # create change deltas for search term !! check if this may ruin data !!
            delta_df = delta_df - delta_df.min()
            delta_df = delta_df / delta_df.max() * 100

        #         set delta_df which is delta per word and seasonally corrected as whole_df
            whole_df = delta_df

            # create mean column for every country    
            x = whole_df[terms[0]] * 0    # create dataframe with same amount of rows as whole_df and 0 values
            for i in whole_df.columns:
                x += whole_df[i]
                if tpc == list(kw_dict[lang])[0]:
                    all_terms_df[i] = whole_df[i]
            x = x / len(whole_df.columns)
            whole_df['Mean'] = x

            # After Data correcting and Mean creation add Categories to weighted df with the necessary weights
            if tpc == list(kw_dict[lang])[0]:
                weighted_sbpri_df[country] += weights[list(kw_dict[lang])[0]]*whole_df['Mean']
                weighted_regulation_df[country] = whole_df['Mean']

            if tpc == list(kw_dict[lang])[1]:
                weighted_sbpri_df[country] += weights[list(kw_dict[lang])[1]]*whole_df['Mean']
                weighted_sanctions_df[country] = whole_df['Mean']

            if tpc == list(kw_dict[lang])[2]:
                weighted_sbpri_df[country] += weights[list(kw_dict[lang])[2]]*whole_df['Mean']
                weighted_situation_df[country] = whole_df['Mean']


    weighted_sbpri_df = weighted_sbpri_df.applymap(lambda x: x/sum(weights.values()))

    # push new data to database
    Data.objects.all().delete() # delete data in database
    
    for country in weighted_sbpri_df:
        for row in weighted_sbpri_df.index:
            Data.objects.create(date=row, country=country, category='SBPRI', value=weighted_sbpri_df[country][row])

    for country in weighted_regulation_df:
        for row in weighted_regulation_df.index:
            Data.objects.create(date=row, country=country, category=categories[1], value=weighted_regulation_df[country][row]) 

    for country in weighted_sanctions_df:
        for row in weighted_sanctions_df.index:
            Data.objects.create(date=row, country=country, category=categories[2], value=weighted_sanctions_df[country][row])     

    for country in weighted_situation_df:
        for row in weighted_situation_df.index:
            Data.objects.create(date=row, country=country, category=categories[3], value=weighted_situation_df[country][row])                 
       