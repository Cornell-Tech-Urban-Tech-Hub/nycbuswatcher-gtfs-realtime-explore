Usage:

```
pip install gtfs-realtime-bindings
export API_KEY=<your MTA API key>
python3 gtfs-rt-test.py --feed=[positions, updates, alerts]
```


The most useful is `--feed=positions`

The script will only display one bus (set in `bus_id` at the top of `gtfs-rt-test.py`
If you don't get any result on the feed=positions, try changing the `bus_id`.

Remove that if statement on line 44 and 45 and it will print the whole streaming positions for all buses, this is what you would use for your map I think.



