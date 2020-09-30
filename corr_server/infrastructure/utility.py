from itertools import groupby, islice
from copy import deepcopy
from collections import defaultdict, OrderedDict
from definitions import annotation_new, ssu_helix_numbering
from discrepancy import matrix_discrepancy, relative_discrepancy
from ordering import optimalLeafOrder
import numpy as np
import math
import csv


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
    prob_list = []
    for sublist in corr_list:
        try:
            b = sorted(sublist, key=lambda x: int(x.split('|')[-1]))
            sorted_list.append(b)
        except:
            prob_list.append(sublist)
            continue

    return sorted_list, prob_list


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


def build_coord_relative(core_list, corr_list):
    # Create list of IFES
    ife_list = []
    for sublist in core_list:
        ife = '|'.join(sublist[0].split('|')[:3])
        ife_list.append(ife)

    combined_units = merge_list(core_list, corr_list)

    # Create list of coordinates as strings
    coord_unordered = []
    for x in combined_units:
        x = ','.join(x)
        coord_unordered.append(x)

    # Create a dictionary of ifes with coordinate data
    ife_coord = dict(zip(ife_list, coord_unordered))

    return ife_list, ife_coord


def build_coord_core(ife_list, core_list):
    # Create list of coordinates as strings
    coord_unordered = []
    for x in core_list:
        x = ','.join(x)
        coord_unordered.append(x)

    # Create a dictionary of ifes with coordinate data
    ife_coord_core = dict(zip(ife_list, coord_unordered))

    return ife_coord_core


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


def pw_similarity(lst1, lst2):
    score = 0

    for a1, b1 in zip(lst1, lst2):
        if a1 == b1:
            score += 0
        elif (a1 == 'n' + b1) or (b1 == 'n' + a1):
            score += 0.5
        elif a1 == '-' or b1 == '-':
            score += 1.0
        elif a1 != b1:
            score += 0.8

    return score


def calculate_pw_score(ife_list, pw_list):
    scores = defaultdict(lambda: defaultdict(int))

    for a in range(0, len(ife_list)):
        for b in range(a + 1, len(ife_list)):
            score = pw_similarity(pw_list[a], pw_list[b])
            scores[ife_list[a][1]][ife_list[b][1]] = score

    return scores


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


def get_ordering_manual(ife_list, coord_data, default_ordering):
    # Get the default ordering for the ife in the list
    chain_order = []
    for chain in ife_list:
        for elem in default_ordering:
            if chain == elem[1]:
                chain_order.append(int(elem[0]))

    # Build a list of tuple pairs with the ife list and default ordering
    ife_unordered = zip(chain_order, ife_list)
    # Reorder the tuple pairs based on ordering
    ife_reordered = sorted(ife_unordered, key=lambda x: x[0])
    # Build a list of reordered ifes
    chain_reordered = [elem[1] for elem in ife_reordered]
    # Build a new and continuous ordering list starting from zero
    new_order = [idx for idx, chain in enumerate(chain_reordered)]
    # Build a list of tuple pairs containing the new ordering list and the reordered ife list
    ifes_ordered = zip(new_order, chain_reordered)

    coord_ordered = []
    # append the coordinates based on new ordering
    for index in ifes_ordered:
        for key, val in coord_data.iteritems():
            if index[1] == key:
                coord_ordered.append(val)

    return ifes_ordered, coord_ordered


def reorder_core(ifes_ordered, core_data):
    coord_core_ordered = []
    # append the coordinates based on new ordering
    for index in ifes_ordered:
        for key, val in core_data.iteritems():
            if index[1] == key:
                coord_core_ordered.append(val)

    return coord_core_ordered


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
    percentile = "{:.3f}".format(np.percentile(a, 95))
    mean = "{:.3f}".format(np.mean(a))
    median = "{:.3f}".format(np.median(a))
    max_disc = "{:.3f}".format(np.amax(a))

    heatmap_data = [
        {"ife1": if1, "ife1_index": if1_index, "ife2": if2, "ife2_index": if2_index, "discrepancy": discrepancy}
        for if1, if1_index, if2, if2_index, discrepancy in zip(ife1, index1, ife2, index2, disc_formatted)
    ]

    dist_data = zip(ife1, ife2, disc_formatted)

    return max_disc, percentile, mean, median, heatmap_data, dist_data


def build_pairwise_heatmap(scores, ifes_ordered):
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

    disc_ordered = [get(scores, first, second) or get(scores, second, first) for first, second in ife_pairs]

    disc_formatted = []
    for disc in disc_ordered:
        disc = '%.2f' % disc
        disc_formatted.append(disc)

    heatmap_data = [
        {"ife1": if1, "ife1_index": if1_index, "ife2": if2, "ife2_index": if2_index, "discrepancy": discrepancy}
        for if1, if1_index, if2, if2_index, discrepancy in zip(ife1, index1, ife2, index2, disc_formatted)
    ]

    return heatmap_data


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


