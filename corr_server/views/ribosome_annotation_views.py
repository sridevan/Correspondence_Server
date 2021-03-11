import flask
from collections import OrderedDict
from services import ribosome_chains_service as rcs

blueprint = flask.Blueprint('ribosome_annotation', __name__, template_folder='templates')

# This doesn't need to be ordered. But I might want to print this as a csv, so it's good to keep the columns ordered
ribosome_components = OrderedDict()
ribosome_components['SSU_16S'] = None
ribosome_components['LSU_23S'] = None
ribosome_components['LSU_5S'] = None
ribosome_components['mRNA'] = None
ribosome_components['trna_a'] = None
ribosome_components['trna_p'] = None
ribosome_components['trna_e'] = None

# This is the reference dictionary that stores nts that make contacts between specific pair of ribosomal RNA chains
reference_contacts = {
    'ssu_nts_lsu': ['5J7L|1|AA|A|1408', '5J7L|1|AA|A|1418', '5J7L|1|AA|A|1483'],
    'ssu_nts_mrna': ['5J7L|1|AA|G|926', '5J7L|1|AA|4OC|1402', '5J7L|1|AA|C|1403'],
    'ssu_nts_trna_p': ['5J7L|1|AA|G|1338', '5J7L|1|AA|A|1339', '5J7L|1|AA|C|1400'],
    'ssu_nts_trna_a': ['5J7L|1|AA|G|530', '5J7L|1|AA|A|1492', '5J7L|1|AA|A|1493'],
    'ssu_nts_trna_e': ['5J7L|1|AA|G|693', '5J7L|1|AA|A|694'],
    'lsu_nts_trna_e': ['5J7L|1|DA|G|2112', '5J7L|1|DA|G|2421', '5J7L|1|DA|C|2422'],
    'lsu_nts_trna_p': ['5J7L|1|DA|OMG|2251', '5J7L|1|DA|G|2252', '5J7L|1|DA|G|2253'],
    'lsu_nts_trna_a': ['5J7L|1|DA|G|2553', '5J7L|1|DA|G|2583', '5J7L|1|DA|U|2585']
}


"""
#TODO
Refactor the code to get all the correspondences at one go instead of doing it individually
for each chain
"""


@blueprint.route('/ribosome')
def annotate_ribosome_chains():
    # this needs to be ssu chain
    test_ife = '5UYL|1|A'
    # test_ife = '5H5U|1|h'
    # test_ife = '4V9O|1|BA'
    ribosome_components['SSU_16S'] = test_ife
    # Get all RNA chain from the query structure
    # test_ssu is a tuple of pdb and chain of test_ife ('6BU8', 'A')
    # rna chains is a list of rna chain from test_ife ribosome structure except the test ssu
    test_ssu, rna_chains = rcs.get_rna_chain(test_ife)
    # Returns a list of corresponding nts that should interact with LSU if available in the query structure from the
    # reference
    ssu_nts_lsu_corr = rcs.get_nts_corr(reference_contacts['ssu_nts_lsu'], test_ssu)
    ribosome_components['LSU_23S'], rna_chains = rcs.infer_interacting_chain(ssu_nts_lsu_corr, rna_chains)
    # Get the pdb & chain information from the LSU ife
    lsu_pdb, lsu_model, lsu_chain = ribosome_components['LSU_23S'].split('|')
    # Build a tuple of (pdb, chain) for the LSU ife
    test_lsu = (lsu_pdb, lsu_chain)
    # Returns a list of corresponding nts that should interact with mRNA if available in the query structure from the
    # reference
    ssu_nts_mrna_corr = rcs.get_nts_corr(reference_contacts['ssu_nts_mrna'], test_ssu)
    # Infer mRNA chain
    ribosome_components['mRNA'], rna_chains = rcs.infer_interacting_chain(ssu_nts_mrna_corr, rna_chains)
    # Returns a list of corresponding nts that should interact with SSU P-site tRNA if available in the query
    # structure from the reference
    ssu_nts_ptrna_corr = rcs.get_nts_corr(reference_contacts['ssu_nts_trna_p'], test_ssu)
    # Infer P-site tRNA chain
    # name is ambiguous -- SSU/LSU?
    ribosome_components['trna_p'], rna_chains = rcs.infer_interacting_chain(ssu_nts_ptrna_corr, rna_chains)
    # Returns a list of corresponding nts that should interact with SSU A-site tRNA if available in the query
    # structure from the reference
    ssu_nts_atrna_corr = rcs.get_nts_corr(reference_contacts['ssu_nts_trna_a'], test_ssu)
    # Infer A-site tRNA chain
    ribosome_components['trna_a'], rna_chains = rcs.infer_interacting_chain(ssu_nts_atrna_corr, rna_chains,
                                                                            ribosome_components, 'atrna')
    # Returns a list of corresponding nts that should interact with LSU E-site tRNA if available in the query
    # structure from the reference
    lsu_nts_etrna_corr = rcs.get_nts_corr(reference_contacts['lsu_nts_trna_e'], test_lsu)
    # Returns a list of corresponding nts that should interact with SSU E-site tRNA if available in the query
    # structure from the reference
    ssu_nts_etrna_corr = rcs.get_nts_corr(reference_contacts['ssu_nts_trna_e'], test_ssu)
    # Infer E-site tRNA chain
    ribosome_components['trna_e'], rna_chains = rcs.infer_interacting_chain(lsu_nts_etrna_corr, rna_chains,
                                                                            ribosome_components, 'etrna')
    # Returns a list of corresponding nts that should interact with LSU E-site tRNA if available in the query
    # structure from the reference
    lsu_nts_atrna_corr = rcs.get_nts_corr(reference_contacts['lsu_nts_trna_a'], test_lsu)
    # Returns a list of corresponding nts that should interact with LSU E-site tRNA if available in the query
    # structure from the reference
    lsu_nts_ptrna_corr = rcs.get_nts_corr(reference_contacts['lsu_nts_trna_p'], test_lsu)
    # Infer A-site tRNA state
    atrna_state = rcs.infer_tRNA_state(ribosome_components, 'trna_a', reference_contacts, lsu_nts_atrna_corr,
                                       ssu_nts_ptrna_corr, lsu_nts_ptrna_corr)
    # Infer P-site tRNA state
    ptrna_state = rcs.infer_tRNA_state(ribosome_components, 'trna_p', reference_contacts, lsu_nts_ptrna_corr,
                                       ssu_nts_etrna_corr, lsu_nts_etrna_corr)
    # Infer E-site tRNA state
    etrna_state = rcs.infer_tRNA_state(ribosome_components, 'trna_e')
    trna_states = (atrna_state, ptrna_state, etrna_state)
    return str(ribosome_components) + " " + str(trna_states)
