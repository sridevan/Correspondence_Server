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
ribosome_components['aminoacyl-trna'] = None
ribosome_components['peptidyl-trna'] = None
ribosome_components['exit-trna'] = None

# This is the reference dictionary that stores nts that make contacts between specific pair of ribosomal RNA chains
reference_units_ssu = {
    'ssu_nts_lsu': ['5J7L|1|AA|A|1408', '5J7L|1|AA|A|1418', '5J7L|1|AA|A|1483'],
    'ssu_nts_mrna': ['5J7L|1|AA|G|926', '5J7L|1|AA|4OC|1402', '5J7L|1|AA|C|1403'],
    'ssu_nts_ptrna': ['5J7L|1|AA|G|1338', '5J7L|1|AA|A|1339', '5J7L|1|AA|C|1400'],
    'ssu_nts_atrna': ['5J7L|1|AA|G|530', '5J7L|1|AA|A|1492', '5J7L|1|AA|A|1493'],
    'ssu_nts_etrna': ['5J7L|1|AA|G|693', '5J7L|1|AA|A|694']

}

reference_units_lsu = {
    'lsu_nts_atrna': ['5J7L|1|DA|G|2553', '5J7L|1|DA|G|2583', '5J7L|1|DA|U|2585'],
    'lsu_nts_etrna': ['5J7L|1|DA|G|2112', '5J7L|1|DA|G|2421', '5J7L|1|DA|C|2422'],
    'lsu_nts_ptrna': ['5J7L|1|DA|OMG|2251', '5J7L|1|DA|G|2252', '5J7L|1|DA|G|2253'],
}


reference_units = {
    'ssu_nts_lsu': ['5J7L|1|AA|A|1408', '5J7L|1|AA|A|1418', '5J7L|1|AA|A|1483'],
    'ssu_nts_mrna': ['5J7L|1|AA|G|926', '5J7L|1|AA|4OC|1402', '5J7L|1|AA|C|1403'],
    'ssu_nts_ptrna': ['5J7L|1|AA|G|1338', '5J7L|1|AA|A|1339', '5J7L|1|AA|C|1400'],
    'ssu_nts_atrna': ['5J7L|1|AA|G|530', '5J7L|1|AA|A|1492', '5J7L|1|AA|A|1493'],
    'ssu_nts_etrna': ['5J7L|1|AA|G|693', '5J7L|1|AA|A|694'],
    'lsu_nts_atrna': ['5J7L|1|DA|G|2553', '5J7L|1|DA|G|2583', '5J7L|1|DA|U|2585'],
    'lsu_nts_etrna': ['5J7L|1|DA|G|2112', '5J7L|1|DA|G|2421', '5J7L|1|DA|C|2422'],
    'lsu_nts_ptrna': ['5J7L|1|DA|OMG|2251', '5J7L|1|DA|G|2252', '5J7L|1|DA|G|2253']
}


@blueprint.route('/ribosome')
def annotate_ribosome_chains():
    # this needs to be ssu chain
    test_ife = '5UYL|1|A'
    ribosome_components['SSU_16S'] = test_ife
    test_ssu, components_ife = rcs.get_components_ife(test_ife)
    # Returns a list of unit_ids that should interact with the 23S in the test_ife based on the ref
    ssu_nts_lsu_corr = rcs.get_units_correspondence(reference_units['ssu_nts_lsu'], test_ssu)
    # Infer 23S ife
    ribosome_components['LSU_23S'], components_ife = rcs.infer_interacting_chain(ssu_nts_lsu_corr,
                                                                                 components_ife)
    # Get the pdb & chain information from the LSU ife
    lsu_pdb, _, lsu_chain = ribosome_components['LSU_23S'].split('|')
    # Build a tuple of (pdb, chain)
    test_lsu = (lsu_pdb, lsu_chain)
    test_units_corr = rcs.units_correspondence(reference_units, test_ssu, test_lsu)
    # Infer mRNA ife
    ribosome_components['mRNA'], components_ife = rcs.infer_interacting_chain(test_units_corr['ssu_mrna'],
                                                                              components_ife)

    # Infer P-tRNA ife
    ribosome_components['peptidyl-trna'], components_ife = rcs.infer_interacting_chain(test_units_corr['ssu_ptrna'],
                                                                                       components_ife)
    # Infer A-tRNA ife
    ribosome_components['aminoacyl-trna'], components_ife = rcs.infer_interacting_chain(test_units_corr['ssu_atrna'],
                                                                                        components_ife,
                                                                                        ribosome_components,
                                                                                        'atrna')
    # Infer E-tRNA ife
    ribosome_components['exit-trna'], components_ife = rcs.infer_interacting_chain(test_units_corr['lsu_etrna'],
                                                                                   components_ife,
                                                                                   ribosome_components, 'etrna')
    # Infer A-tRNA state
    atrna_state = rcs.infer_tRNA_state(ribosome_components, 'aminoacyl-trna', test_units_corr)
    # Infer P-tRNA state
    ptrna_state = rcs.infer_tRNA_state(ribosome_components, 'peptidyl-trna', test_units_corr)
    # Infer E-tRNA state
    etrna_state = rcs.infer_tRNA_state(ribosome_components, 'exit-trna', test_units_corr)
    trna_states = (atrna_state, ptrna_state, etrna_state)
    return str(ribosome_components)
