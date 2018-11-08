import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import calendar

SEC_PER_DAY = 86400
MM_PER_M = 1000
WB_COMPONENTS = ['scalarTotalRunoff', 'scalarGroundEvaporation', 'pptrate',
                 'scalarCanopyEvaporation', 'scalarCanopyTranspiration',
                 'scalarSnowSublimation', 'scalarCanopySublimation',
                 'scalarSWE', 'scalarTotalSoilWat', 'scalarCanopyWat']
WB_LONGNAMES = ['Evapotranspiration (ET)', 'Runoff', 'Precipitation',
                'Soil & canopy moisture',
                'Snow water equivalent (SWE)', 'Baseflow']


def _determine_suffix(ds):
    suffix = ''
    for var in list(ds.keys()):
        if var.startswith(WB_COMPONENTS[0]):
            if var == WB_COMPONENTS[0]:
                return suffix
            else:
                return var.replace(WB_COMPONENTS[0], '_')


def aggregate_wb_vars(ds):
    out_vars = ['evaporation', 'precipitation', 'runoff',
                'swe', 'soil_moisture', 'baseflow']  # , 'canopy_moisture']
    suffix = _determine_suffix(ds)
    ds = ds.where(ds['scalarTotalRunoff{}'.format(suffix)] > -100, drop=True)
    ds['precipitation'] = ds['pptrate{}'.format(suffix)] * SEC_PER_DAY
    ds['evaporation'] = - SEC_PER_DAY * (
            ds['scalarGroundEvaporation{}'.format(suffix)]
            + ds['scalarCanopyEvaporation{}'.format(suffix)]
            + ds['scalarCanopyTranspiration{}'.format(suffix)]
            + ds['scalarSnowSublimation{}'.format(suffix)]
            + ds['scalarCanopySublimation{}'.format(suffix)])
    ds['runoff'] = (ds['scalarTotalRunoff{}'.format(suffix)]
                     * SEC_PER_DAY * MM_PER_M)
    ds['baseflow'] = - SEC_PER_DAY * MM_PER_M * (
            ds['scalarAquiferBaseflow{}'.format(suffix)])
    ds['swe'] = ds['scalarSWE{}'.format(suffix)]
    ds['soil_moisture'] = (ds['scalarTotalSoilLiq{}'.format(suffix)]
                            + ds['scalarTotalSoilIce{}'.format(suffix)]
                            + ds['scalarCanopyIce{}'.format(suffix)]
                            + ds['scalarCanopyLiq{}'.format(suffix)])
    return ds[out_vars]


def calc_monthly_flux(da: xr.DataArray, year: int) -> xr.DataArray:
    """Calculates monthly change in a data array for a given year"""
    feb_end = 29 if calendar.isleap(year) else 28
    start = [f'9-30-{year-1}', f'10-31-{year-1}', f'11-30-{year-1}',
             f'12-31-{year-1}', f'01-31-{year}', f'02-{feb_end}-{year}',
             f'03-31-{year}', f'04-30-{year}', f'05-31-{year}',
             f'06-30-{year}', f'07-31-{year}', f'08-31-{year}']
    end = [f'10-31-{year-1}', f'11-30-{year-1}', f'12-31-{year-1}',
           f'01-31-{year}', f'02-{feb_end}-{year}', f'03-31-{year}',
           f'04-30-{year}', f'05-31-{year}', f'06-30-{year}',
           f'07-31-{year}', f'08-31-{year}', f'09-30-{year}']
    da = da.copy(deep=True).resample(time='D').mean()
    return np.array([da.sel(time=e).values - da.sel(time=s).values
                     for s, e in zip(start, end)])


def calc_monthly_sum(da: xr.DataArray, year: int) -> xr.DataArray:
    """Calculates monthly change in a data array for a given year"""
    feb_end = 29 if calendar.isleap(year) else 28
    start = [f'10-01-{year-1}', f'11-01-{year-1}', f'12-01-{year-1}',
             f'01-01-{year}', f'02-01-{year}', f'03-01-{year}',
             f'04-01-{year}', f'05-01-{year}', f'06-01-{year}',
             f'07-01-{year}', f'08-01-{year}', f'09-01-{year}']
    end = [f'10-31-{year-1}', f'11-30-{year-1}', f'12-31-{year-1}',
           f'01-31-{year}', f'02-{feb_end}-{year}', f'03-31-{year}',
           f'04-30-{year}', f'05-31-{year}', f'06-30-{year}',
           f'07-31-{year}', f'08-31-{year}', f'09-30-{year}']
    da = da.copy(deep=True).resample(time='D').mean()
    return np.array([da.sel(time=slice(s, e)).sum(dim='time')
                     for s, e in zip(start, end)])


