import itertools
import csv
from collections import OrderedDict
from data.models import UnitPairInteractions
from itertools import combinations, groupby
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


def get_pairwise_tertiary(corr_complete, ife_list):
    unit1 = []
    unit2 = []
    bpair = []
    bstack = []
    bphosphate = []
    bribose = []
    for sublist in corr_complete:
        pairwise_lr = UnitPairInteractions.query \
            .filter(UnitPairInteractions.unit_id_1.in_(sublist)) \
            .filter(UnitPairInteractions.f_crossing >= 4)

        for row in pairwise_lr:
            unit1.append(row.unit_id_1)
            unit2.append(row.unit_id_2)
            bpair.append(row.f_lwbp)
            bstack.append(row.f_stacks)
            bphosphate.append(row.f_bphs)
            bribose.append(row.f_brbs)

    pairwise_lr_info = zip(unit1, unit2, bpair, bstack, bphosphate, bribose)

    pairwise_lr_filtered = []
    for sublist in pairwise_lr_info:
        new_sublist = list(filter(None, sublist))
        pairwise_lr_filtered.append(new_sublist)

    for sublist in pairwise_lr_filtered:
        if len(sublist) == 2:
            sublist.append('perp')

    pairwise_lr_filtered = ui.get_ssu_helix_numbering(pairwise_lr_filtered)

    pw_list = [list(g) for i, g in itertools.groupby(pairwise_lr_filtered, lambda x: '|'.join(x[0].split('|')[:3]))]

    pw_dict = OrderedDict()
    for ife in ife_list:
        pw_dict[ife] = 'No interactions'

    for sublist in pw_list:
        ife = '|'.join(sublist[0][0].split('|')[:3])
        for k, v in pw_dict.items():
            if k == ife:
                pw_dict[k] = sublist

    rna_chain = ui.get_chain_id(pw_dict)

    return pw_dict, rna_chain


def get_pairwise_rnap(corr_lst, ife_list):
    pr_dict = OrderedDict()
    for ife in ife_list:
        pr_dict[ife] = 'No interactions'

    rna_unit = []
    protein_unit = []
    for sublist in corr_lst:
        pdbid = sublist[0].split('|')[0]
        try:
            with open('/Applications/mamp/htdocs/contact_list_rename/contact_list_' + pdbid + '.csv', 'U') as f:
                csv_reader = csv.reader(f, delimiter=',')
                for lines in csv_reader:
                    for unit in sublist:
                        if unit == str(lines[0]):
                            rna_unit.append(str(lines[0]))
                            protein_unit.append(str(lines[3]))
        except Exception:
            print 'Cannot open a file'

    interaction_contacts = zip(rna_unit, protein_unit)
    interaction_contacts = set(interaction_contacts)
    interaction_contacts = [list(x) for x in interaction_contacts]

    interaction_contacts, chain_info = ui.get_ssu_helix_numbering_contacts(interaction_contacts)

    key_func = lambda x: '|'.join(x[0].split('|')[:3])
    sorted_res = sorted(interaction_contacts, key=lambda x: x[0])
    contacts_list = [list(g) for i, g in itertools.groupby(sorted_res, key_func)]

    for sublist in contacts_list:
        ife = '|'.join(sublist[0][0].split('|')[:3])
        for k, v in pr_dict.items():
            if k == ife:
                pr_dict[k] = sublist

    protein_chain = ui.get_chain_id(pr_dict)

    return pr_dict, protein_chain
