import pandas as pd
from influxdb import InfluxDBClient

def query_iot_data(db, query_start_time, query_end_time, nid, channels_list=None):
    
    query_start_time_str = query_start_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    query_end_time_str   = query_end_time.strftime("%Y-%m-%d %H:%M:%S.%f")

    client_gen3 = InfluxDBClient(host=db.host, port=db.port, database=db.database)
    
    try:
        channels_str = "|".join(channels_list)
        q = f""" SELECT W, nid, channel FROM "{db.source_table}" WHERE ("nid" = '{nid}') and ("channel" =~ /^({channels_str})$/) and (time >= '{query_start_time_str}') and (time < '{query_end_time_str}')"""

    except:
        
        q = f""" SELECT W, nid, channel FROM "{db.source_table}" WHERE ("nid" = '{nid}') and (time >= '{query_start_time_str}') and (time < '{query_end_time_str}')"""
    
    results_gen3 = client_gen3.query(q)

    df = pd.DataFrame(results_gen3.get_points())
    
    # df_ti = df.set_index('time')
    if df.shape[0] > 0:
        return df
    else:
        df = pd.DataFrame({'time': pd.Series(dtype='str'),
                       'W': pd.Series(dtype='float'),
                       'nid': pd.Series(dtype='str'),
                          'channel':pd.Series(dtype='str')})
        return df

def db_read_query(db, query_start_time, query_end_time, df_meta,
                  meta_columns_for_join = ['nid', 'channel_number']):
    
    nids_groups = df_meta.groupby([meta_columns_for_join[0]])
    
    df_iot_all = pd.DataFrame([])
    
    for nid, groups in nids_groups:
        
        df_iot_nid = query_iot_data(db, query_start_time, query_end_time, nid, channels_list=groups[meta_columns_for_join[1]].to_list())
        df_iot_all = pd.concat([df_iot_all, df_iot_nid])


    df_iot_all.time = pd.to_datetime(df_iot_all.time)
    df_iot_all_ti = df_iot_all.set_index('time')

    return df_iot_all_ti

    