def monthly_water_balance(ds: xr.Dataset, year: int,
                          agg_dims: list=None) -> pd.DataFrame:
    wb_vars = ['evaporation', 'runoff', 'precipitation',
               'soil_moisture', 'swe', 'baseflow']
    wy_slice = slice(f'10-01-{year-1}', f'9-30-{year}')
    time_group = ds.sel(time=wy_slice).time.dt.month

    wb_monthly = ds.sel(time=wy_slice).groupby(time_group).sum(dim=['time'])
    if agg_dims is not None:
        wb_monthly = wb_monthly[wb_vars].sum(dim=agg_dims)
    else:
        wb_monthly = wb_monthly[wb_vars]
        
    wb_monthly['swe'].values = calc_monthly_flux(ds['swe'], year)
    wb_monthly['soil_moisture'].values = (
            calc_monthly_flux(ds['soil_moisture'], year))
    wb_monthly['evaporation'].values = (
            calc_monthly_sum(ds['evaporation'], year))
    wb_monthly['runoff'].values = calc_monthly_sum(ds['runoff'], year)
    wb_monthly['baseflow'].values = calc_monthly_sum(ds['baseflow'], year)
    wb_monthly['precipitation'].values = (
            calc_monthly_sum(ds['precipitation'], year))

    wb_df = wb_monthly.to_dataframe()
    wb_df.index -= 1
    return wb_df


def calc_seasonal_flux(da: xr.DataArray, year: int) -> xr.DataArray:
    """Calculates seasonal change in a data array for a given year"""
    feb_end = 29 if calendar.isleap(year) else 28
    start = [f'12-01-{year-1}', f'03-01-{year}',
             f'06-01-{year}', f'08-31-{year}']
    end = [f'02-{feb_end}-{year}', f'05-31-{year}',
           f'08-31-{year}', f'11-30-{year}']
    da = da.copy(deep=True).resample(time='D').mean()
    return np.array([da.sel(time=e).values - da.sel(time=s).values
                     for s, e in zip(start, end)])


def calc_seasonal_sum(da: xr.DataArray, year: int) -> xr.DataArray:
    """Calculates seasonal change in a data array for a given year"""
    feb_end = 29 if calendar.isleap(year) else 28
    start = [f'12-01-{year-1}', f'03-01-{year}',
             f'06-01-{year}', f'09-01-{year}']
    end = [f'02-{feb_end}-{year}', f'05-31-{year}',
           f'08-31-{year}', f'11-30-{year}']
    da = da.copy(deep=True).resample(time='D').sum()
    return np.array([da.sel(time=slice(s, e)).sum(dim='time')
                     for s, e in zip(start, end)])


def seasonal_water_balance(ds: xr.Dataset, year: int,
                           agg_dims: list=None) -> pd.DataFrame:
    wb_vars = ['evaporation', 'runoff', 'precipitation',
               'soil_moisture', 'swe', 'baseflow']
    wy_slice = slice(f'11-30-{year-1}', f'12-31-{year}')
    time_group = ds.sel(time=wy_slice).time.dt.season
    wb_seasonal = ds.sel(time=wy_slice).groupby(time_group).sum(dim=['time'])
    
    if agg_dims is not None:
        wb_seasonal = wb_seasonal[wb_vars].sum(dim=agg_dims)
    else:
        wb_seasonal = wb_seasonal[wb_vars]
        
    wb_seasonal['swe'].values = calc_seasonal_flux(ds['swe'], year)
    wb_seasonal['soil_moisture'].values = (
            calc_seasonal_flux(ds['soil_moisture'], year))
    wb_seasonal['soil_moisture'].values += (
            calc_seasonal_sum(ds['evaporation'], year))
    wb_seasonal['runoff'].values = calc_seasonal_sum(ds['runoff'], year)
    wb_seasonal['baseflow'].values = calc_seasonal_sum(ds['baseflow'], year)
    wb_seasonal['precipitation'].values = (
            calc_seasonal_sum(ds['precipitation'], year))

    wb_df = wb_seasonal.to_dataframe()
    return wb_df


def water_balance(ds, start_year, end_year, how='seasonal',
                       ax=None, legend=True):
    if how not in ['seasonal', 'monthly']:
        raise NotImplementedError()
    s_df = []
    ds_agg = aggregate_wb_vars(ds)
    if how == 'seasonal':
        for year in np.arange(start_year, end_year):
            s_df.append(seasonal_water_balance(ds_agg, year, agg_dims=['hru']))
        s_df = pd.concat(s_df).groupby('season').mean()
        months = ['Winter', 'Spring', 'Summer', 'Fall']
    elif how == 'monthly':
        for year in np.arange(start_year, end_year):
            s_df.append(monthly_water_balance(ds_agg, year, agg_dims=['hru']))
        s_df = pd.concat(s_df).groupby('month').mean()
        months = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar',
                  'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
    s_df.columns = WB_LONGNAMES

    if not ax:
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
    s_df.plot(kind='bar', ax=ax,  stacked=True, legend=legend)
    plt.sca(ax)
    plt.xticks(np.arange(len(months)), months, rotation=45)

    ax.axhline(0, color='black', linewidth=2, label='')
    ax.set_xlabel('')
    ax.set_axisbelow(True)
    return ax
