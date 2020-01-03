from data.models import UnitCorrespondence
from sqlalchemy import case, tuple_
from infrastructure.utility import check_insertion, check_modifications, group_corr, sort_sublist, sort_list


def get_correspondence(query_units, members_list):
    # This section of the code deals with getting the complete corresponding unit_ids
    ordering = case(
        {unit: index for index, unit in enumerate(query_units)},
        value=UnitCorrespondence.unit_id_1
    )

    correspondence_complete = UnitCorrespondence.query \
        .filter(UnitCorrespondence.unit_id_1.in_(query_units)) \
        .order_by(ordering) \
        .filter(tuple_(UnitCorrespondence.pdb_id_2, UnitCorrespondence.chain_name_2)
                .in_(members_list))

    corr_units = []
    for row in correspondence_complete:
        corr_units.append(row.unit_id_2)

    corr_filtered = check_insertion(corr_units)
    corr_grouped = group_corr(corr_filtered)
    corr_grouped = [x for x in corr_grouped if len(x) == len(query_units)]
    corr_grouped = sort_sublist(corr_grouped)
    corr_grouped.append(query_units)
    corr_complete = corr_grouped
    corr_std = check_modifications(corr_complete)

    return corr_complete, corr_std


def get_correspondence_core(core_units, members_list):
    # This section of the code deals with getting the complete corresponding unit_ids
    ordering = case(
        {unit: index for index, unit in enumerate(core_units)},
        value=UnitCorrespondence.unit_id_1
    )

    correspondence_complete = UnitCorrespondence.query \
        .filter(UnitCorrespondence.unit_id_1.in_(core_units)) \
        .order_by(ordering) \
        .filter(tuple_(UnitCorrespondence.pdb_id_2, UnitCorrespondence.chain_name_2)
                .in_(members_list))

    corr_units = []
    for row in correspondence_complete:
        corr_units.append(row.unit_id_2)

    core_filtered = check_insertion(corr_units)
    core_grouped = group_corr(core_filtered)
    core_grouped = [x for x in core_grouped if len(x) == len(core_units)]
    core_grouped = sort_sublist(core_grouped)
    core_units = sort_list(core_units)
    core_grouped.append(core_units)
    core_complete = core_grouped

    return core_complete
