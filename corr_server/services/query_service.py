from collections import OrderedDict
from data.models import UnitInfo, LoopInfo
from infrastructure.utility import get_sorted_units, sort_list


def get_complete_units(query_list):
    query_ife = '5J7L|1|DA|%|'
    incomplete_list = [query_ife + elem for elem in query_list]

    complete_units = []
    for unit in incomplete_list:
        query = UnitInfo.query.filter(UnitInfo.unit_id.like(unit))
        for row in query:
            complete_units.append(row.unit_id)

    complete_units = sort_list(complete_units)

    return complete_units


def get_complete_units_double(lst1, lst2):
    core_ife = '5J7L|1|DA|%|'
    query_ife = '5J7L|1|AA|%|'
    incomplete_core = [core_ife + elem for elem in lst1]
    incomplete_query = [query_ife + elem for elem in lst2]

    complete_core = []
    for unit in incomplete_core:
        query = UnitInfo.query.filter(UnitInfo.unit_id.like(unit))
        for row in query:
            complete_core.append(row.unit_id)

    complete_query = []
    for unit in incomplete_query:
        query = UnitInfo.query.filter(UnitInfo.unit_id.like(unit))
        for row in query:
            complete_query.append(row.unit_id)

    complete_query = sort_list(complete_query)

    return complete_core, complete_query


def get_complete_units_relative(query_list):
    query_ife = '5J7L|1|AA|%|'
    incomplete_list = [query_ife + elem for elem in query_list]

    complete_units = []
    for unit in incomplete_list:
        query = UnitInfo.query.filter(UnitInfo.unit_id.like(unit))
        for row in query:
            complete_units.append(row.unit_id)

    return complete_units


def get_chain_idx(query):
    range_selection = []
    for elem in query:
        range_selection.append(elem)

    chain_idx = []
    for sublist in query:
        units_query = UnitInfo.query.filter(UnitInfo.unit_id.in_(sublist))

        for rows in units_query:
            chain_idx.append(rows.chain_index)

    return chain_idx


def get_query_units(query_type, query_list):
    query_units = []

    if query_type == 'single_range':

        query_ife = '|'.join(query_list[0][0].split('|')[:3])
        query_pdb = query_list[0][0].split('|')[0]
        query_chain = query_list[0][0].split('|')[2]
        chain_idx = get_chain_idx(query_list)
        chain_idx.sort()

        units_query = UnitInfo.query.filter_by(pdb_id=query_pdb, chain=query_chain). \
            filter(UnitInfo.chain_index.between(chain_idx[0], chain_idx[1])) \
            .order_by(UnitInfo.chain_index).all()

        for row in units_query:
            query_units.append(row.unit_id)

    elif query_type == 'multiple_ranges':

        query_ife = '|'.join(query_list[0][0].split('|')[:3])
        query_pdb = query_list[0][0].split('|')[0]
        query_chain = query_list[0][0].split('|')[2]
        chain_idx = get_chain_idx(query_list)
        chain_idx.sort()
        # partition_size = len(query_list)
        # Partition the list into a list of lists containing the start and end units of each range
        chain_idx = [chain_idx[i:i + 2] for i in range(0, len(chain_idx), 2)]

        for i in chain_idx:
            units_query = UnitInfo.query.filter_by(pdb_id=query_pdb, chain=query_chain). \
                filter(UnitInfo.chain_index.between(i[0], i[1])) \
                .order_by(UnitInfo.chain_index).all()
            for row in units_query:
                query_units.append(row.unit_id)

        query_units = list(OrderedDict.fromkeys(query_units))

    elif query_type == 'units_str':
        incomplete_units = []
        for unit in query_list:
            incomplete_units.append(unit[0])
            query_units = get_complete_units(incomplete_units)
            query_ife = '|'.join(query_units[0].split('|')[:3])


    # todo work to do
    elif query_type == 'loop_id':

        loop_id = query_list[0][0]
        units_query = LoopInfo.query.filter_by(loop_id=loop_id)

        for row in units_query:
            unsorted_units = row.unit_ids
            loop_position = row.loop_name

        query_units = get_sorted_units(unsorted_units)
        query_ife = '|'.join(query_units[0].split('|')[:3])
        query_pdb = query_units[0].split('|')[0]

    return query_ife, query_units


def get_query_units_relative(query_type, query_list):
    incomplete_units = []
    for unit in query_list:
        incomplete_units.append(unit[0])
        query_units = get_complete_units_relative(incomplete_units)
        query_ife = '|'.join(query_units[0].split('|')[:3])

    return query_units, query_ife


def get_query_units_double(query_type, query_list):
    core_incomplete = []
    query_incomplete = []
    for i in range(0, 18):
        core_incomplete.append(query_list[i][0])
    for i in range(18, len(query_list)):
        query_incomplete.append(query_list[i][0])

    core_nts, query_units = get_complete_units_double(core_incomplete, query_incomplete)
    return core_nts, query_units
