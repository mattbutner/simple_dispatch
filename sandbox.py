import pickle
import numpy
import scipy
import os.path
import pandas
from simple_dispatch import generatorData
from simple_dispatch import bidStack
from simple_dispatch import dispatch
from  mefs_from_simple_dispatch import generateMefs
from  mefs_from_simple_dispatch import plotDispatch


run_year = 2017
#input variables. Right now the github only has 2017 data on it.
#specific the location of the data directories
# ferc 714 data from here: https://www.ferc.gov/docs-filing/forms/form-714/data.asp
# ferc 714 ids available on the simple_dispatch github repository
# egrid data from here: https://www.epa.gov/energy/emissions-generation-resource-integrated-database-egrid
# eia 923 data from here: https://www.eia.gov/electricity/data/eia923/
# cems data from here: ftp://newftp.epa.gov/DmDnLoad/emissions/hourly/monthly/
# easiur data from here: https://barney.ce.cmu.edu/~jinhyok/easiur/online/
# fuel_default_prices.xlsx compiled from data from https://www.eia.gov/
ferc714_part2_schedule6_csv = 'Part 2 Schedule 6 - Balancing Authority Hourly System Lambda.csv'
ferc714IDs_csv='Respondent IDs.csv'
cems_folder_path ='C:\\Users\\mattb\\Documents\\GitHub\\simple_dispatch'
easiur_csv_path ='egrid_2016_plant_easiur.csv'
fuel_commodity_prices_xlsx = 'fuel_default_prices.xlsx'
if run_year == 2017:
    egrid_data_xlsx = 'egrid2016_data.xlsx'
    eia923_schedule5_xlsx = 'EIA923_Schedules_2_3_4_5_M_12_2017_Final_Revision.xlsx'
if run_year == 2016:
    egrid_data_xlsx = 'egrid2016_data.xlsx'
    eia923_schedule5_xlsx = 'EIA923_Schedules_2_3_4_5_M_12_2016_Final_Revision.xlsx'
if run_year == 2015:
    egrid_data_xlsx = 'egrid2014_data.xlsx'
    eia923_schedule5_xlsx = 'EIA923_Schedules_2_3_4_5_M_12_2015_Final_Revision.xlsx'
if run_year == 2014:
    egrid_data_xlsx = 'egrid2014_data.xlsx'
    eia923_schedule5_xlsx = 'EIA923_Schedules_2_3_4_5_M_12_2014_Final_Revision.xlsx'
#loop through nerc regions
#for nerc_region in ['TRE']:
for nerc_region in [ 'NPCC']:
    try:
        #if you've already run generatorData before, there will be a shortened pickled dictionary that we can just load in now. The 2017 pickled dictionaries can be downloaded from the simple_dispatch github repository. You can also download cems data and compile them using the generatorData object
        with open('generator_data_short_%s_%s.obj'%(nerc_region, str(run_year)), 'rb') as file:
            gd_short = pickle.load(file)
            gd_short.df.columns

    except:
        #run the generator data object
        gd = generatorData(nerc_region, egrid_fname=egrid_data_xlsx, eia923_fname=eia923_schedule5_xlsx, ferc714IDs_fname=ferc714IDs_csv, ferc714_fname=ferc714_part2_schedule6_csv, cems_folder=cems_folder_path, easiur_fname=easiur_csv_path, include_easiur_damages=True, year=run_year, fuel_commodity_prices_excel_dir=fuel_commodity_prices_xlsx, hist_downtime=False, coal_min_downtime = 12, cems_validation_run=False)
        #pickle the trimmed version of the generator data object
        gd_short = {'year': gd.year, 'nerc': gd.nerc, 'hist_dispatch': gd.hist_dispatch, 'demand_data': gd.demand_data, 'mdt_coal_events': gd.mdt_coal_events, 'df': gd.df}

        pickle.dump(gd_short, open('generator_data_short_%s_%s.obj'%(nerc_region, str(run_year)), 'wb'))
    #now that we have the generator data cleaned up, we can build the merit order and run the dispatch
    #we can add a co2 price to the dispatch calculation
