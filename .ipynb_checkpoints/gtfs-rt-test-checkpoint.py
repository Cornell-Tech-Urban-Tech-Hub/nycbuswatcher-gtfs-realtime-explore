# MTA Buswatcher
# GTFS-Realtime explorations
# 2021 may 16
# 2021 nov 12 update

# config
bus_id = '5370'

# sample data
#

'''
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
'''

import os, time
import argparse
import requests
import datetime
from google.transit import gtfs_realtime_pb2
from geopy.distance import geodesic

def parse_positions(feed):
    buses={}
    for entity in feed.entity:
        if entity.id == f'MTABC_{bus_id}':
            print(entity)
        buses[str(entity.id)[-4:]]=(entity.vehicle.position.latitude,entity.vehicle.position.longitude,entity.vehicle.timestamp)
    return buses

def show_delta(new_positions,old_positions):
    for id,new_position_data in new_positions.items():
        if id == bus_id:

            try:
                old_position=old_positions[id]
                coords_1 = (old_position[0], old_position[1])
                coords_2 = (new_position_data[0], new_position_data[1])
                distance_traveled=geodesic(coords_1, coords_2).meters

                # t1=datetime.datetime.utcfromtimestamp(old_position[2])
                # t2=datetime.datetime.utcfromtimestamp(new_position_data[2])
                # time_delta=t2-t1
                if distance_traveled > 0:
                    print ('At {}, I saw bus #{} at {},{} which was {} meters from before.'.format(
                                datetime.datetime.utcfromtimestamp(new_position_data[2]).strftime('%Y-%m-%d %H:%M:%S'),
                                id,
                                new_position_data[0],
                                new_position_data[1],
                                distance_traveled
                            )
                           )


            except:
                pass


if __name__ == '__main__':

    # parse command options
    parser = argparse.ArgumentParser()
    parser.add_argument('--feed',
                        choices=['updates', 'positions', 'alerts'],
                        help='MTA Buses GTFS-Realtime feed to fetch (updates,positions,alerts)')
    args = parser.parse_args()


    # make our url
    endpoints =    { 'updates':'http://gtfsrt.prod.obanyc.com/tripUpdates?key={}',
                     'positions':'http://gtfsrt.prod.obanyc.com/vehiclePositions?key={}',
                     'alerts':'http://gtfsrt.prod.obanyc.com/alerts?key={}'
                     }
    base_url=endpoints[args.feed]
    api_key = os.environ['API_KEY']
    url = base_url.format(api_key)

    # parse and print
    feed = gtfs_realtime_pb2.FeedMessage()

    new_positions={}
    old_positions={}

    # loop forever
    while 1:

        response = requests.get(url)
        feed.ParseFromString(response.content)

        if args.feed == 'updates':
            for entity in feed.entity:
                if entity.HasField('trip_update'):
                    print (entity.trip_update)

        elif args.feed == 'positions':
            new_positions = parse_positions(feed)
            show_delta(new_positions, old_positions)
            old_positions = new_positions

        elif args.feed == 'alerts':
            for entity in feed.entity:
                print(entity)
            pass

        # time.sleep(10)
