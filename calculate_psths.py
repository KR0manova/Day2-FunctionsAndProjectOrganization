# %% Import library
from importlib import reload
import psth_utils
reload(psth_utils)
#from psth_utils import download_data

# %% Script Parameters

url = 'https://uni-bonn.sciebo.de/s/oTfGigwXQ4g0raW'
filename = 'data.nc'

# %% Download Data
# Exercise (Example): Make a download_data(url, filename) function:
reload(psth_utils)
psth_utils.download_data(url=url, filename=filename)

# %% Load Data
# Exercise: Make a `load_data(filename)` function, returning the `dset` variable.

# %% Extract Experiment-Level Data
# Exercise: Make an `extract_trials(filename)` function, returning the `trials` variable.
    
#dset = xr.load_dataset(filename)
#trials = dset[['contrast_left', 'contrast_right', 'stim_onset']].to_dataframe()
#trials
reload(psth_utils)
trials = psth_utils.extract_trials(filename)
#trials = extract_trials(filename)
print(trials)

# %% Extract Spike-Time Data
# Exercise: Make an `extract_spikes(filename)` function, returning the `spikes` variable.

reload(psth_utils)
spikes = psth_utils.extract_spikes(filename)
#dset = xr.load_dataset(filename)
#spikes = dset[['spike_trial', 'spike_cell', 'spike_time']].to_dataframe()
#spikes
print(spikes)


# %% Extract Cell-Level Data
# Exercise: Make an `extract_cells(filename)` function, returning the `cells` variable.

reload(psth_utils)
cells=psth_utils.extract_cells(filename)
print(cells)

# %% Merge and Compress Extracted Data
# Exercise: Make a `merge_data(trials, cells, spikes)` function, returning the `merged` variable.

reload(psth_utils)
merged=psth_utils.merge_data(trials, cells, spikes)
merged.info()


# %% Calculate Time Bins for PSTH
# Exercise: Make a `compute_time_bins(time, bin_interval)` function, returning the `time_bins` variable.

reload(psth_utils)

time = merged['time']
bin_interval = 0.05

time_bins=psth_utils.compute_time_bins(time, bin_interval)
print(time_bins)

# %% filter out stimuli with contrast on the right.
# No function needed here for this exercise.

filtered = merged[merged['contrast_right'] == 0]
print(f"Filtered out {len(merged) - len(filtered)} ({len(filtered) / len(merged):.2%}) of spikes in dataset.")
filtered

# %% Make PSTHs
# Exercise: Make a `compute_psths(data, time_bins)` function here, returning the `psth` variable.

reload(psth_utils)
psth=psth_utils.compute_psths(filtered, time_bins, bin_interval)
psth


# %% Plot PSTHs
# Make a `plot_psths(psth)` function here, returning the `g` variable.

reload(psth_utils)

g=psth_utils.plot_psths(psth)
g
g.savefig('PSTHs.png')


# %%
