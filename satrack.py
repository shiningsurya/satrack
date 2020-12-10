# coding: utf-8
import sys
import tqdm
import numpy as np
import pandas as pd
from skyfield.api import load, Topos
from skyfield.api import EarthSatellite
import astropy.time as at
import astropy.units as au
import astropy.coordinates as asc
print ()
##################################
MIN_ANG_SEP = 1
epoch = at.Time ('2020-12-09T23:40:00',)
SRC   = asc.SkyCoord ('01h58m00.7502s', '65d43m00.3152s', frame='icrs')
lat   = asc.Angle('50d31m29s')
lon   = asc.Angle('6d52m58s')
elev  = 319
TLE   = "TLE_INFO.pkl"
OUT   = "NEAR_SOURCE.pkl"
##################################
eff_el= asc.EarthLocation(lat=lat, lon=lon, height=319)
AA    = asc.AltAz (location=eff_el, obstime=epoch)
SRCaa = SRC.transform_to (AA)
ALT, AZ = SRCaa.alt.value, SRCaa.az.value
print ("SOURCE AT ALT {0} AZ {1}".format(ALT, AZ))
##################################
df    = pd.read_pickle (TLE)
######################################
ts    = load.timescale ()
et    = ts.from_astropy (epoch)
loc   = Topos(latitude_degrees=lat.value,longitude_degrees=lon.value,elevation_m=elev)
D2R   = np.pi / 180.
def ang_sep (alt1,az1, alt2,az2):
    """
    https://space.stackexchange.com/questions/22044/angular-distance-between-two-satellites-given-azimuth-and-elevation-angles-for-e/22057
    """
    c_az_dif = np.cos (D2R * abs (az1 - az2))
    co_alt1  = D2R * ( 90 - alt1 )
    co_alt2  = D2R * ( 90 - alt2 )
    c_ca1, s_ca1 = np.cos (co_alt1), np.sin (co_alt1)
    c_ca2, s_ca2 = np.cos (co_alt2), np.sin (co_alt2)
    #
    rhs  = ( c_ca1 * c_ca2 ) + (s_ca1 * s_ca2 * c_az_dif)
    return np.arccos (rhs) / D2R
######################################
LIDX = []
for idx in tqdm.tqdm (df.index, desc='SAT'):
    tsat = df.loc[idx]
    sat   = EarthSatellite (tsat.line1, tsat.line2, tsat['name'], ts)
    diff  = sat - loc
    tt    = diff.at (et)
    alt,az,dist = tt.altaz ()
    sep   = ang_sep (alt.degrees, az.degrees, ALT, AZ)
    if sep <= MIN_ANG_SEP:
        print (sep)
        LIDX.append (idx)
######################################
print ("FOUND {0} SAT".format(len(LIDX)))
rf = pd.DataFrame (df.loc[LIDX])
print (rf)
rf.to_pickle (OUT)
# print (ang_sep (18.7, 121.5, 48.2, 218.7))


