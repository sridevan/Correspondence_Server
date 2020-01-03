from data.models import UnitCenters
from sqlalchemy import case
import numpy as np


def get_center(corr_std):
    units_center = []
    # units_num_center = [] # debugging statement
    query_std_len = len(corr_std[0])

    # This section of the code deals with the database query to get the centers data
    for units in corr_std:

        ordering = case(
            {id: index for index, id in enumerate(units)},
            value=UnitCenters.unit_id
        )

        centers_query = UnitCenters.query.filter(UnitCenters.unit_id.in_(units),
                                                 UnitCenters.name == 'base').order_by(ordering)
        for row in centers_query:
            units_center.append(np.array([row.x, row.y, row.z]))
            # units_num_center.append(row.unit_id) # debugging statement

    units_center_list = [units_center[i:i + query_std_len] for i in xrange(0, len(units_center), query_std_len)]

    return units_center_list
