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