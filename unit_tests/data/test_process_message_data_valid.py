process_message_null = {
    'entry-timestamp': None,
    'action-type': 'NEW',
    'item-signature': None,
    'entry-number': 19,
    'key': None,
    'item-hash': None
}

process_message_valid = {
    "item-hash": "test",
    "item-signature": "test",
    "key": "12345678",
    "action-type": "NEW",
    "entry-number": 19,
    "entry-timestamp": "2017-04-27 11:09:28.996676",
    "item": {
        "geometry": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "crs": {
                        "type": "name",
                        "properties": {
                            "name": "EPSG:27700"
                        }
                    },
                    "type": "Polygon",
                    "coordinates": [[[294915.40831620456, 93347.98452708151],
                                     [294908.2551678813, 93313.65262390542],
                                     [294917.2574326514, 93310.89385218851],
                                     [294924.7282665854, 93345.54135279212],
                                     [294915.40831620456, 93347.98452708151]]]
                },
                "properties": {
                    "id": "26"
                }
            }]
        },
        "instrument": "Deed",
        "start-date": "2017-01-01",
        "charge-type": "Planning",
        "local-land-charge": "12345704",
        "registration-date": "2017-01-01",
        "statutory-provision": "Planning Act",
        "charge-creation-date": "2014-07-20",
        "originating-authority": "ExeterCityCouncil",
        "further-information-location": "local-land-charges@exeter.gov.uk",
        "charge-geographic-description": "Exeter-220001",
        "further-information-reference": "PLA/220026"
    }
}

process_message_valid_vary = {
    "item-hash": "test",
    "item-signature": "test",
    "key": "12345678",
    "action-type": "UPDATED",
    "entry-number": 19,
    "item-changes": {
        "something": "changed"
    },
    "entry-timestamp": "2017-04-27 11:09:28.996676",
    "item": {
        "geometry": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "crs": {
                        "type": "name",
                        "properties": {
                            "name": "EPSG:27700"
                        }
                    },
                    "type": "Polygon",
                    "coordinates": [[[294915.40831620456, 93347.98452708151],
                                     [294908.2551678813, 93313.65262390542],
                                     [294917.2574326514, 93310.89385218851],
                                     [294924.7282665854, 93345.54135279212],
                                     [294915.40831620456, 93347.98452708151]]]
                },
                "properties": {
                    "id": "26"
                }
            }]
        },
        "instrument": "Deed",
        "start-date": "2017-01-01",
        "end-date": "2018-01-01",
        "charge-type": "Planning",
        "local-land-charge": "12345704",
        "registration-date": "2017-01-01",
        "statutory-provision": "Planning Act",
        "charge-creation-date": "2014-07-20",
        "originating-authority": "ExeterCityCouncil",
        "further-information-location": "local-land-charges@exeter.gov.uk",
        "charge-geographic-description": "Exeter-220001",
        "further-information-reference": "PLA/220026"
    }
}
