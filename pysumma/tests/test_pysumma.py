import os
import pathlib
import pytest
import pysumma as ps
import shutil
import xarray as xr

EXE = 'summa.exe'
RUN_METHOD = 'local'
ROOT = f'{pathlib.Path(__file__).parent.absolute()}/data/summa_setup_template'


def write_file_manager():
    with open(f'{ROOT}/template_file_manager.txt') as f:
        lines = f.readlines()
    with open(f'{ROOT}/file_manager.txt', 'w') as f:
        lines = [l.replace('PWD', f'{ROOT}') for l in lines]
        f.writelines(lines)
            

def test_file_manager():
    write_file_manager()
    fm = ps.FileManager(f'{ROOT}/file_manager.txt')
    assert type(fm) == ps.FileManager
    assert type(fm.decisions) == ps.Decisions
    assert type(fm.output_control) == ps.OutputControl
    assert type(fm.global_hru_params) == ps.GlobalParams
    assert type(fm.global_gru_params) == ps.GlobalParams
    assert type(fm.force_file_list) == ps.ForcingList
    assert type(fm.local_attributes) == xr.Dataset
    assert type(fm.trial_params) == xr.Dataset
    assert type(fm.initial_conditions) == xr.Dataset
    assert fm.genparm is not None
    assert fm.mptable is not None
    assert fm.soilparm is not None
    assert fm.vegparm is not None


def test_decisions():
    meta = ps.decisions.DECISION_META
    dec = ps.Decisions(f'{ROOT}/settings/decisions.txt')
    for o in dec.list_options():
        assert dec[o].value in dec[o].available_options
        for val in dec[o].available_options:
            dec[o] = val
            assert dec[o].value == val


def test_force_file_list():
    ffl = ps.ForcingList(f'{ROOT}/forcings/forcing_file_list.txt')
    assert len(ffl.forcing_data) == 1
    ds = ffl.open_forcing_data()[0]
    assert type(ds) == xr.Dataset
    assert 'SWRadAtm' in ds
    assert 'time' in ds.dims
    assert 'hru' in ds.dims


def test_output_control():
    oc = ps.OutputControl(f'{ROOT}/settings/output_control.txt')
    assert len(oc.list_options()) == 5
    assert oc['scalarSWE'].statistic == 'instant'
    assert oc['scalarSWE'].period == 1
    oc['scalarSWE'] = {'period': 24, 'sum': 1,
                      'instant': 0, 'mean': 0,
                      'min':0, 'max':0, 'mode':0}
    assert oc['scalarSWE'].statistic == 'sum'
    assert oc['scalarSWE'].period == 24


def test_global_params():
    hru_params = ps.GlobalParams(f'{ROOT}/params/local_param_info.txt')
    gru_params = ps.GlobalParams(f'{ROOT}/params/basin_param_info.txt')
    print(hru_params['tempCritRain'])
    assert hru_params['tempCritRain'].value[0] == 273.16


def test_simulation():
    write_file_manager()
    fman = f'{ROOT}/file_manager.txt'
    sim = ps.Simulation(EXE, fman)
    sim.run(RUN_METHOD)
    assert sim.status == 'Success', sim.stdout
    ds = sim.output
    assert type(ds) == xr.Dataset
    assert 'scalarSWE' in ds
    os.remove(f'{ROOT}/output/template_output_pysumma_run_timestep.nc')


def test_ensemble():
    write_file_manager()
    fman = f'{ROOT}/file_manager.txt'
    config = {'run0': {'trial_parameters': {'tempCritRain': 263.16}},
              'run1': {'trial_parameters': {'tempCritRain': 283.16}},}
    ens = ps.Ensemble(EXE, config, fman, num_workers=2)
    ens.run(RUN_METHOD)
    assert len(ens.summary()['Success']) == 2
    out = ens.open_output()
    assert type(out['run0']) == xr.Dataset
    assert (out['run0']['scalarSWE'].mean(dim='time') 
            < out['run1']['scalarSWE'].mean(dim='time'))
    os.remove(f'{ROOT}/output/template_output_run0_timestep.nc')
    os.remove(f'{ROOT}/output/template_output_run1_timestep.nc')
 


def test_ostrich():
    pass


def test_cleanup():
    shutil.rmtree(f'{ROOT}/.pysumma')