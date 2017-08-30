import numpy as np
import pandas as pd
import extract_pupil_features as epf
import extract_running_features as err

def get_grating_specific_traces(exp, raw, binned=False):

    '''
    Arguments:
    ---------------------------------------------------------------------------
    exp: Individual experiment object loaded from the brain observatory
    raw: Boolean. False for df/f calcium signal. True for raw fluroescence trace
    Returns:
    ----------------------------------------------------------------------------
    output: Dictionary containing the following fields
        fluorescence: data frame object containing the trial sorted responses for all
        static grating activity in the given experiment session. Each element in the
        data frame is an array with dims cells X time
        pupil size: A data frame object containing the trial sorted pupil size for all
        different natural scenes presented
        pupil location: A data frame object containing the trial sorted pupil location for all
        different natural scenes presented
        running speed: A data frame object containing the trial sorted running speed for all
        different natural scenes presented
        time: A data frame object containing the trial sorted times stamps for all
        different natural scenes presented. Aligns with the previous dictionary fields
    cell_ids: numpy array containing unique cell ids. Index of cell id matches
    with row of cell X time matrix contained inside the fluroescence field of the
    output dictionary
    '''

    cell_ids = exp.get_cell_specimen_ids()
    if raw:
        t, dff = exp.get_fluorescence_traces()  # Read in calcium signal
    else:
        t, dff = exp.get_dff_traces()        # Read in calcium signal

    pr = exp.get_pupil_size()
    pr = pr[1]
    t, pl = exp.get_pupil_location(as_spherical = False)
    t, rs = exp.get_running_speed()
    p_rate, _ = extract_smooth_pupil_rate(exp)
    sac_rate = extract_smooth_saccade_rate(exp)

    stim_table = exp.get_stimulus_table('static_gratings')

    stim_id = []
    for i, s in enumerate(stim_table['orientation']):
        stim_id.append(",".join([str(stim_table['orientation'][i]), str(stim_table['spatial_frequency'][i]),
                                     str(stim_table['phase'][i])]))
    stim_table['id'] = stim_id # add column with unique id

    stim_ids = list(set(stim_id)) # make list of all possible unique ids
    columns = stim_ids
    df = pd.DataFrame([], index = range(0,50), columns = columns)
    pr_df = pd.DataFrame([], index = range(0,50), columns = columns)
    t_df = pd.DataFrame([], index = range(0,50), columns = columns)
    pl_df = pd.DataFrame([], index = range(0,50), columns = columns)
    rs_df = pd.DataFrame([], index = range(0,50), columns = columns)
    p_rate_df = pd.DataFrame([], index = range(0,50), columns = columns)
    sac_rate_df = pd.DataFrame([], index = range(0,50), columns = columns)


    if binned:
        for j, us in enumerate(stim_ids):
            start = stim_table['start'][stim_table['id']==us].values
            end = stim_table['end'][stim_table['id']==us].values

            for i in range(0, len(start)):
                    df[us][i]= np.mean((dff[:,start[i]:end[i]]), axis=1)
                    pr_df[us][i] = np.nanmean(pr[start[i]:end[i]])
                    pl_df[us][i] = np.nanmean(pl[start[i]:end[i], :], axis = 0)
                    t_df[us][i] = np.nanmean(t[start[i]:end[i]])
                    rs_df[us][i] = np.nanmean(rs[start[i]:end[i]])
                    p_rate_df[us][i] = np.nanmean(p_rate[start[i]:end[i]])
                    sac_rate_df[us][i] = np.nanmean(sac_rate[start[i]:end[i]])

    else:
        for j, us in enumerate(stim_ids):
            start = stim_table['start'][stim_table['id']==us].values
            end = stim_table['end'][stim_table['id']==us].values

            for i in range(0, len(start)):
                    df[us][i]=(dff[:,start[i]:end[i]])
                    pr_df[us][i] = pr[start[i]:end[i]]
                    pl_df[us][i] = pl[start[i]:end[i], :]
                    t_df[us][i] = t[start[i]:end[i]]
                    rs_df[us[i]] = rs[start[i]:end[i]]
                    p_rate_df[us][i] = (p_rate[start[i]:end[i]])
                    sac_rate_df[us][i] = (sac_rate[start[i]:end[i]])
    output = dict()
    output['fluorescence'] = df
    output['pupil size'] = pr_df
    output['pupil location'] = pl_df
    output['time'] = t_df
    output['running speed'] = rs_df
    output['pupil rate'] = p_rate_df
    output['saccade rate'] = sac_rate_df
    return output, cell_ids