def get_annotation_new(ifes_ordered):
    trna_occupancy = []
    functional_state = []
    factors_bound = []
    antibiotic_bound = []
    calculated_head = []
    calculated_intersubunit = []
    description = []
    structure_method = []
    structure_resolution = []
    principal_investigator = []
    publication_year = []
    codon_pairing = []

    for ife1 in ifes_ordered:
        for ife2 in annotation_new:
            if ife1[1] == ife2[0]:
                calculated_head.append(ife2[1])
                calculated_intersubunit.append(ife2[2])
                description.append(ife2[3])
                structure_method.append(ife2[4])
                structure_resolution.append(ife2[5])
                principal_investigator.append(ife2[6])
                publication_year.append(ife2[7])
                trna_occupancy.append(ife2[8])
                functional_state.append(ife2[9])
                factors_bound.append(ife2[10])
                antibiotic_bound.append(ife2[11])
                codon_pairing.append(ife2[12])

    return calculated_head, calculated_intersubunit, description, structure_method, structure_resolution, \
           principal_investigator, publication_year, trna_occupancy, functional_state, factors_bound, \
           antibiotic_bound, codon_pairing


def reorder_pw(ifes_ordered, pw_info):
    new_order = []
    for elem in ifes_ordered:
        new_order.append(elem[1])

    pw_info_ordered = custom_order(pw_info, new_order)

    return pw_info_ordered


def reorder_chain(ifes_ordered, chain_unordered):
    new_order = []
    for elem in ifes_ordered:
        new_order.append(elem[1])

    chain_info_ordered = custom_order(chain_unordered, new_order)

    return chain_info_ordered


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


def build_uid(query_list, query_ife):
    range_list = []
    for sublist in query_list:
        sublist = map(lambda orig_string: query_ife + '|%|' + orig_string, sublist)
        range_list.append(sublist)
    return range_list


def helix_assignment(residue_num):
    for key1, val1 in ssu_helix_numbering.items():
        if len(val1) == 2:
            if val1[0] <= int(residue_num) <= val1[1]:
                helix_pos = key1
        else:
            if val1[0] <= int(residue_num) <= val1[1] or val1[2] <= int(residue_num) <= val1[3]:
                helix_pos = key1
    return helix_pos


def get_ssu_helix_numbering(pw_list):
    for sublist in pw_list:
        ife1 = '|'.join(sublist[0].split('|')[:3])
        ife2 = '|'.join(sublist[1].split('|')[:3])
        res1num = sublist[0].split('|')[-1]
        res2num = sublist[1].split('|')[-1]
        res1_helix_num = helix_assignment(res1num)
        if ife2 == ife1:
            res2_helix_num = helix_assignment(res2num)
        else:
            chain_res2 = ife2.split('|')[2]
            res2_helix_num = 'Chain ' + chain_res2
        sublist.insert(2, res1_helix_num)
        sublist.insert(3, res2_helix_num)

    return pw_list


def get_ssu_helix_numbering_contacts(pw_list):
    chain_info = {}
    for sublist in pw_list:
        ife1 = '|'.join(sublist[0].split('|')[:3])
        ife2 = '|'.join(sublist[1].split('|')[:3])
        res1num = sublist[0].split('|')[-1]
        res2num = sublist[1].split('|')[-1]
        res1_helix_num = helix_assignment(res1num)
        chain_id = []
        if ife2 == ife1:
            res2_helix_num = helix_assignment(res2num)
        else:
            chain_res2 = ife2.split('|')[2]
            res2_helix_num = 'Chain ' + chain_res2
            chain_id.append(ife2)
        sublist.append(res1_helix_num)
        sublist.append(res2_helix_num)
        chain_info[ife1] = chain_id

    return pw_list, chain_info


def get_chain_id(contacts_dict):
    chain_collection = []
    key_collection = []

    for k, v in contacts_dict.items():
        pdbid = k.split('|')[0]
        if type(v) is not list:
            key_collection.append(k)
            chain_collection.append([])
        if type(v) is list:
            chain_info = []
            for sublist in v:
                if sublist[3].startswith("Chain"):
                    chain = sublist[3].split(" ")[1]
                    chain_info.append((pdbid, chain))
            chain_info = list(set(chain_info))
            chain_collection.append(chain_info)
            key_collection.append(k)

    chain_dict = OrderedDict(zip(key_collection, chain_collection))

    return chain_dict


def merge_chain_info(rna_dict, protein_dict):
    chain_info = OrderedDict()
    for key in (rna_dict.viewkeys() | protein_dict.keys()):
        if key in rna_dict: chain_info.setdefault(key, []).extend(rna_dict[key])
        if key in protein_dict: chain_info.setdefault(key, []).extend(protein_dict[key])

    return chain_info


def build_dist(dist_data, query_units):
    with open('/Applications/mamp/htdocs/Results/relative/SSU/5J7L/Disc_IL_bound/' + str(query_units[0]) + '_disc.csv',
              "w") as f:
        writer = csv.writer(f)
        writer.writerow(["ID1", "ID2", "Disc"])
        for row in dist_data:
            writer.writerow(row)


def get_center_len(center_data):
    center = []
    for k, v in enumerate(center_data):
        if len(v) != 11:
            center.append(k)

    return center


def process_pw(annotation):
    pw = []
    for k, v in annotation.items():
        for k1, v2 in v.items():
            pw.append(v2)
        size = len(v)

    processed_pw = [pw[i:i + size] for i in range(0, len(pw), size)]

    return processed_pw
