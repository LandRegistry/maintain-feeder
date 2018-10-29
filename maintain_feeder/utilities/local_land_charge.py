from maintain_feeder import config
from maintain_feeder.extensions import session
from maintain_feeder.exceptions import ApplicationError
from maintain_feeder.models import LocalLandCharge, LocalLandChargeHistory, GeometryFeature
from llc_schema_dto import llc_schema
from shapely.geometry import asShape
from geoalchemy2 import shape
from sqlalchemy import func


def process_land_charge(logger, body):
    """Process a local land charge message"""

    land_charge_full_json = llc_schema.convert(
        body["item"], config.SCHEMA_VERSION)
    land_charge_id = body['key']
    land_charge_type = land_charge_full_json['charge-type']
    entry_number = body['entry-number']
    entry_timestamp = body['entry-timestamp']

    new_charge = False
    land_charge_item_changes = None
    cancelled = False
    further_information_reference = None
    prev_version = False

    if session.query(LocalLandChargeHistory).filter(LocalLandChargeHistory.entry_number > entry_number,
                                                    LocalLandChargeHistory.id == land_charge_id).first():
        logger.info("Entry {} is for a previous version of LLC {}".format(entry_number, land_charge_id))
        prev_version = True

    # New Charges
    if body['action-type'] == "NEW":
        logger.info("Entry {} for LLC {} is for a new charge".format(entry_number, land_charge_id))
        new_charge = True

    # Updated Charges
    if 'item-changes' in body:
        land_charge_item_changes = body['item-changes']

    # Cancelled Charges
    if 'end-date' in land_charge_full_json and land_charge_full_json['end-date']:
        logger.info("Entry {} for LLC {} is for a cancellation".format(entry_number, land_charge_id))
        cancelled = True

    if 'further-information-reference' in land_charge_full_json:
        further_information_reference = land_charge_full_json['further-information-reference']

    if not cancelled and not new_charge:
        logger.info("Entry {} for LLC {} is for a vary".format(entry_number, land_charge_id))

    logger.info("Attempting to add new history row for charge {}, entry_number {}"
                .format(land_charge_id, entry_number))
    new_land_charge_history = LocalLandChargeHistory(land_charge_id, land_charge_full_json, cancelled,
                                                     entry_number, entry_timestamp,
                                                     land_charge_item_changes)

    session.add(new_land_charge_history)

    if not prev_version:
        logger.info("Attempting to add new row for charge {}, entry_number {}"
                    .format(land_charge_id, entry_number))
        new_land_charge = LocalLandCharge(land_charge_id, land_charge_type, land_charge_full_json,
                                          cancelled, further_information_reference)
        # work on the merged object to get hold of the geometry
        new_land_charge = session.merge(new_land_charge)

        # create GeometryFeature(s)
        logger.info("Extracting geometry for charge {}, entry_number {}"
                    .format(land_charge_id, entry_number))
        new_land_charge.geometry = []
        # flush to get geometry removed
        session.flush()
        if land_charge_full_json['geometry']['type'] == 'FeatureCollection':
            for feature in land_charge_full_json['geometry']['features']:
                geo_shape = asShape(feature['geometry'])
                current_geo_id = feature['properties']['id']
                new_geo = GeometryFeature(func.ST_Force2D(
                    shape.from_shape(geo_shape, srid=27700)), current_geo_id)
                new_land_charge.geometry.append(new_geo)
        else:
            # Should contain at least one Geometry in FeatureCollection
            logger.error("No FeatureCollection for charge {}, entry_number {}"
                         .format(land_charge_id, entry_number))
            raise ApplicationError("No FeatureCollection found in entry")

    session.commit()

    if prev_version:
        logger.info("Previous version of charge stored. ID: {}, entry number {}"
                    .format(land_charge_id, entry_number))
    elif new_charge:
        logger.info("New LLC stored. ID: {}, entry number: {}"
                    .format(land_charge_id, entry_number))
    else:
        logger.info("Modified LLC stored. ID: {}, entry number: {}"
                    .format(land_charge_id, entry_number))
