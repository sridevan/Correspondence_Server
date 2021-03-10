from collections import OrderedDict
from data.models import ChainInfo, UnitCorrespondence, UnitPairInteractions


# Remove RNA chain from the list once assigned
def update_chain_list(chain_list, chain_to_remove):
    try:
        chain_list.remove(chain_to_remove)
    except:
        pass

    return chain_list


# Get all the RNA chains from the ribosome structure
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


# Get the corresponding nts based on the reference nts in 5J7L
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


def infer_Asite_tRNA_chain(nr_chain, ribosome_components):
    chain_name = None
    if len(nr_chain) == 1:
        chain_name = list(nr_chain)[0]
    elif len(nr_chain) > 1:
        nr_chain.remove(ribosome_components['mRNA'])
        chain_name = list(nr_chain)[0]
    else:
        chain_name = None

    return chain_name


def infer_Esite_tRNA_chain(potential_chain_name, ribosome_components):
    chain_name = None
    if chain_name == ribosome_components['trna_p']:
        chain_name = None
    else:
        chain_name = potential_chain_name

    return chain_name


def infer_interacting_chain(corr_nts, rna_chains, ribosome_components=None, chain_type=None):
    chain_name = None

    if chain_type is None:
        for chain in rna_chains:
            nt2 = '{}|%'.format(chain)
            for nt in corr_nts:
                query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                    .filter(UnitPairInteractions.unit_id_2.like(nt2))

                if query.count() == 1:
                    chain_name = chain

    elif chain_type == 'atrna':
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

        chain_name = infer_Asite_tRNA_chain(nr_chain, ribosome_components)

    elif chain_type == 'etrna':
        for chain in rna_chains:
            nt2 = '{}|%'.format(chain)
            for nt in corr_nts:
                query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                    .filter(UnitPairInteractions.unit_id_2.like(nt2))

                if query.count() == 1:
                    chain_name = chain

        # Check whether the chain is a P-site tRNA since it can form P/E state. If not, assign it as E-site tRNA chain
        chain_name = infer_Esite_tRNA_chain(chain_name, ribosome_components)

    rna_chains = update_chain_list(rna_chains, chain_name)

    return chain_name, rna_chains
