from collections import OrderedDict
from data.models import ChainInfo, UnitCorrespondence, UnitPairInteractions


# Remove RNA chain from the list once assigned
def update_chain_list(chain_list, chain_to_remove):
    try:
        chain_list.remove(chain_to_remove)
    except:
        pass

    return chain_list


# Get all the RNA chains from the ribosome structure except the starting chain which
# is the ife chain
# only the first ife is included
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


# Get the corresponding nts based on the reference nts
# For example, they can be from 5J7L
# query_chain is a tuple of pdb,chain of the query structure
# todo limit to one result because of possible symmetry operators
# think about when the query doesn't exist, catch error
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
    '''

    :param corr_nts:
    :param rna_chains:
    :param ribosome_components:
    :param chain_type:
    :return: Chain_name which is an ife
    '''
    chain_name = None

    if chain_type is None:
        for chain in rna_chains:
            # '5J7L|1|AA|%'
            nt2 = '{}|%'.format(chain)
            for nt in corr_nts:
                query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                    .filter(UnitPairInteractions.unit_id_2.like(nt2))

                # consider same nt interacting more than once
                # consider changing name
                # consider if there's more than one chain
                if query.count() == 1:
                    chain_name = chain
                    # return chain_name

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

    # remove ife once assigned
    rna_chains = update_chain_list(rna_chains, chain_name)

    return chain_name, rna_chains


def test_contacts(chain, ssu_nts_contact):
    nt2 = '{}|%'.format(chain)
    contact = False

    for nt in ssu_nts_contact:
        query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
            .filter(UnitPairInteractions.unit_id_2.like(nt2))

        if query.count() == 1:
            contact = True

    return contact


def infer_tRNA_state(ribosome_components, trna_type, ref_contacts=None, contact1=None, contact2=None, contact3=None):
    SSU_neighboring_contact = False
    LSU_neighboring_contact = False
    LSU_contact = False
    SSU_state = '-'
    LSU_state = '-'
    complete_state = None

    if trna_type == 'trna_a':

        if ribosome_components[trna_type] is not None:

            LSU_contact = test_contacts(ribosome_components[trna_type], contact1)
            SSU_neighboring_contact = test_contacts(ribosome_components[trna_type], contact2)
            LSU_neighboring_contact = test_contacts(ribosome_components[trna_type], contact3)

            if SSU_neighboring_contact is True:
                SSU_state = 'ap'
            else:
                SSU_state = 'A'

            if LSU_contact is True and LSU_neighboring_contact is True:
                LSU_state = 'AP'
            elif LSU_contact is True and LSU_neighboring_contact is False:
                LSU_state = 'A'
            elif LSU_contact is False and LSU_neighboring_contact is True:
                LSU_state = 'P'
            else:
                LSU_state = '*'

            complete_state = '{}/{}'.format(SSU_state, LSU_state)

    elif trna_type == 'trna_p':

        if ribosome_components[trna_type] is not None:

            LSU_contact = test_contacts(ribosome_components[trna_type], contact1)
            SSU_neighboring_contact = test_contacts(ribosome_components[trna_type], contact2)
            LSU_neighboring_contact = test_contacts(ribosome_components[trna_type], contact3)

            if SSU_neighboring_contact is True:
                SSU_state = 'pe'
            else:
                SSU_state = 'P'

            if LSU_contact is True and LSU_neighboring_contact is True:
                LSU_state = 'PE'
            elif LSU_contact is True and LSU_neighboring_contact is False:
                LSU_state = 'P'
            elif LSU_contact is False and LSU_neighboring_contact is True:
                LSU_state = 'E'
            else:
                LSU_state = '*'

            complete_state = '{}/{}'.format(SSU_state, LSU_state)

    elif trna_type == 'trna_e':

        if ribosome_components[trna_type] is not None:
            complete_state = 'E/E'

    return complete_state


def format_trna_states(ribosome_components, state1, state2, state3):
    pass
