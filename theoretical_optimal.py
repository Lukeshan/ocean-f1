import matplotlib.pyplot as plt
import pandas as pd
import fastf1.plotting

fastf1.Cache.enable_cache('cache')

# fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

# Key Variables

driver_code = 'RUS'
season_year = 2025
season_round = 5
session_type = "R"

mini_sector_length = 100

session = fastf1.get_session(season_year, season_round, session_type)
session.load()
circuit_info = session.get_circuit_info()

# Pick driver
laps_raw_df = session.laps.pick_drivers(driver_code)
laps_df = laps_raw_df[['LapNumber','Stint','PitOutTime','PitInTime','Compound','TyreLife','LapStartDate','TrackStatus','Deleted','DeletedReason']].copy()
car_data_df = pd.DataFrame(columns=['LapNumber','Date', 'RPM', 'Speed', 'nGear', 'Throttle', 'Brake', 'DRS', 'Source', 'Time', 'SessionTime', 'Distance'])
for lap_index in range(0,laps_df.shape[0]):
    lap_data_df = laps_raw_df.iloc[lap_index].get_car_data().add_distance()
    lap_data_df = lap_data_df.drop(["Source","Time","SessionTime"], axis = 1)
    lap_data_df["DRS"] = lap_data_df["DRS"].isin([10,12,14])
    lap_data_df["LapNumber"] = lap_index+1
    car_data_df = lap_data_df if lap_index == 0 else pd.concat([car_data_df,lap_data_df], ignore_index=True)

circuit_length = car_data_df["Distance"].max()
mini_sector_count = (circuit_length // mini_sector_length)
mini_sector_count = mini_sector_count + 1 if not mini_sector_count else 0
car_data_df["MiniSectorNumber"] = car_data_df["Distance"] // mini_sector_length
car_data_df["MiniSectorNumber"] = car_data_df["MiniSectorNumber"].apply(lambda m_s: m_s if m_s else 1)

#specify path for export
path = r'cache\\laps_df_export.txt'

# export DataFrame to text file
with open(path, 'w') as f:
    df_string = car_data_df.to_string(header=True, index=True)
    f.write(df_string)