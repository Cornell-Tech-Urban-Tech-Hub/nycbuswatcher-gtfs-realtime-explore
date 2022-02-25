# MTA Buswatcher
# GTFS-Realtime explorations
# 2021 may 16
# 2021 nov 12 update
# 2022 feb 11 update — no longer request geos / geopy
# 2022 feb 24 added parsers for alerts, updates

import os, time
import argparse
import requests
import datetime as dt
from google.transit import gtfs_realtime_pb2

from math import radians, cos, sin, asin, sqrt

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def parse_positions(feed, args):
    # if we are only tracking one vehicle
    if args.vehicle_id:
        # fix format and cast to string
        if args.vehicle_id < 1000:
            target_vehicle_id = f"_{str(args.vehicle_id)}"
        else:
            target_vehicle_id = str(args.vehicle_id)
            
        for entity in feed.entity:
            if entity.id[-4:] == target_vehicle_id:
                if args.verbose == True:
                    print(entity)
                else:
                    print(dt.datetime.fromtimestamp(entity.vehicle.timestamp),
                        entity.vehicle.trip.route_id,
                        f"\tbus {entity.vehicle.vehicle.id[-4:]}", 
                        entity.vehicle.position.latitude,
                        entity.vehicle.position.longitude
                        )        
    # if we are tracking all vehicles
    elif not args.vehicle_id:
        for entity in feed.entity:
            if args.verbose == True:
                print(entity)
            else:
                print(dt.datetime.fromtimestamp(entity.vehicle.timestamp),
                    entity.vehicle.trip.route_id, 
                    f"\tbus {entity.vehicle.vehicle.id[-4:]}", 
                    entity.vehicle.position.latitude,
                    entity.vehicle.position.longitude
                    )
    return

def parse_updates(feed, args):
    ## old code
    # for entity in feed.entity:
    #     if entity.HasField('trip_update'):
    #         print (entity.trip_update)
            
    ## new code            
    # if we are only tracking one vehicle
    if args.vehicle_id:
        # fix format and cast to string
        if args.vehicle_id < 1000:
            target_vehicle_id = f"_{str(args.vehicle_id)}"
        else:
            target_vehicle_id = str(args.vehicle_id)
            
        for entity in feed.entity:
            print('*',end = '')
            if entity.id[-4:] == target_vehicle_id:
                if args.verbose == True:
                    print(entity)
                else:
                    print(dt.datetime.fromtimestamp(entity.vehicle.timestamp),
                        entity.vehicle.trip.route_id,
                        f"\tbus {entity.vehicle.vehicle.id[-4:]}", 
                        entity.vehicle.position.latitude,
                        entity.vehicle.position.longitude
                        )        
    # if we are tracking all vehicles
    elif not args.vehicle_id:
        for entity in feed.entity:
            if args.verbose == True:
                print(entity)
            else:
                print(dt.datetime.fromtimestamp(entity.vehicle.timestamp),
                    entity.vehicle.trip.route_id, 
                    f"\tbus {entity.vehicle.vehicle.id[-4:]}", 
                    entity.vehicle.position.latitude,
                    entity.vehicle.position.longitude
                    )
    return



if __name__ == '__main__':

    # parse command options
    parser = argparse.ArgumentParser()
    parser.add_argument('--key',
                    required=True,
                    help='Your MTA developer API key')
    parser.add_argument('--feed',
                        choices=['updates', 'positions', 'alerts'],
                        required=True,
                        help='MTA Buses GTFS-Realtime feed to fetch (updates,positions,alerts)')
    parser.add_argument('--interval',
                    type=check_positive,
                    required=True,
                    help='Interval in seconds between grabs')
    parser.add_argument('--vehicle_id',
                        type=check_positive,
                        required=False,
                        help='Track single bus only, using provided vehicle_id')
    parser.add_argument('--verbose', 
                        dest='verbose', 
                        action='store_true',
                        help='Verbose tracking echo entire parsed record.')
    
    args = parser.parse_args()

    # make our urls
    endpoints =    { 'updates':'http://gtfsrt.prod.obanyc.com/tripUpdates?key={}',
                     'positions':'http://gtfsrt.prod.obanyc.com/vehiclePositions?key={}',
                     'alerts':'http://gtfsrt.prod.obanyc.com/alerts?key={}'
                     }
    base_url=endpoints[args.feed]
    api_key = args.key
    url = base_url.format(api_key)

    # parse and print
    feed = gtfs_realtime_pb2.FeedMessage()
    
    # 
    if args.vehicle_id:
        print(f'tracking bus {args.vehicle_id}')
    else:
        print("tracking all buses")

    # loop forever
    while 1:
        response = requests.get(url)
        feed.ParseFromString(response.content)

        if args.feed == 'updates':
            parse_updates(feed, args)

        elif args.feed == 'positions':
            parse_positions(feed, args)

        elif args.feed == 'alerts':
            for entity in feed.entity:
                print(entity)
            pass

        # wait until we fetch again
        time.sleep(args.interval)
