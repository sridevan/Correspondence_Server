from collections import OrderedDict
from data.models import UnitPairInteractions
from itertools import combinations
from sqlalchemy import tuple_
from infrastructure import utility as ui


def get_pairwise_annotation(corr_complete, query_units, ife_list):
    bps_comb = []
    for a in range(0, len(corr_complete)):
        bps_comb.append([(map(str, comb)) for comb in combinations(corr_complete[a], 2)])

    unit1 = []
    unit2 = []
    bpair = []
    bstack = []
    bphosphate = []
    bribose = []
    for a in range(0, len(corr_complete)):
        bps_list = UnitPairInteractions.query.filter(
            tuple_(UnitPairInteractions.unit_id_1, UnitPairInteractions.unit_id_2) \
                .in_(bps_comb[a]))

        for row in bps_list:
            unit1.append(row.unit_id_1)
            unit2.append(row.unit_id_2)
            bpair.append(row.f_lwbp)
            bstack.append(row.f_stacks)
            bphosphate.append(row.f_bphs)
            bribose.append(row.f_brbs)

        pairwise_info = zip(unit1, unit2, bpair, bstack, bphosphate, bribose)

    filtered_pw_info = []
    for elem in pairwise_info:
        a = list(filter(lambda a: a != None, elem))
        filtered_pw_info.append(a)

    units_order = {}
    for idx, unit in enumerate(query_units):
        unit = unit.split('|')[-1]
        units_order[unit] = idx + 1

    n1 = []
    n2 = []

    for n in filtered_pw_info:
        n_1 = n[0].split('|')[-1]
        n_2 = n[1].split('|')[-1]
        try:
            n1.append(int(n_1))
            n2.append(int(n_2))
        except:
            pass

    possible_pw = zip(n1, n2)
    unique_pw = list(set(possible_pw))
    pw_sorted = sorted(unique_pw, key=ui.getkey)

    pw_info = {k: OrderedDict({t: '-' for t in pw_sorted}) for k in ife_list}

    for sub_lst in filtered_pw_info:
        k0, k1 = '|'.join(sub_lst[0].split('|')[:3]), '|'.join(sub_lst[1].split('|')[:3])
        if k0 == k1 and k0 in pw_info:
            try:
                sub_key = (int(sub_lst[0][sub_lst[0].rfind('|') + 1:]), int(sub_lst[1][sub_lst[1].rfind('|') + 1:]))
                pw_info[k0][sub_key] = sub_lst[2] if len(sub_lst) == 3 else ';'.join(sub_lst[2:])
            except:
                pass

    return pw_info, pw_sorted
