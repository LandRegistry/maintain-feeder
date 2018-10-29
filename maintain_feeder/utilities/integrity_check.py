from maintain_feeder.extensions import session
from maintain_feeder.models import LocalLandChargeHistory
from sqlalchemy import select, func, and_


def check_integrity(max_entry):
    series = select([func.generate_series(1, max_entry).label('seq_no')]).alias('series')
    res = session.query(
        series.c.seq_no).join(
        LocalLandChargeHistory,
        and_(
            series.c.seq_no == LocalLandChargeHistory.entry_number),
            isouter=True).filter(
                LocalLandChargeHistory.entry_number == None).all()
    return [row[0] for row in res]
