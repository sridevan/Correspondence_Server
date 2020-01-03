from itertools import groupby, islice
from copy import deepcopy
from collections import defaultdict, OrderedDict
from definitions import ribosome_subunits, rotation_data, rotation_head, annotation, annotation_LSU
from discrepancy import matrix_discrepancy, relative_discrepancy
from ordering import optimalLeafOrder
import numpy as np
import math


def custom_order(dct, spec):
    res = OrderedDict()
    for key in spec:
        if key in dct:
            res[key] = dct.pop(key)
    res.update(dct.items())

    return res


def getkey(item):
    return item[0]


def get(d, first, second):
    return d.get(second, {}).get(first, 0.0)


def get_sorted_units(units):
    unsorted_units = units.split(',')
    sorted_units = sorted(unsorted_units, key=lambda x: int(x.split('|')[4]))
    return sorted_units


def reject_ife(members_list, reject_list):
    # remove ifes that are joined (+)
    rejected_members = []
    for i, v in enumerate(members_list):
        if any(c in '+' for c in v):
            rejected_members.append(members_list[i])
            del members_list[i]

    for elem in reject_list:
        for i, v in enumerate(members_list):
            if elem == v:
                rejected_members.append(members_list[i])
                del members_list[i]

    return rejected_members, members_list


def check_insertion(corr_units):
    for unit in corr_units:
        ife_num = unit.split('|')[-1]
        try:
            num = int(ife_num)
        except ValueError:
            corr_units.remove(unit)

    return corr_units


def group_corr(corr_list):
    """
    The list has to be sorted before it could be grouped
    But the sorting is based on the string, not residue number
    Hence, it has to be sorted again according to the residue number
    """
    corr_list.sort()
    keyf = lambda x: '|'.join(x.split('|')[:3])
    corr_grouped = [list(items) for gr, items in groupby(corr_list, key=keyf)]

    return corr_grouped


def sort_list(single_list):
    sorted_list = sorted(single_list, key=lambda x: int(x.split('|')[-1]))

    return sorted_list


def sort_sublist(corr_list):
    sorted_list = []
    for sublist in corr_list:
        b = sorted(sublist, key=lambda x: int(x.split('|')[-1]))
        sorted_list.append(b)

    return sorted_list


def check_modifications(corr_complete):
    accepted_seq = ['A', 'C', 'G', 'U']
    mod_idx = []
    corr_std = deepcopy(corr_complete)

    for sublist in corr_complete:
        for unit in sublist:
            seq = unit.split('|')[3]
            if seq not in accepted_seq:
                mod_idx.append(sublist.index(unit))

    mod_unique = set(mod_idx)
    mod_idx = list(mod_unique)

    for elem1 in corr_std:
        for ele in sorted(mod_idx, reverse=True):
            del elem1[ele]

    return corr_std


def build_coord(corr_list):
    # Create list of IFES
    ife_list = []
    for sublist in corr_list:
        ife = '|'.join(sublist[0].split('|')[:3])
        ife_list.append(ife)

    # Create list of coordinates as strings
    coord_unordered = []
    for x in corr_list:
        x = ','.join(x)
        coord_unordered.append(x)

    # Create a dictionary of ifes with coordinate data
    ife_coord = dict(zip(ife_list, coord_unordered))

    return ife_list, ife_coord


def build_coord_double(corr_list, size):
    # Create list of IFES
    lsu_list = []
    ssu_list = []
    for sublist in corr_list:
        lsu_ife = '|'.join(sublist[0].split('|')[:3])
        ssu_ife = '|'.join(sublist[-1].split('|')[:3])
        lsu_list.append(lsu_ife)
        ssu_list.append(ssu_ife)

    # Create list of coordinates as strings
    coord_unordered = []
    for x in corr_list:
        x = ','.join(x[12:len(x)])
        coord_unordered.append(x)

    # Create a dictionary of ifes with coordinate data
    ife_coord = dict(zip(lsu_list, coord_unordered))

    return lsu_list, ssu_list, ife_coord


def calculate_geometric_disc(ife_list, rotation_data, center_data):
    distances = defaultdict(lambda: defaultdict(int))

    for a in range(0, len(ife_list)):
        for b in range(a + 1, len(ife_list)):
            disc = matrix_discrepancy(center_data[a], rotation_data[a], center_data[b],
                                      rotation_data[b])
            distances[ife_list[a]][ife_list[b]] = disc

        # Empty list to append pairs of IFE with NaN discrepancy
        ife_nan = []

        for k, v in distances.items():
            for i1, i2 in v.items():
                if math.isnan(i2):
                    ife_nan.append((k, i1))
                    v[i1] = -0.1

    return distances


def calculate_relative_disc(ife_list, center_data, core_len, query_len):
    distances = defaultdict(lambda: defaultdict(int))

    for a in range(0, len(ife_list)):
        for b in range(a + 1, len(ife_list)):
            disc = relative_discrepancy(center_data[a], center_data[b], core_len, query_len)
            distances[ife_list[a]][ife_list[b]] = disc

    return distances


