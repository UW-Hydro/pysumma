import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import calendar

EB_COMPONENTS = ['scalarNetRadiation', 'scalarLatHeatTotal',
                 'scalarSenHeatTotal', 'scalarCanairNetNrgFlux',
                 'scalarCanopyNetNrgFlux', 'scalarGroundNetNrgFlux']
EB_LONGNAMES = ['Net radiation', 'Latent heat', 'Sensible heat',
                'Canopy airspace flux', 'Canopy flux', 'Ground flux']


def _determine_suffix(ds):
    suffix = ''
    for var in list(ds.keys()):
        if var.startswith(EB_COMPONENTS[0]):
            if var == EB_COMPONENTS[0]:
                return suffix
            else:
                return var.replace(EB_COMPONENTS[0], '_')
    else:
        raise KeyError('Could not locate all variables necessary '
                       'for calculating energy balances! The '
                       f'required variables are {", ".join(EB_COMPONENTS)}')


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


def monthly_energy_balance(ds: xr.Dataset, year: int,
                           agg_dims: list=None) -> pd.DataFrame:
    suffix = _determine_suffix(ds)
    wy_slice = slice(f'10-01-{year-1}', f'9-30-{year}')
    time_group = ds.sel(time=wy_slice).time.dt.month
    wb_monthly = ds.sel(time=wy_slice).groupby(time_group).sum(dim=['time'])
    wb_monthly[f'scalarNetRadiation{suffix}'].values = (
            calc_monthly_sum(ds[f'scalarNetRadiation{suffix}'], year))
    wb_monthly[f'scalarLatHeatTotal{suffix}'].values = (
            calc_monthly_sum(ds[f'scalarLatHeatTotal{suffix}'], year))
    wb_monthly[f'scalarSenHeatTotal{suffix}'].values = (
            calc_monthly_sum(ds[f'scalarSenHeatTotal{suffix}'], year))
    wb_monthly[f'scalarCanairNetNrgFlux{suffix}'].values = (
            calc_monthly_sum(-ds[f'scalarCanairNetNrgFlux{suffix}'], year))
    wb_monthly[f'scalarCanopyNetNrgFlux{suffix}'].values = (
            calc_monthly_sum(-ds[f'scalarCanopyNetNrgFlux{suffix}'], year))
    wb_monthly[f'scalarGroundNetNrgFlux{suffix}'].values = (
            calc_monthly_sum(-ds[f'scalarGroundNetNrgFlux{suffix}'], year))

    wb_monthly = wb_monthly[EB_COMPONENTS]
    if agg_dims is not None:
        wb_monthly = wb_monthly.sum(dim=agg_dims)
    wb_df = wb_monthly.to_dataframe()
    wb_df.index -= 1
    return wb_df


def seasonal_energy_balance(ds: xr.Dataset, year: int,
                            agg_dims: list=None) -> pd.DataFrame:
    suffix = _determine_suffix(ds)
    wy_slice = slice(f'11-30-{year-1}', f'12-31-{year}')
    time_group = ds.sel(time=wy_slice).time.dt.season
    wb_seasonal = ds.sel(time=wy_slice).groupby(time_group).sum(dim=['time'])
    wb_seasonal[f'scalarNetRadiation{suffix}'].values = (
            calc_seasonal_sum(ds[f'scalarNetRadiation{suffix}'], year))
    wb_seasonal[f'scalarLatHeatTotal{suffix}'].values = (
            calc_seasonal_sum(ds[f'scalarLatHeatTotal{suffix}'], year))
    wb_seasonal[f'scalarSenHeatTotal{suffix}'].values = (
            calc_seasonal_sum(ds[f'scalarSenHeatTotal{suffix}'], year))
    wb_seasonal[f'scalarCanairNetNrgFlux{suffix}'].values = (
            calc_seasonal_sum(-ds[f'scalarCanairNetNrgFlux{suffix}'], year))
    wb_seasonal[f'scalarCanopyNetNrgFlux{suffix}'].values = (
            calc_seasonal_sum(-ds[f'scalarCanopyNetNrgFlux{suffix}'], year))
    wb_seasonal[f'scalarGroundNetNrgFlux{suffix}'].values = (
            calc_seasonal_sum(-ds[f'scalarGroundNetNrgFlux{suffix}'], year))

    wb_seasonal = wb_seasonal[EB_COMPONENTS]
    if agg_dims is not None:
        wb_seasonal = wb_seasonal.sum(dim=agg_dims)
    wb_df = wb_seasonal.to_dataframe()
    return wb_df


def energy_balance(ds, start_year, end_year, how='seasonal',
                   ax=None, legend=True):
    if how not in ['seasonal', 'monthly']:
        raise NotImplementedError()
    s_df = []
    if how == 'seasonal':
        for year in np.arange(start_year, end_year):
            s_df.append(seasonal_energy_balance(ds, year))
        s_df = pd.concat(s_df).groupby('season').mean()
        months = ['Winter', 'Spring', 'Summer', 'Fall']
    elif how == 'monthly':
        for year in np.arange(start_year, end_year):
            s_df.append(monthly_energy_balance(ds, year))
        s_df = pd.concat(s_df).groupby('month').mean()
        months = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar',
                  'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
    s_df.columns = EB_LONGNAMES

    if not ax:
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
    s_df.plot(kind='bar', ax=ax,  stacked=True, legend=legend)
    plt.sca(ax)
    plt.xticks(np.arange(len(months)), months, rotation=45)

    ax.axhline(0, color='black', linewidth=2, label='')
    ax.set_xlabel('')
    ax.set_axisbelow(True)
    return ax