def get_spont_specific_fluorescence_traces(exp, raw, binned=False):
    '''
    Arguments:
    ---------------------------------------------------------------------------
    exp: Individual experiment object loaded from the brain observatory
    raw: Boolean. False for df/f calcium signal. True for raw fluroescence trace
    Returns:
    ----------------------------------------------------------------------------
    output: Dictionary containing the following fields
        fluorescence: data frame object containing the trial sorted responses for all
        spontaeuous activity in the given experiment session. Each element in the
        data frame is an array with dims cells X time
        pupil size: A data frame object containing the trial sorted pupil size for all
        different natural scenes presented
        pupil location: A data frame object containing the trial sorted pupil location for all
        different natural scenes presented
        running speed: A data frame object containing the trial sorted running speed for all
        different natural scenes presented
        time: A data frame object containing the trial sorted times stamps for all
        different natural scenes presented. Aligns with the previous dictionary fields
    cell_ids: numpy array containing unique cell ids. Index of cell id matches
    with row of cell X time matrix contained inside the fluroescence field of the
    output dictionary
    '''

    cell_ids = exp.get_cell_specimen_ids()
    if raw:
        t, dff = exp.get_fluorescence_traces()  # Read in calcium signal
    else:
        t, dff = exp.get_dff_traces()        # Read in calcium signal

    pr = exp.get_pupil_size()
    pr = pr[1]
    t, pl = exp.get_pupil_location(as_spherical = False)
    t, rs = exp.get_running_speed()
    p_rate, _ = extract_smooth_pupil_rate(exp)
    sac_rate = extract_smooth_saccade_rate(exp)

    stim_table = exp.get_spontaneous_activity_stimulus_table()
    dff_temp = pr_temp = t_temp = pl_temp = rs_temp = p_rate_temp = sac_rate_temp = dict()

    dff_temp['spont'] = pr_temp['spont'] = pl_temp['spont'] = t_temp['spont'] = t_temp['spont'] = rs_temp['spont'] = p_rate_temp['spont'] = sac_rate_temp['spont'] = []

    if binned:
        for i in range(0,len(stim_table['start'].values)):
            start = stim_table['start'][i]
            end = stim_table['end'][i]
            dff_temp['spont'].append(np.nanmean(dff[:,start:end],axis=1))
            pr_temp['spont'].append(np.nanmean(pr[start:end]))
            pl_temp['spont'].append(np.nanmean(pl[start:end,:],axis=0))
            t_temp['spont'].append(np.nanmean(t[start:end]))
            rs_temp['spont'].append(np.nanmean(rs[start:end]))
            p_rate_temp['spont'].append(np.nanmean(p_rate[start:end]))
            sac_rate_temp['spont'].append(np.append(sac_rate[start:end]))
    else:
        for i in range(0, len(stim_table['start'].values)):
            start = stim_table['start'][i]
            end = stim_table['end'][i]
            dff_temp['spont'].append(dff[:,start:end])
            pr_temp['spont'].append(pr[start:end])
            pl_temp['spont'].append(pl[start:end,:])
            t_temp['spont'].append(t[start:end])
            rs_temp['spont'].append(rs[start:end])
            rs_temp['spont'].append(np.nanmean(rs[start:end]))
            p_rate_temp['spont'].append((p_rate[start:end]))
            sac_rate_temp['spont'].append((sac_rate[start:end]))

    output = dict()
    columns = sorted(dff_temp.keys())
    output['fluorescence'] = pd.DataFrame(data=dff_temp, columns=columns)
    columns = sorted(pr_temp.keys())
    output['pupil size'] = pd.DataFrame(data=pr_temp, columns=columns)
    output['time']= pd.DataFrame(data=t_temp, columns = columns)
    output['pupil location'] = pd.DataFrame(data=pl_temp, columns = columns)
    output['running speed'] = pd.DataFrame(data = rs_temp, columns = columns)
    output['pupil rate'] = pd.DataFrame(data = p_rate_temp, columns = columns)
    output['saccade rate'] = pd.DataFrame(data = sac_rate_temp, columns = columns)

    return output, cell_ids

