from data.models import UnitRotations
from sqlalchemy import case
import numpy as np


def get_rotation(corr_std):
    # Create list to store the rotation np array
    units_rotation = []
    # units_num_rotation = [] # debugging statement
    query_std_len = len(corr_std[0])

    # This section of the code deals with the database query to get the rotation data
    for units in corr_std:

        ordering = case(
            {id: index for index, id in enumerate(units)},
            value=UnitRotations.unit_id
        )

        rotation_query = UnitRotations.query.filter(UnitRotations.unit_id.in_(units)).order_by(ordering)

        for row in rotation_query:
            units_rotation.append(np.array([[row.cell_0_0, row.cell_0_1, row.cell_0_2],
                                            [row.cell_1_0, row.cell_1_1, row.cell_1_2],
                                            [row.cell_2_0, row.cell_2_1, row.cell_2_2]]))
            # units_num_rotation.append(row.unit_id) # debugging statement

    units_rotation_list = [units_rotation[i:i + query_std_len] for i in xrange(0, len(units_rotation), query_std_len)]

    return units_rotation_list
