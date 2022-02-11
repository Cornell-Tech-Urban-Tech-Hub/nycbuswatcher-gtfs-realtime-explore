Usage:

## requirements

`pip install requests gtfs-realtime-bindings`

An API key from the MTA

## usage

### Required arguments

`--key` Your meta developer API key (in quotes?)

`--feed` [positions, alerts, updates]

`--interval` [seconds to wait between fetches]

### Optional arguments

`--vehicle_id` Unique ID for a single vehicle to track. If you don't get any result on the feed=positions, try changing the `bus_id`.

## examples

Track positions for one line

`python gtfs-rt-test.py --feed=positions --interval=30 --vehicle_id=5870 --key='3nb42j4b23j4243bjb42j4b23j'`

Track positions for every line

`python gtfs-rt-test.py --feed=positions --interval=30 --key='3nb42j4b23j4243bjb42j4b23j'`


# sample positions record

```
id: "MTA NYCT_8440"
vehicle {
    trip {
    trip_id: "JA_B1-Sunday-120200_MISC_776"
    start_date: "20210516"
    route_id: "Q3"
    direction_id: 0
}
position {
    latitude: 40.660133361816406
    longitude: -73.77267456054688
    bearing: 20.289199829101562
}
timestamp: 1621210252
stop_id: "500158"
vehicle {
    id: "MTA NYCT_8440"
}
}
```