def get_ns_specific_fluorescence_traces(exp, raw, binned = False):

    '''
    Arguments:
    ---------------------------------------------------------------------------
    exp: Individual experiment object loaded from the brain observatory
    raw: Boolean. False for df/f calcium signal. True for raw fluroescence trace
    Returns:
    ----------------------------------------------------------------------------
    output: Dictionary containing the following fields
        fluorescence: data frame object containing the trial sorted responses for all
        natural scenes activity in the given experiment session. Each element in the
        data frame is an array with dims cells X time
        pupil size: A data frame object containing the trial sorted pupil size for all
        different natural scenes presented
        pupil location: A data frame object containing the trial sorted pupil location for all
        different natural scenes presented
        running speed: A data frame object containing the trial sorted running speed for all
        different natural scenes presented
        time: A data frame object containing the trial sorted times stamps for all
        different natural scenes presented. Aligns with the previous dictionary fields
    cell_ids: numpy array containing unique cell ids. Index of cell id matches
    with row of cell X time matrix contained inside the fluroescence field of the
    output dictionary
    '''

    cell_ids = exp.get_cell_specimen_ids()

    if raw:
        t, dff = exp.get_fluorescence_traces()  # Read in calcium signal
    else:
        t, dff = exp.get_dff_traces()        # Read in calcium signal

    pr = exp.get_pupil_size()
    pr = pr[1]
    t, pl = exp.get_pupil_location(as_spherical = False)
    t, rs = exp.get_running_speed()
    p_rate, _ = extract_smooth_pupil_rate(exp)
    sac_rate = extract_smooth_saccade_rate(exp)

    stim = 'natural_scenes'
    stim_table = exp.get_stimulus_table(stim)
    unique_stim = np.sort(exp.get_stimulus_table('natural_scenes')['frame'].unique(), axis=None)

    dff_temp = pr_temp = t_temp = pl_temp = rs_temp = p_rate_temp = sac_rate_temp =dict()

    if binned:
        for i, u_s in enumerate(unique_stim):
            start = stim_table['start'][stim_table['frame']==u_s].values
            end = start + 7#stim_table['end'][stim_table['frame']==u_s].values
            dff_temp[u_s] = pr_temp[u_s] = pl_temp[u_s] = t_temp[u_s] = rs_temp[u_s] = p_rate_temp[u_s] = sac_rate_temp[u_s] = []

            for j in range(0, len(start)):
                    dff_temp[u_s].append(np.nanmean(dff[:,start[j]:end[j]], axis = 1))
                    pr_temp[u_s].append(np.nanmean(pr[start[j]:end[j]]))
                    pl_temp[u_s].append(np.nanmean(pl[start[j]:end[j], :], axis=0))
                    t_temp[u_s].append(np.nanmean(t[start[j]:end[j]]))
                    rs_temp[u_s].append(np.nanmean(rs[start[j]:end[j]]))
                    p_rate_temp[u_s].append(np.nanmean(p_rate[start[j]:end[j]]))
                    sac_rate_temp[u_s].append(np.nanmean(sac_rate[start[j]:end[j]]))

    else:
        for i, u_s in enumerate(unique_stim):
            start = stim_table['start'][stim_table['frame']==u_s].values
            end = start + 7#stim_table['end'][stim_table['frame']==u_s].values
            dff_temp[u_s] = pr_temp[u_s] = pl_temp[u_s] = t_temp[u_s] = rs_temp[u_s] = p_rate_temp[u_s] = sac_rate_temp[u_s] = []
            for j in range(0, len(start)):
                    dff_temp[u_s].append(dff[:,start[j]:end[j]])
                    pr_temp[u_s].append(pr[start[j]:end[j]])
                    pl_temp[u_s].append(pl[start[j]:end[j], :])
                    t_temp[u_s].append(t[start[j]:end[j]])
                    rs_temp[u_s].append(rs[start[j]:end[j]])
                    p_rate_temp[u_s].append((p_rate[start[j]:end[j]]))
                    sac_rate_temp[u_s].append((sac_rate[start[j]:end[j]]))
    output = dict()
    columns = sorted(dff_temp.keys())
    output['fluorescence'] = pd.DataFrame(data=dff_temp, columns=columns)
    columns = sorted(pr_temp.keys())
    output['pupil size'] = pd.DataFrame(data=pr_temp, columns = columns)
    output['time'] = pd.DataFrame(data=t_temp, columns = columns)
    output['pupil location'] = pd.DataFrame(data=pl_temp, columns = columns)
    output['running speed'] = pd.DataFrame(data= rs_temp, columns = columns)
    output['pupil rate'] = pd.DataFrame(data= p_rate_temp, columns = columns)
    output['saccade rate'] = pd.DataFrame(data= sac_rate_temp, columns = columns)
    return output, cell_ids

def get_ns_dff_by_trial(exp, cell_specimen_ids=None):
    if cell_specimen_ids is None:
        cell_specimen_ids = exp.get_cell_specimen_ids()

    t, dff = exp.get_dff_traces(cell_specimen_ids=cell_specimen_ids)        # Read in calcium signal

    stim = 'natural_scenes'
    stim_table = exp.get_stimulus_table(stim)
    unique_stim = np.sort(exp.get_stimulus_table('natural_scenes')['frame'].unique(), axis=None)
    dff_temp = dict()
    for i, u_s in enumerate(unique_stim):
        start = stim_table['start'][stim_table['frame']==u_s].values
        end = start + 7#stim_table['end'][stim_table['frame']==u_s].values
        dff_temp[u_s] = []
        for j in range(0, len(start)):
                dff_temp[u_s].append(dff[:,start[j]:end[j]])
    columns = sorted(dff_temp.keys())
    dff_df = pd.DataFrame(data=dff_temp, columns=columns)
    return dff_df
