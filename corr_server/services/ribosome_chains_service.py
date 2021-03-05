from collections import OrderedDict
from data.models import ChainInfo, UnitCorrespondence, UnitPairInteractions


def update_chain_list(chain_list, chain_to_remove):
    try:
        chain_list.remove(chain_to_remove)
    except:
        pass

    return chain_list


def get_rna_chain(ife):
    pdb, model, chain = ife.split('|')

    molecule_type = 'Polyribonucleotide (RNA)'

    chain_ids = []
    # Get all RNA chains from the ribosome except the 16S rRNA chain
    query = ChainInfo.query.filter(ChainInfo.pdb_id == pdb) \
        .filter(ChainInfo.entity_macromolecule_type == molecule_type) \
        .filter(ChainInfo.chain_name != chain)

    for row in query:
        chain_ids.append(row.chain_name)

    # Assume model number is 1 here
    rna_chains = ['{}|1|{}'.format(pdb, elem) for elem in chain_ids]
    query_info = (pdb, chain)

    return query_info, rna_chains


def get_nts_corr(nts_list, query_chain):
    pdb, chain = query_chain[0], query_chain[1]

    nts_corr = []
    for nt in nts_list:
        query = UnitCorrespondence.query.filter(UnitCorrespondence.unit_id_1 == nt) \
            .filter(UnitCorrespondence.pdb_id_2 == pdb) \
            .filter(UnitCorrespondence.chain_name_2 == chain)

        for row in query:
            nts_corr.append(row.unit_id_2)

    return nts_corr


def infer_23S_chain(corr_nts, rna_chains):
    lsu_23S_chain = ''
    for chain in rna_chains:
        nt2 = '{}|%'.format(chain)
        for nt in corr_nts:
            query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                .filter(UnitPairInteractions.unit_id_2.like(nt2))

            if query.count() == 1:
                lsu_23S_chain = chain

    rna_chains = update_chain_list(rna_chains, lsu_23S_chain)

    return lsu_23S_chain, rna_chains


def infer_mrna_chain(corr_nts, rna_chains):
    mrna_chain = ''
    test_query = []
    for chain in rna_chains:
        nt2 = '{}|%'.format(chain)
        for nt in corr_nts:
            test_query.append((nt, nt2))
            query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                .filter(UnitPairInteractions.unit_id_2.like(nt2))

            if query.count() == 1:
                mrna_chain = chain

    rna_chains = update_chain_list(rna_chains, mrna_chain)

    return mrna_chain, rna_chains


def infer_ptrna_chain(corr_nts, rna_chains):
    ptrna_chain = ''
    test_query = []
    for chain in rna_chains:
        nt2 = '{}|%'.format(chain)
        for nt in corr_nts:
            test_query.append((nt, nt2))
            query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                .filter(UnitPairInteractions.unit_id_2.like(nt2))

            if query.count() == 1:
                ptrna_chain = chain

    rna_chains = update_chain_list(rna_chains, ptrna_chain)

    return ptrna_chain, rna_chains


def infer_atrna_chain(corr_nts, rna_chains, mrna_chain):
    nr_chain = set()
    for chain in rna_chains:
        nt2 = '{}|%'.format(chain)
        for nt in corr_nts:
            # test_query.append((nt, nt2))
            query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                .filter(UnitPairInteractions.unit_id_2.like(nt2))

            for row in query:
                chain2 = '|'.join(row.unit_id_2.split('|')[:3])
                nr_chain.add(chain2)

    # A-site nts can also interact with mRNA. So we want to remove mRNA chain before assigning a-tRNA if present
    if len(nr_chain) == 1:
        atrna_chain = list(nr_chain)[0]
    elif len(nr_chain) > 1:
        nr_chain.remove(mrna_chain)
        atrna_chain = list(nr_chain)[0]
    else:
        atrna_chain = None

    rna_chains = update_chain_list(rna_chains, atrna_chain)

    return atrna_chain, rna_chains


def infer_etrna_chain(corr_nts, rna_chains, ptrna_chain):
    nr_chain = []
    possible_etrna_chain = ''
    for chain in rna_chains:
        nt2 = '{}|%'.format(chain)
        for nt in corr_nts:
            # test_query.append((nt, nt2))
            query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                .filter(UnitPairInteractions.unit_id_2.like(nt2))

            if query.count() == 1:
                possible_etrna_chain = chain

    if possible_etrna_chain == ptrna_chain:
        etrna_chain = None
    else:
        etrna_chain = possible_etrna_chain

    rna_chains = update_chain_list(rna_chains, etrna_chain)

    return etrna_chain, rna_chains


def infer_5S_chain(rna_chains):
    chain_length_list = []
    lsu_5S_chain = ''
    for ife in rna_chains:
        pdb, model, chain = ife.split('|')

        query = ChainInfo.query.filter(ChainInfo.pdb_id == pdb) \
                               .filter(ChainInfo.chain_name == chain)

        for row in query:
            chain_length_list.append((ife, row.chain_length))

    for chain in chain_length_list:
        if 110 < int(chain[1]) < 130:
            lsu_5S_chain = chain[0]

    rna_chains = update_chain_list(rna_chains, lsu_5S_chain)

    return lsu_5S_chain, rna_chains


def check_atrna_state_lsu(atrna_chain, corr_asite, corr_psite):
    pass


