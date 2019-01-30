"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script contains constants to use in the app.

"""


# LISTS OF YAHOO FINANCE SECTORS

LIST_COM_SECTORS = ['financial', 'healthcare', 'services', 'utilities', 'industrial_goods',
                    'basic_materials', 'conglomerates', 'consumer_goods', 'technology']

LIST_ES_SECTORS = ['Energia', 'Banca-y-Seguros', 'Construccion', 'Telecomunicaciones',
                   'Tecnologicas', 'Internet', 'Alimentacion-y-Consumo', 'Motor-y-Automocion',
                   'Turismo-y-Servicios', 'Farmaceutica', 'Textil', 'Audiovisual-y-Medios']

LIST_FR_SECTORS = ['Aeronautique', 'Automobile', 'Energie-et-environnement', 'Immobilier-et-BTP',
                   'Industrie-lourde', 'Sante-et-Chimie', 'Services-et-distribution',
                   'Telecoms', 'Matieres-premieres', 'Internet', 'High-Tech']

LIST_DE_SECTORS = ['energy', 'financial', 'healthcare', 'business_services', 'telecom_utilities',
                   'hardware_electronics', 'software_services', 'automobil',
                   'consumer_product_media', 'industrials', 'diversified_business',
                   'retailing_hospitality', 'chemie']

LIST_IT_SECTORS = ['Petrolio-e-Gas-Naturale', 'Chimica-e-Materie-Prime', 'Industria',
                   'Beni-di-Consumo', 'Salute', 'Servizi-al-Consumo', 'Telecomunicazioni',
                   'Servizi-Pubblici', 'Finanza', 'Tecnologia']

LIST_UK_SECTORS = ['autos_transportation', 'energy', 'financial', 'healthcare',
                   'telecoms_utilities', 'hardware_electronics', 'software_services',
                   'industrials', 'manufacturing_materials', 'leisure', 'retailing_hospitality',
                   'consumer_products_media']

# LIST OF YAHOO LANGUAGES

LIST_LANGUAGES = ['es', 'fr', 'de', 'it', 'uk']

# LISTS OF SECTORS BY GICS

LIST_GICS_UTILITIES = ['utilities', 'Servizi-Pubblici']

LIST_GICS_ENERGY = ['Energia', 'Energie-et-environnement', 'energy', 'Petrolio-e-Gas-Naturale']

LIST_GICS_INDUSTRIALS = ['Industrie-lourde', 'conglomerates', 'industrial_goods', 'Aeronautique',
                         'Services-et-distribution']

LIST_GICS_CONS_DISC = ['Motor-y-Automocion', 'Turismo-y-Servicios', 'Textil', 'Automobile',
                       'retailing_hospitality', 'automobil', 'autos_transportation', 'leisure']

LIST_GICS_CONS_STP = ['consumer_goods', 'Alimentacion-y-Consumo', 'Beni-di-Consumo',
                      'consumer_products_media']

LIST_GICS_HEALTH = ['healthcare', 'Farmaceutica', 'Salute', 'Sante-et-Chimie']

LIST_GICS_FINANCIAL = ['financial', 'Banca-y-Seguros', 'Finanza']

LIST_GICS_COM_SERV = ['Telecomunicaciones', 'telecom_utilities', 'Telecoms',
                      'Telecomunicazioni', 'telecoms_utilities', 'Servizi-al-Consumo',
                      'Audiovisual-y-Medios']

LIST_GICS_INF_TECH = ['technology', 'Tecnologicas', 'High-Tech', 'Tecnologia',
                      'hardware_electronics', 'software_services', 'Internet']

LIST_GICS_REAL_STATE = ['Immobilier-et-BTP', 'services']

LIST_GICS_NAMES = ['Communication services', 'Consumer discretionary', 'Consumer staples',
                   'Energy', 'Financials', 'Healthcare', 'Real state', 'Industrials',
                   'Information technology', 'Utilities']

# LISTS OF SECTORS BY ICB

LIST_ICB_OIL_GAS = ['Petrolio-e-Gas-Naturale']

LIST_ICB_BASIC_MAT = ['basic_materials', 'Matieres-premieres', 'manufacturing_materials',
                      'Chimica-e-Materie-Prime', 'chemie']

LIST_ICB_INDUSTRIALS = ['Industrie-lourde', 'conglomerates', 'industrial_goods', 'Aeronautique',
                        'industrials', 'Industria', 'Construccion', 'diversified_business',
                        'business_services']

LIST_ICB_CONS_GOOD = ['consumer_goods', 'Alimentacion-y-Consumo', 'autos_transportation',
                      'Beni-di-Consumo', 'Motor-y-Automocion', 'Automobile', 'automobil',
                      'Textil', 'consumer_products_media']

LIST_ICB_HEALTH = ['healthcare', 'Farmaceutica', 'Salute', 'Sante-et-Chimie']

LIST_ICB_TECH = ['internet', 'Internet', 'High-Tech', 'technology', 'Tecnologia',
                 'software_services', 'Tecnologicas', 'hardware_electronics']

LIST_ICB_FINANCIAL = ['financial', 'Banca-y-Seguros', 'Finanza', 'services', 'Immobilier-et-BTP']

LIST_ICB_UTILITIES = ['utilities', 'Servizi-Pubblici', 'Energia', 'energy',
                      'Energie-et-environnement']

LIST_ICB_TELECOM = ['Telecomunicaciones', 'telecom_utilities', 'telecoms_utilities',
                    'Telecoms', 'Telecomunicazioni']

LIST_ICB_CONS_SERV = ['Servizi-al-Consumo', 'Turismo-y-Servicios',
                      'retailing_hospitality', 'leisure', 'Audiovisual-y-Medios',
                      'Services-et-distribution']

LIST_ICB_NAMES = ['Oil & gas', 'Basic materials', 'Industrials', 'Consumer goods',
                  'Healthcare', 'Technology', 'Financials', 'Utilities',
                  'Telecommunication', 'Consumer services']

# INDEXES

INDEXES = {'%5EIBEX': 'Ibex 35', '%5EFCHI': 'CAC 40', '%5EGDAXI': 'DAX', '%5EFTSE': 'FTSE 100',
           '%5EBFX': 'BEL 20', '%5EDJI': 'Dow Jones Industrial Average',
           'FTSEMIB.MI': 'FTSE MIB INDEX', '%5EMXX': 'IPC Mexico', '%5EMERV': 'MERVAL',
           '%5ENDX': 'NASDAQ 100', '%5EIXIC': 'NASDAQ Composite', 'PSI20.LS': 'PSI 20'}

# LIST OF COUNTRIES

LIST_COUNTRIES = ['Monaco', 'Spain', 'Netherland', 'Argentina', 'Mexico', 'Italy', 'Canada',
                  'Japan', 'Chile', 'Ireland', 'Taiwan', 'Belgium', 'Bermuda', 'Peru',
                  'Brazil']
