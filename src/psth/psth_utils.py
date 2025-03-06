def download_data(url, filename):
    from pathlib import Path
    import owncloud

    client = owncloud.Client.from_public_link(url)
    client.get_file('/', filename)

    if Path(filename).exists():
        print('Download Succeeded.')

    return None

def extract_trials(filename):
    import xarray as xr
    dset = xr.load_dataset(filename)
    trials = dset[['contrast_left', 'contrast_right', 'stim_onset']].to_dataframe()
    return trials

def extract_spikes(filename):
    import xarray as xr
    dset = xr.load_dataset(filename)
    spikes = dset[['spike_trial', 'spike_cell', 'spike_time']].to_dataframe()
    return spikes

def extract_cells(filename):
    import xarray as xr
    dset = xr.load_dataset(filename)
    cells = dset['brain_groups'].to_dataframe()
    return cells

def merge_data(trials, cells, spikes):
    import pandas as pd
    merged = pd.merge(left=cells, left_index=True, right=spikes, right_on='spike_cell')
    merged = pd.merge(left=trials, right=merged, left_index=True, right_on='spike_trial').reset_index(drop=True)
    merged.columns
    merged = (merged
        .rename(columns=dict(
            brain_groups="brain_area",
            spike_trial="trial_id",
            spike_cell="cell_id",
            spike_time="time"
        ))
        [[
            'trial_id',
            'contrast_left',
            'contrast_right',
            'stim_onset',
            'cell_id',
            'brain_area',
            'time'
        ]]
        .astype(dict(   
            brain_area = 'category',
        ))
        # 
    )
    return merged

def compute_time_bins(time, bin_interval):
    import numpy as np
    time = np.round(time, decimals=6)  # Round time to the nearest microsecond, to reduce floating point errors.
    time_bins = np.floor(time /bin_interval) * bin_interval  # Round down to the nearest time bin start
    time_bins
    return time_bins

def compute_psths(data, time_bins, bin_interval):
    psth = (
    data
    .groupby([time_bins, 'trial_id', 'contrast_left', 'cell_id', 'brain_area'], observed=True, )
    .size()
    .rename('spike_count')
    .reset_index()
    )
    psth = (
    psth
    .groupby(['time', 'contrast_left', 'brain_area'], observed=True)
    .spike_count
    .mean()
    .rename('avg_spike_count')
    .reset_index()
    )
    psth['avg_spike_rate'] = psth['avg_spike_count'] * bin_interval
    return psth

def plot_psths(psth):
    import seaborn as sns
    g = sns.FacetGrid(data=psth, col='brain_area', col_wrap=2)
    g.map_dataframe(sns.lineplot, x='time', y='avg_spike_count', hue='contrast_left')
    g.add_legend()
    return g
