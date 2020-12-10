# satrack
Simple tool to track satellites when doing radio astronomy

Given
- Observatory location (lat, long, elevation)
- RA/DEC of source of interest
- epoch of observation

Takes TLE of a satellite, computes Alt,Az of the satellite and compares it with Alt,Az of the source of interest in the epoch of observation.

If the angular separation is less than `MIN_ANG_SEP`, the TLE is recorded.

## working

Download some TLEs. 
Convert TLEs to pandas.DataFrame using `pickler.py`
Edit `satrack.py` to your liking

Run `satrack.py`