def get_ordering(ife_list, distances, coord_data):
    dist = np.zeros((len(ife_list), len(ife_list)))
    for index1, member1 in enumerate(ife_list):
        curr = distances.get(member1, {})
        for index2, member2 in enumerate(ife_list):
            dist[index1, index2] = curr.get(member2, 0)

    dist = (dist + np.swapaxes(dist, 0, 1))

    # ordering, _, _ = orderWithPathLengthFromDistanceMatrix(dist, 10, scanForNan=True)
    disc_order = optimalLeafOrder(dist)

    new_ordering = []
    idx_ordering = []

    for idx, order in enumerate(disc_order):
        new_ordering.append(ife_list[order])
        idx_ordering.append(idx)

    ifes_ordered = zip(idx_ordering, new_ordering)

    coord_ordered = []
    # append the coordinates based on new ordering
    for index in ifes_ordered:
        for key, val in coord_data.iteritems():
            if index[1] == key:
                coord_ordered.append(val)

    return ifes_ordered, coord_ordered


def build_heatmap_data(distances, ifes_ordered):
    index1 = []
    index2 = []
    ife1 = []
    ife2 = []

    for member1 in ifes_ordered:
        for member2 in ifes_ordered:
            index1.append(member1[0])
            ife1.append(member1[1])
            index2.append(member2[0])
            ife2.append(member2[1])

    ife_pairs = zip(ife1, ife2)

    disc_ordered = [get(distances, first, second) or get(distances, second, first) for first, second in ife_pairs]

    disc_formatted = []
    for disc in disc_ordered:
        disc = '%.4f' % disc
        disc_formatted.append(disc)

    a = np.array(disc_formatted)
    a = a.astype(np.float)
    percentile = np.percentile(a, 95)
    max_disc = np.amax(a)

    heatmap_data = [
        {"ife1": if1, "ife1_index": if1_index, "ife2": if2, "ife2_index": if2_index, "discrepancy": discrepancy}
        for if1, if1_index, if2, if2_index, discrepancy in zip(ife1, index1, ife2, index2, disc_formatted)
    ]

    return max_disc, percentile, heatmap_data


def get_annotation(ifes_ordered):
    trna_occupancy = []
    functional_state = []
    factors_bound = []
    antibiotic_bound = []

    for order in ifes_ordered:
        for state in annotation:
            if order[1] == state[0]:
                trna_occupancy.append(state[1])
                functional_state.append(state[2])
                factors_bound.append(state[3])
                antibiotic_bound.append(state[4])

    reported_intersubunit = []
    calculated_intersubunit = []
    for order in ifes_ordered:
        for ife in rotation_data:
            if order[1] == ife[0]:
                reported_intersubunit.append(ife[2])
                calculated_intersubunit.append(ife[3])

    reported_head = []
    calculated_head = []
    for order in ifes_ordered:
        for ife in rotation_head:
            if order[1] == ife[0]:
                reported_head.append(ife[2])
                calculated_head.append(ife[3])

    return trna_occupancy, functional_state, factors_bound, antibiotic_bound, reported_intersubunit, \
           calculated_intersubunit, reported_head, calculated_head


def get_annotation_double(ifes_ordered):
    trna_occupancy = []
    functional_state = []
    factors_bound = []
    antibiotic_bound = []

    for order in ifes_ordered:
        for state in annotation_LSU:
            if order[1] == state[0]:
                trna_occupancy.append(state[1])
                functional_state.append(state[2])
                factors_bound.append(state[3])
                antibiotic_bound.append(state[4])

    reported_intersubunit = []
    calculated_intersubunit = []
    for order in ifes_ordered:
        for ife in rotation_data:
            if order[1] == ife[1]:
                reported_intersubunit.append(ife[2])
                calculated_intersubunit.append(ife[3])

    reported_head = []
    calculated_head = []
    for order in ifes_ordered:
        for ife in rotation_head:
            if order[1] == ife[1]:
                reported_head.append(ife[2])
                calculated_head.append(ife[3])

    return trna_occupancy, functional_state, factors_bound, antibiotic_bound, reported_intersubunit, \
           calculated_intersubunit, reported_head, calculated_head


def reorder_pw(ifes_ordered, pw_info):
    new_order = []
    for elem in ifes_ordered:
        new_order.append(elem[1])

    pw_info_ordered = custom_order(pw_info, new_order)

    return pw_info_ordered


def reorder_pw_double(ifes_ordered, pw_info):
    lsu_order = []
    for elem in ifes_ordered:
        lsu_order.append(elem[1])

    ssu_order = []
    for e1 in lsu_order:
        for e2 in ribosome_subunits:
            if e1 == e2[1]:
                ssu_order.append(e2[0])

    pw_info_ordered = custom_order(pw_info, ssu_order)

    return pw_info_ordered


# need to change the len of the core nts manually
def partition_list(query_units):
    query_len = len(query_units) - 10
    seclist = [10, query_len]
    it = iter(query_units)

    sliced = [list(islice(it, 0, i)) for i in seclist]

    core_units = sliced[0]
    query_units = sliced[1]

    return core_units, query_units


def merge_double(ref, dict1, dict2):
    ssu_key = []
    for k1, v1 in dict1.iteritems():
        for subunit_pairs in ref:
            if k1 == subunit_pairs[1]:
                k2 = subunit_pairs[0]
                ssu_key.append(k2)

    ssu_reordered = OrderedDict()
    for k1 in ssu_key:
        ssu_reordered[k1] = dict2.get(k1)

    merged_lists = [a + b for (a, b) in zip(dict1.values(), ssu_reordered.values())]

    return merged_lists


def merge_list(lst1, lst2):
    merged_lists = [a + b for (a, b) in zip(lst1, lst2)]
    return merged_lists


def create_dict(lst1):
    dict_corr = OrderedDict()
    ife_list = []
    for sublist in lst1:
        ife = '|'.join(sublist[0].split('|')[:3])
        dict_corr[ife] = sublist

    return dict_corr
