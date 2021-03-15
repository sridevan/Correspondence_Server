from collections import OrderedDict
from data.models import ChainInfo, UnitCorrespondence, UnitPairInteractions


# Remove ribosome component ife once it has been assigned
def update_chain_list(chain_list, chain_to_remove):
    try:
        chain_list.remove(chain_to_remove)
    except:
        pass

    return chain_list


# Get all the RNA chains from the ribosome structure except the starting chain which
# is the ife chain
# only the first ife is included
def get_components_ife(ife):
    pdb, _, chain = ife.split('|')

    molecule_type = 'Polyribonucleotide (RNA)'

    chain_ids = []
    # Get all RNA chains from the ribosome except the query chain (16S in this example)
    query = ChainInfo.query.filter(ChainInfo.pdb_id == pdb) \
        .filter(ChainInfo.entity_macromolecule_type == molecule_type) \
        .filter(ChainInfo.chain_name != chain)

    for row in query:
        chain_ids.append(row.chain_name)

    # Build the ifes from the pdb and chain information. Assume model num is 1
    ife_list = ['{}|1|{}'.format(pdb, elem) for elem in chain_ids]
    query_info = (pdb, chain)

    return query_info, ife_list


def get_units_correspondence(units_list, test_info):
    """
    This query returns a list of corresponding unit_ids from a particular chain in a structure based on a
    given list of unit_ids

    #TODO
    Consider symmetry operators

    :param units_list: List
        Query list of unit_ids
    :param test_info: Tuple
        A tuple of (pdb, chain)
    :return: units_corr: List
        A list of corresponding unit_ids in the test_info
    """
    pdb, chain = test_info[0], test_info[1]
    units_corr = []

    for nt in units_list:
        query = UnitCorrespondence.query.filter(UnitCorrespondence.unit_id_1 == nt) \
            .filter(UnitCorrespondence.pdb_id_2 == pdb) \
            .filter(UnitCorrespondence.chain_name_2 == chain)

        for row in query:
            units_corr.append(row.unit_id_2)

    return units_corr


def units_correspondence(reference_units, test_ssu, test_lsu):
    corr_dict = {}
    for key, value in reference_units.items():
        label_1, _, label_3 = key.split('_')
        new_key = '{}_{}'.format(label_1, label_3)
        if label_1 == 'ssu':
            units_list = get_units_correspondence(value, test_ssu)
            corr_dict[new_key] = units_list
        else:
            units_list = get_units_correspondence(value, test_lsu)
            corr_dict[new_key] = units_list

    return corr_dict


def infer_atrna_ife(ifes, ribosome_components):
    if len(ifes) == 1:
        atrna_ife = list(ifes)[0]
    # assume there could only be two 
    elif len(ifes) > 1:
        ifes.remove(ribosome_components['mRNA'])
        atrna_ife = list(ifes)[0]
    else:
        atrna_ife = None

    return atrna_ife


def infer_etrna_ife(possible_etrna_ife, ribosome_components):
    """
    Check if the E-site trna is the same as the P-site trna. We are checking for the presence of E-tRNA by "looking" at
    chains that could possibly interact with the E-tRNA binding site in the LSU. Since P-tRNA can form P/E state, we
    need to test for this possibility.

    :param possible_etrna_ife: String
        Possible E-tRNA ife
    :param ribosome_components: Dict
        A dict containing ribosome chains as keys and the assigned ifes as values
    :return: String
        E-tRNA ife
    """

    if possible_etrna_ife == ribosome_components['peptidyl-trna']:
        etrna_ife = None
    else:
        etrna_ife = possible_etrna_ife

    return etrna_ife


def get_interacting_ife(corr_units, component_ifes):
    """
    :param corr_units:
    :param component_ifes:
    :return:
    """
    interacting_ife = None
    for ife in component_ifes:
        # '5J7L|1|AA|%'
        unit2 = '{}|%'.format(ife)
        for nt in corr_units:
            query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                .filter(UnitPairInteractions.unit_id_2.like(unit2)) \
                .count()

            # consider same nt interacting more than once
            # consider changing name
            # consider if there's more than one chain
            if query >= 1:
                interacting_ife = ife

    return interacting_ife


def infer_interacting_chain(corr_nts, rna_chains, ribosome_components=None, chain_type=None):
    """
    :param corr_nts:
    :param rna_chains:
    :param ribosome_components:
    :param chain_type:
    :return: Chain_name which is an ife
    """
    chain_name = None

    if chain_type is None:
        for chain in rna_chains:
            # '5J7L|1|AA|%'
            nt2 = '{}|%'.format(chain)
            for nt in corr_nts:
                query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                    .filter(UnitPairInteractions.unit_id_2.like(nt2)) \
                    .count()

                # consider same nt interacting more than once
                # consider changing name
                # consider if there's more than one chain
                if query >= 1:
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

        chain_name = infer_atrna_ife(nr_chain, ribosome_components)

    elif chain_type == 'etrna':
        for chain in rna_chains:
            nt2 = '{}|%'.format(chain)
            for nt in corr_nts:
                query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == nt) \
                    .filter(UnitPairInteractions.unit_id_2.like(nt2))

                if query.count() == 1:
                    chain_name = chain

        # Check whether the chain is a P-site tRNA since it can form P/E state. If not, assign it as E-site tRNA chain
        chain_name = infer_etrna_ife(chain_name, ribosome_components)

    # remove ife from the original list once it has been assigned
    rna_chains = update_chain_list(rna_chains, chain_name)

    return chain_name, rna_chains


def check_neighboring_contacts(ife, units_corr):
    unit2 = '{}|%'.format(ife)
    contacts_made = False

    for unit1 in units_corr:
        query = UnitPairInteractions.query.filter(UnitPairInteractions.unit_id_1 == unit1) \
            .filter(UnitPairInteractions.unit_id_2.like(unit2)) \
            .count()

        if query >= 1:
            contacts_made = True

    return contacts_made


def infer_tRNA_state(ribosome_components, trna_type, corr_dict):
    complete_state = None
    if trna_type == 'aminoacyl-trna':

        if ribosome_components[trna_type] is not None:

            LSU_contact = check_neighboring_contacts(ribosome_components[trna_type], corr_dict['lsu_atrna'])
            SSU_neighboring_contact = check_neighboring_contacts(ribosome_components[trna_type], corr_dict['ssu_ptrna'])
            LSU_neighboring_contact = check_neighboring_contacts(ribosome_components[trna_type], corr_dict['lsu_ptrna'])

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

    elif trna_type == 'peptidyl-trna':

        if ribosome_components[trna_type] is not None:

            LSU_contact = check_neighboring_contacts(ribosome_components[trna_type], corr_dict['lsu_ptrna'])
            SSU_neighboring_contact = check_neighboring_contacts(ribosome_components[trna_type], corr_dict['ssu_etrna'])
            LSU_neighboring_contact = check_neighboring_contacts(ribosome_components[trna_type], corr_dict['lsu_etrna'])

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

    elif trna_type == 'exit-trna':

        if ribosome_components[trna_type] is not None:
            complete_state = 'E/E'

    return complete_state

