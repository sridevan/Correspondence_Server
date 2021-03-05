import flask
from collections import OrderedDict
from services import ribosome_chains_service as rcs

blueprint = flask.Blueprint('ribosome_annotation', __name__, template_folder='templates')

ribosome_components = OrderedDict()
ribosome_components['SSU_16S'] = None
ribosome_components['LSU_23S'] = None
ribosome_components['LSU_5S'] = None
ribosome_components['mRNA'] = None
ribosome_components['trna_a'] = None
ribosome_components['trna_p'] = None
ribosome_components['trna_e'] = None

ssu_nts_lsu = ['5J7L|1|AA|A|1408', '5J7L|1|AA|A|1418', '5J7L|1|AA|A|1483']
ssu_nts_mrna = ['5J7L|1|AA|G|926', '5J7L|1|AA|4OC|1402', '5J7L|1|AA|C|1403']
ssu_nts_trna_p = ['5J7L|1|AA|G|1338', '5J7L|1|AA|A|1339', '5J7L|1|AA|C|1400']
ssu_nts_trna_a = ['5J7L|1|AA|G|530', '5J7L|1|AA|A|1492', '5J7L|1|AA|A|1493']
lsu_nts_trna_e = ['5J7L|1|DA|G|2112', '5J7L|1|DA|G|2421', '5J7L|1|DA|C|2422']
lsu_nts_trna_p = ['5J7L|1|DA|OMG|2251', '5J7L|1|DA|G|2252', '5J7L|1|DA|G|2253']
lsu_nts_trna_a = ['5J7L|1|DA|G|2553', '5J7L|1|DA|G|2583', '5J7L|1|DA|U|2585']


@blueprint.route('/ribosome')
def calculate_interaction_statistics():
    test_ife = '6BU8|1|A'
    #test_ife = '5H5U|1|h'

    #test_ife = '4V9O|1|BA'
    ribosome_components['SSU_16S'] = test_ife
    # Get all RNA chain from the query structure
    ref_chain_info, rna_chains = rcs.get_rna_chain(test_ife)
    # Get corresponding nts that bind LSU in the query structure from the reference
    ssu_nts_lsu_corr = rcs.get_nts_corr(ssu_nts_lsu, ref_chain_info)
    # Infer 23S Chain
    lsu_23S_chain, rna_chains = rcs.infer_23S_chain(ssu_nts_lsu_corr, rna_chains)
    # Get corresponding nts that bind mRNA in the query structure from the reference
    ssu_nts_mrna_corr = rcs.get_nts_corr(ssu_nts_mrna, ref_chain_info)
    # Infer mRNA Chain
    mrna_chain, rna_chains = rcs.infer_mrna_chain(ssu_nts_mrna_corr, rna_chains)
    # Get corresponding nts that bind SSU P-site tRNA in the query structure from the reference
    ssu_nts_ptrna_corr = rcs.get_nts_corr(ssu_nts_trna_p, ref_chain_info)
    # Infer P-site tRNA chain
    ptrna_chain, rna_chains = rcs.infer_ptrna_chain(ssu_nts_ptrna_corr, rna_chains)
    # Get corresponding nts that bind SSU A-site tRNA in the query structure from the reference
    ssu_nts_atrna_corr = rcs.get_nts_corr(ssu_nts_trna_a, ref_chain_info)
    # Infer A-site tRNA chain
    atrna_chain, rna_chains = rcs.infer_atrna_chain(ssu_nts_atrna_corr, rna_chains, mrna_chain)
    # Infer 5S chain
    lsu_5S_chain, rna_chains = rcs.infer_5S_chain(rna_chains)
    # Get the pdb & chain information for LSU
    lsu_pdb, lsu_model, lsu_chain = lsu_23S_chain.split('|')
    # Get corresponding nts that bind LSU E-site tRNA in the query structure from the reference
    lsu_nts_etrna_corr = rcs.get_nts_corr(lsu_nts_trna_e, (lsu_pdb, lsu_chain))
    # Infer E-site tRNA chain
    etrna_chain, rna_chains = rcs.infer_etrna_chain(lsu_nts_etrna_corr, rna_chains, ptrna_chain)
    ribosome_components['LSU_23S'] = lsu_23S_chain
    ribosome_components['LSU_5S'] = lsu_5S_chain
    ribosome_components['mRNA'] = mrna_chain
    ribosome_components['trna_a'] = atrna_chain
    ribosome_components['trna_p'] = ptrna_chain
    ribosome_components['trna_e'] = etrna_chain
    # Get corresponding nts that bind LSU A-site tRNA in the query structure from the reference
    lsu_nts_atrna_corr = rcs.get_nts_corr(lsu_nts_trna_a, (lsu_pdb, lsu_chain))
    # Get corresponding nts that bind LSU P-site tRNA in the query structure from the reference
    lsu_nts_ptrna_corr = rcs.get_nts_corr(lsu_nts_trna_p, (lsu_pdb, lsu_chain))
    atrna_lsu_state = rcs.check_atrna_state_lsu(atrna_chain, lsu_nts_trna_a, lsu_nts_trna_p)


