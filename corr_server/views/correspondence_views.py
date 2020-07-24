import flask
from flask import render_template, request
import json
import services.correspondence_service as cs
import services.query_service as qs
import services.equivalence_class_service as em
import services.rotation_service as rs
import services.center_service as ccs
import services.pairwise_int_service as ps
import services.chain_info_service as ci
import infrastructure.process_input as pi
import infrastructure.utility as ui

blueprint = flask.Blueprint('correspondence', __name__, template_folder='templates')

bound = [('4V9D', 'AA'), ('4V9D', 'BA'), ('4V9O', 'BA'), ('4V9O', 'DA'), ('4V9O', 'FA'), ('4V9O', 'HA'), ('4V9P', 'BA'),
         ('4V9P', 'DA'), ('4V9P', 'FA'), ('4V9P', 'HA'), ('6GWT', 'a'), ('6GXM', 'a'), ('6GXN', 'a'), ('6GXO', 'a'),
         ('4V54', 'AA'), ('4V54', 'CA'), ('4V55', 'AA'), ('4V55', 'CA'), ('4V9C', 'CA'), ('5KCS', '1a'), ('3J9Y', 'a'),
         ('3JCE', 'a'), ('5AFI', 'a'), ('5UYK', 'A'), ('5UYL', 'A'), ('5UYM', 'A'), ('5UYN', 'A'), ('5UYP', 'A'),
         ('5UYQ', 'A'), ('5WDT', 'a'), ('5WE4', 'a'), ('5WE6', 'a'), ('5WF0', 'a'), ('5WFK', 'a'), ('5WFS', 'a'),
         ('3J9Z', 'SA'), ('3JA1', 'SA'), ('3JCJ', 'g'), ('6DNC', 'A'), ('5NP6', 'D'), ('6H4N', 'a'), ('5H5U', 'h'),
         ('5MDV', '2'), ('5MDW', '2'), ('5MDY', '2'), ('5MGP', 'a'), ('5U4I', 'a'), ('5U9F', 'A'), ('5U9G', 'A'),
         ('6ENF', 'a'), ('6ENJ', 'a'), ('6ENU', 'a'), ('6C4I', 'a'), ('3JBU', 'A'), ('3JBV', 'A'), ('5JTE', 'AA'),
         ('5JU8', 'AA'), ('5NWY', '0'), ('5O2R', 'a'), ('5LZD', 'a'), ('5IQR', '2'), ('5KPS', '27'), ('5KPW', '26'),
         ('5KPX', '26'), ('5L3P', 'a'), ('4V85', 'AA'), ('4V89', 'AA'), ('3JCD', 'a'), ('6O9J', 'a'), ('6O9K', 'a'),
         ('6BY1', 'BA'), ('6BY1', 'AA'), ('6ORE', '2'), ('6OSQ', '2'), ('6ORL', '2'), ('6OUO', '2'), ('6OT3', '2'),
         ('6OSK', '2'), ('6Q97', '2'), ('6Q9A', '2'), ('6NQB', 'A')]

bound_new = [('4V9D', 'AA'),
             ('4V9O', 'BA'),
             ('4V9O', 'DA'),
             ('4V9O', 'FA'),
             ('4V9O', 'HA'),
             ('4V9P', 'BA'),
             ('4V9P', 'DA'),
             ('4V9P', 'FA'),
             ('4V9P', 'HA'),
             ('6GWT', 'a'),
             ('6GXM', 'a'),
             ('6GXN', 'a'),
             ('6GXO', 'a'),
             ('4V54', 'AA'),
             ('4V54', 'CA'),
             ('4V55', 'AA'),
             ('4V55', 'CA'),
             ('4V9C', 'CA'),
             ('5KCS', '1a'),
             ('3J9Y', 'a'),
             ('3JCE', 'a'),
             ('5AFI', 'a'),
             ('5UYK', 'A'),
             ('5UYL', 'A'),
             ('5UYM', 'A'),
             ('5UYN', 'A'),
             ('5UYP', 'A'),
             ('5UYQ', 'A'),
             ('5WDT', 'a'),
             ('5WE4', 'a'),
             ('5WE6', 'a'),
             ('5WF0', 'a'),
             #('5WFK', 'a'),
             ('5WFS', 'a'),
             ('3J9Z', 'SA'),
             ('3JA1', 'SA'),
             ('3JCJ', 'g'),
             ('6DNC', 'A'),
             ('6H4N', 'a'),
             ('5H5U', 'h'),
             ('5MDV', '2'),
             ('5MDW', '2'),
             ('5MDY', '2'),
             ('5MGP', 'a'),
             ('5U4I', 'a'),
             #('5U4J', 'a'),
             ('5U9F', 'A'),
             ('5U9G', 'A'),
             ('6ENF', 'a'),
             ('6ENJ', 'a'),
             ('6ENU', 'a'),
             ('6C4I', 'a'),
             ('3JBU', 'A'),
             ('3JBV', 'A'),
             ('5JTE', 'AA'),
             ('5JU8', 'AA'),
             ('5NWY', '0'),
             ('5O2R', 'a'),
             ('5LZD', 'a'),
             ('5IQR', '2'),
             ('5KPS', '27'),
             ('5KPW', '26'),
             ('5KPX', '26'),
             ('5L3P', 'a'),
             ('4V85', 'AA'),
             ('4V89', 'AA'),
             ('3JCD', 'a'),
             ('6O9K', 'a'),
             ('6OGF', '3'),
             ('6OG7', '3'),
             ('6OSQ', '2'),
             ('6ORL', '2'),
             ('6OUO', '2'),
             ('6OT3', '2'),
             ('6OSK', '2'),
             ('6Q9A', '2'),
             ('6NQB', 'A'),
             ('6SZS', 'a')]

empty = [('4V4Q', 'AA'), ('4V4Q', 'CA'), ('4V50', 'AA'), ('4V50', 'CA'), ('4V5B', 'BA'), ('4V5B', 'DA'), ('4YBB', 'AA'),
         ('4YBB', 'BA'), ('5IT8', 'AA'), ('5IT8', 'BA'), ('5J5B', 'AA'), ('5J5B', 'BA'), ('5J7L', 'AA'), ('5J7L', 'BA'),
         ('5J88', 'AA'), ('5J88', 'BA'), ('5J8A', 'AA'), ('5J8A', 'BA'), ('5J91', 'AA'), ('5J91', 'BA'), ('5JC9', 'AA'),
         ('5JC9', 'BA'), ('5MDZ', '2'), ('6BU8', 'A'), ('4U1U', 'AA'), ('4U1U', 'CA'), ('4U1V', 'AA'), ('4U1V', 'CA'),
         ('4U20', 'AA'), ('4U20', 'CA'), ('4U24', 'AA'), ('4U24', 'CA'), ('4U25', 'AA'), ('4U25', 'CA'), ('4U26', 'AA'),
         ('4U26', 'CA'), ('4U27', 'AA'), ('4U27', 'CA'), ('4V4H', 'AA'), ('4V4H', 'CA'), ('4V52', 'AA'), ('4V52', 'CA'),
         ('4V53', 'AA'), ('4V53', 'CA'), ('4V56', 'AA'), ('4V56', 'CA'), ('4V57', 'AA'), ('4V57', 'CA'), ('4V64', 'AA'),
         ('4V64', 'CA'), ('4V7S', 'AA'), ('4V7S', 'CA'), ('4V7T', 'AA'), ('4V7T', 'CA'), ('4V7U', 'AA'), ('4V7U', 'CA'),
         ('4V7V', 'AA'), ('4V7V', 'CA'), ('4V9C', 'AA'), ('4WF1', 'AA'), ('4WF1', 'CA'), ('4WOI', 'AA'), ('4WOI', 'DA'),
         ('4WWW', 'QA'), ('4WWW', 'XA'), ('5KCR', '1a'), ('5LZA', 'a'), ('4V6C', 'AA'), ('4V6C', 'CA'), ('4V6D', 'AA'),
         ('4V6D', 'CA'), ('4V6E', 'AA'), ('4V6E', 'CA')]

default_ordering = [('0', '5AFI|1|a'), ('1', '5UYM|1|A'), ('2', '5LZD|1|a'), ('3', '5WDT|1|a'), ('4', '5WE4|1|a'),
                    ('5', '5WE6|1|a'), ('6', '3JCE|1|a'), ('7', '5WFS|1|a'), ('8', '6ENJ|1|a'), ('9', '6BU8|1|A'),
                    ('10', '4V6E|1|AA'), ('11', '5UYQ|1|A'), ('12', '4WOI|1|DA'), ('13', '5KPX|1|26'),
                    ('14', '4V9C|1|AA'), ('15', '5O2R|1|a'), ('16', '6DNC|1|A'), ('17', '4V6D|1|AA'),
                    ('18', '4V9D|1|BA'), ('19', '6H4N|1|a'), ('20', '5JTE|1|AA'), ('21', '5WFK|1|a'),
                    ('22', '6ENU|1|a'), ('23', '6GWT|1|a'), ('24', '5KCR|1|1a'), ('25', '5WF0|1|a'),
                    ('26', '5JU8|1|AA'), ('27', '5LZA|1|a'), ('28', '3JCD|1|a'), ('29', '5U9F|1|A'),
                    ('30', '6ENF|1|a'), ('31', '5MDZ|1|2'), ('32', '5NWY|1|0'), ('33', '5MDV|1|2'),
                    ('34', '3JBU|1|A'), ('35', '5UYK|1|A'), ('36', '5U4I|1|a'), ('37', '5UYL|1|A'), ('38', '5MGP|1|a'),
                    ('39', '5U9G|1|A'), ('40', '5MDW|1|2'), ('41', '5UYN|1|A'), ('42', '5KPS|1|27'),
                    ('43', '5IQR|1|2'), ('44', '6C4I|1|a'), ('45', '5KPW|1|26'), ('46', '3J9Z|1|SA'),
                    ('47', '5NP6|1|D'), ('48', '5H5U|1|h'), ('49', '5UYP|1|A'), ('50', '6GXM|1|a'), ('51', '4WOI|1|AA'),
                    ('52', '5MDY|1|2'), ('53', '5L3P|1|a'), ('54', '4V9C|1|CA'), ('55', '5KCS|1|1a'),
                    ('56', '3J9Y|1|a'), ('57', '6GXN|1|a'), ('58', '4V6E|1|CA'), ('59', '4V50|1|CA'),
                    ('60', '4V50|1|AA'), ('61', '4V6D|1|CA'), ('62', '3JCJ|1|g'), ('63', '4V9D|1|AA'),
                    ('64', '6GXO|1|a'), ('65', '3JA1|1|SA'), ('66', '4V9O|1|BA'), ('67', '3JBV|1|A'),
                    ('68', '4V5B|1|BA'), ('69', '4V9O|1|FA'), ('70', '6I7V|1|BA'), ('71', '4WF1|1|CA'),
                    ('72', '4V56|1|AA'), ('73', '4V55|1|AA'), ('74', '4U1U|1|CA'), ('75', '4V64|1|AA'),
                    ('76', '4V57|1|AA'), ('77', '4U20|1|CA'), ('78', '4U27|1|CA'), ('79', '4U25|1|CA'),
                    ('80', '4V4H|1|AA'), ('81', '4V53|1|AA'), ('82', '4V4Q|1|AA'), ('83', '4U1V|1|CA'),
                    ('84', '4V54|1|AA'), ('85', '4V52|1|AA'), ('86', '4U26|1|CA'), ('87', '4U24|1|CA'),
                    ('88', '5JC9|1|BA'), ('89', '4V9O|1|DA'), ('90', '4YBB|1|BA'), ('91', '4V6C|1|CA'),
                    ('92', '5J8A|1|BA'), ('93', '4V7U|1|CA'), ('94', '5J5B|1|BA'), ('95', '5J91|1|BA'),
                    ('96', '5J7L|1|BA'), ('97', '5IT8|1|BA'), ('98', '4V7S|1|CA'), ('99', '4V7V|1|CA'),
                    ('100', '4V7T|1|CA'), ('101', '5J88|1|BA'), ('102', '4WWW|1|XA'), ('103', '4V9P|1|BA'),
                    ('104', '4V9P|1|DA'), ('105', '4U1V|1|AA'), ('106', '4WF1|1|AA'), ('107', '4U20|1|AA'),
                    ('108', '4U27|1|AA'), ('109', '4V7V|1|AA'), ('110', '4U1U|1|AA'), ('111', '4V7U|1|AA'),
                    ('112', '4V7S|1|AA'), ('113', '4U25|1|AA'), ('114', '4V7T|1|AA'), ('115', '4U24|1|AA'),
                    ('116', '5J7L|1|AA'), ('117', '5J91|1|AA'), ('118', '5J5B|1|AA'), ('119', '4V6C|1|AA'),
                    ('120', '4YBB|1|AA'), ('121', '5J8A|1|AA'), ('122', '4WWW|1|QA'), ('123', '5J88|1|AA'),
                    ('124', '5IT8|1|AA'), ('125', '6I7V|1|AA'), ('126', '4U26|1|AA'), ('127', '4V9P|1|HA'),
                    ('128', '5JC9|1|AA'), ('129', '4V9P|1|FA'), ('130', '4V9O|1|HA'), ('131', '4V56|1|CA'),
                    ('132', '4V57|1|CA'), ('133', '4V89|1|AA'), ('134', '4V5B|1|DA'), ('135', '4V55|1|CA'),
                    ('136', '4V64|1|CA'), ('137', '4V53|1|CA'), ('138', '4V54|1|CA'), ('139', '4V52|1|CA'),
                    ('140', '4V85|1|AA'), ('141', '4V4H|1|CA'), ('142', '4V4Q|1|CA')]

new_ordering = [('0', '4V4Q|1|CA'), ('1', '4V4H|1|CA'), ('2', '4V53|1|CA'), ('3', '4V52|1|CA'), ('4', '4V54|1|CA'),
                ('5', '4V64|1|CA'), ('6', '4V55|1|CA'), ('7', '4V57|1|CA'), ('8', '4V5B|1|DA'), ('9', '4V56|1|CA'),
                ('10', '4V9P|1|HA'), ('11', '4V9P|1|FA'), ('12', '4V85|1|AA'), ('13', '4V9O|1|HA'),
                ('14', '4V89|1|AA'), ('15', '4V55|1|AA'), ('16', '4V57|1|AA'), ('17', '4V53|1|AA'),
                ('18', '4V54|1|AA'), ('19', '4V52|1|AA'), ('20', '4V4Q|1|AA'), ('21', '4V4H|1|AA'),
                ('22', '4V64|1|AA'), ('23', '4V56|1|AA'), ('24', '4V9P|1|BA'), ('25', '4V7V|1|AA'),
                ('26', '4V7S|1|AA'), ('27', '4V7U|1|AA'), ('28', '4V6C|1|AA'), ('29', '4V7T|1|AA'),
                ('30', '4WWW|1|QA'), ('31', '5IT8|1|AA'), ('32', '5JC9|1|AA'), ('33', '4U26|1|AA'),
                ('34', '4U24|1|AA'), ('35', '5J7L|1|AA'), ('36', '5J5B|1|AA'), ('37', '5J91|1|AA'),
                ('38', '5J8A|1|AA'), ('39', '5J88|1|AA'), ('40', '4YBB|1|AA'), ('41', '4V9P|1|DA'),
                ('42', '4U25|1|AA'), ('43', '4U27|1|AA'), ('44', '4V7U|1|CA'), ('45', '4V7T|1|CA'),
                ('46', '4V6C|1|CA'), ('47', '4V7S|1|CA'), ('48', '4WWW|1|XA'), ('49', '4V7V|1|CA'),
                ('50', '4V5B|1|BA'), ('51', '3JBV|1|A'), ('52', '4V9O|1|DA'), ('53', '4WF1|1|AA'),
                ('54', '4U1U|1|AA'), ('55', '4U1V|1|AA'), ('56', '4U20|1|AA'), ('57', '3JA1|1|SA'),
                ('58', '4V9O|1|FA'), ('59', '4V50|1|AA'), ('60', '4V50|1|CA'), ('61', '5J7L|1|BA'),
                ('62', '5J5B|1|BA'), ('63', '5J91|1|BA'), ('64', '5IT8|1|BA'), ('65', '5J88|1|BA'),
                ('66', '5J8A|1|BA'), ('67', '5JC9|1|BA'), ('68', '4YBB|1|BA'), ('69', '4U26|1|CA'),
                ('70', '4U24|1|CA'), ('71', '4V6D|1|CA'), ('72', '5H5U|1|h'), ('73', '4V9O|1|BA'),
                ('74', '3JBU|1|A'), ('75', '5NP6|1|D'), ('76', '3JCD|1|a'), ('77', '6C4I|1|a'),
                ('78', '3J9Z|1|SA'), ('79', '5MGP|1|a'), ('80', '5MDZ|1|2'), ('81', '5MDV|1|2'),
                ('82', '5MDW|1|2'), ('83', '5MDY|1|2'), ('84', '6ENF|1|a'), ('85', '5U9F|1|A'),
                ('86', '4V9D|1|AA'), ('87', '5UYL|1|A'), ('88', '4U1U|1|CA'), ('89', '4U20|1|CA'),
                ('90', '4U1V|1|CA'), ('91', '4WF1|1|CA'), ('92', '5UYN|1|A'), ('93', '5UYP|1|A'),
                ('94', '5UYK|1|A'), ('95', '4U25|1|CA'), ('96', '4U27|1|CA'), ('97', '5U9G|1|A'),
                ('98', '6ENU|1|a'), ('99', '5KPS|1|27'), ('100', '5U4I|1|a'), ('101', '5KPW|1|26'),
                ('102', '5L3P|1|a'), ('103', '5IQR|1|2'), ('104', '4V6E|1|CA'), ('105', '5NWY|1|0'),
                ('106', '5O2R|1|a'), ('107', '6DNC|1|A'), ('108', '3J9Y|1|a'), ('109', '3JCJ|1|g'),
                ('110', '5KCS|1|1a'), ('111', '5WF0|1|a'), ('112', '5KCR|1|1a'), ('113', '5UYQ|1|A'),
                ('114', '4V6E|1|AA'), ('115', '5JU8|1|AA'), ('116', '4V9D|1|BA'), ('117', '4WOI|1|AA'),
                ('118', '4V9C|1|CA'), ('119', '4V6D|1|AA'), ('120', '5WFS|1|a'), ('121', '5WE4|1|a'),
                ('122', '5WDT|1|a'), ('123', '5UYM|1|A'), ('124', '6BU8|1|A'), ('125', '6ENJ|1|a'),
                ('126', '5LZD|1|a'), ('127', '5KPX|1|26'), ('128', '5JTE|1|AA'), ('129', '4WOI|1|DA'),
                ('130', '5WE6|1|a'), ('131', '3JCE|1|a'), ('132', '4V9C|1|AA')]


@blueprint.route('/correspondence/<method>/<ife>/<selection>', defaults={'core': None})
@blueprint.route('/correspondence/<method>/<ife>/<selection>/<core>')
# @response(template_file='packages/details.html')
def correspondence_geometric(method, ife, selection, core):
    if method == 'geometric' and core is None:
        query_ife = ife
        query_list = pi.input_type(selection)
        query_type = pi.check_query(query_list)
        query_units = qs.get_query_units(query_type, query_list, query_ife)
        rejected_members, ec_members, ec_id, nr_release = em.get_ec_members(query_ife)
        corr_complete, corr_std = cs.get_correspondence(query_units, ec_members)
        ife_list, coord_data = ui.build_coord(corr_complete)
        # Get the pairwise annotation for the instances in the EC
        pw_info, pw_sorted = ps.get_pairwise_annotation(corr_complete, query_units, ife_list)
        # Get the tertiary pairwise annotation
        pw_lr, rna_chain = ps.get_pairwise_tertiary(corr_complete, ife_list)
        chain_info_rna = ci.get_chain_info(rna_chain)
        rp_contacts, protein_chain = ps.get_pairwise_rnap(corr_complete, ife_list)
        chain_info_protein = ci.get_chain_info(protein_chain)
        chain_info = ui.merge_chain_info(chain_info_rna, chain_info_protein)
        # Get the rotation data for calculating discrepancy
        rotation_data = rs.get_rotation(corr_std)
        # Get the center data for calculating discrepancy
        center_data = ccs.get_center(corr_std)
        # Calculate discrepancy using the geometric method
        discrepancy_data = ui.calculate_geometric_disc(ife_list, rotation_data, center_data)
        # Order the instances by similarity
        ifes_ordered, coord_ordered = ui.get_ordering(ife_list, discrepancy_data, coord_data)
        # ifes_ordered, coord_ordered = ui.get_ordering_manual(ife_list, coord_data, new_ordering)
        # Get discrepancy statistics and build the heatmap data for display
        max_disc, percentile, mean, median, heatmap_data, dist_data = ui.build_heatmap_data(discrepancy_data, ifes_ordered)
        dist_csv = ui.build_dist(dist_data, query_units)
        # Get all the annotation from the definition file
        calculated_head, calculated_intersubunit, description, structure_method, structure_resolution, \
        principal_investigator, publication_year, trna_occupancy, functional_state, factors_bound, \
        antibiotic_bound, codon_pairing = ui.get_annotation_new(ifes_ordered)
        # Reorder the pairwise annotation based on the new ordering
        pw_info_ordered = ui.reorder_pw(ifes_ordered, pw_info)
        pw_lr_ordered = ui.reorder_pw(ifes_ordered, pw_lr)
        rp_contacts_ordered = ui.reorder_pw(ifes_ordered, rp_contacts)
        chain_info_ordered = ui.reorder_chain(ifes_ordered, chain_info)
        return render_template("correspondence_display.html", query_nts=query_units,
                               coord=coord_ordered, coord_core=None, ifes=ifes_ordered, maxDisc=max_disc, p2=percentile,
                               data=heatmap_data, trna_occupancy=trna_occupancy, functional_state=functional_state,
                               factors_bound=factors_bound,
                               calculated_rotation=calculated_intersubunit,
                               calculated_head=calculated_head, antibiotic_bound=antibiotic_bound,
                               description=description, structure_method=structure_method,
                               structure_resolution=structure_resolution, principal_investigator=principal_investigator,
                               publication_year=publication_year, pw_info=pw_info_ordered, pw_list=pw_sorted,
                               pw_tertiary=pw_lr_ordered, rp_contacts=rp_contacts_ordered, release_id=nr_release,
                               ec_id=ec_id, chain_info=chain_info_ordered, mean=mean, mdn=median)
    elif method == 'relative' and core is not None:
        query_ife = ife
        query_list = pi.input_type(selection)
        query_type = pi.check_query(query_list)
        core_selection = core.split(",")
        query_units = qs.get_query_units(query_type, query_list, query_ife)
        core_units = qs.get_complete_units(core_selection, query_ife)
        rejected_members, ec_members, ec_id, nr_release = em.get_ec_members(query_ife)
        # Get correspondence for the query nts
        corr_complete, corr_std = cs.get_correspondence(query_units, bound_new)
        # Get correspondence for the core nts
        core_complete = cs.get_correspondence_core(core_units, bound_new)
        ife_list, coord_data = ui.build_coord_relative(core_complete, corr_complete)
        # Merge the correspondence between core nts and query nts
        corr_complete = ui.merge_list(core_complete, corr_std)
        # Get the pairwise annotation for the instances in the EC
        pw_info, pw_sorted = ps.get_pairwise_annotation(corr_std, query_units, ife_list)
        # Get the tertiary pairwise annotation
        pw_lr, rna_chain = ps.get_pairwise_tertiary(corr_complete, ife_list)
        chain_info_rna = ci.get_chain_info(rna_chain)
        rp_contacts, protein_chain = ps.get_pairwise_rnap(corr_complete, ife_list)
        chain_info_protein = ci.get_chain_info(protein_chain)
        chain_info = ui.merge_chain_info(chain_info_rna, chain_info_protein)
        # Get the center data for calculating discrepancy
        center_data = ccs.get_center(corr_complete)
        # Calculate discrepancy using the geometric method
        discrepancy_data = ui.calculate_relative_disc(ife_list, center_data, len(core_units), len(query_units))
        # Order the instances by similarity
        ifes_ordered, coord_ordered = ui.get_ordering(ife_list, discrepancy_data, coord_data)
        # Get discrepancy statistics and build the heatmap data for display
        max_disc, percentile, heatmap_data = ui.build_heatmap_data(discrepancy_data, ifes_ordered)
        # Get all the annotation from the definition file
        calculated_head, calculated_intersubunit, description, structure_method, structure_resolution, \
        principal_investigator, publication_year, trna_occupancy, functional_state, factors_bound, \
        antibiotic_bound, codon_pairing = ui.get_annotation_new(ifes_ordered)
        # Reorder the pairwise annotation based on the new ordering
        pw_info_ordered = ui.reorder_pw(ifes_ordered, pw_info)
        pw_lr_ordered = ui.reorder_pw(ifes_ordered, pw_lr)
        rp_contacts_ordered = ui.reorder_pw(ifes_ordered, rp_contacts)
        chain_info_ordered = ui.reorder_chain(ifes_ordered, chain_info)
        return render_template("correspondence_display.html", query_nts=query_units,
                               coord=coord_ordered, coord_core=None, ifes=ifes_ordered, maxDisc=max_disc, p2=percentile,
                               data=heatmap_data, trna_occupancy=trna_occupancy, functional_state=functional_state,
                               factors_bound=factors_bound,
                               calculated_rotation=calculated_intersubunit,
                               calculated_head=calculated_head, antibiotic_bound=antibiotic_bound,
                               description=description, structure_method=structure_method,
                               structure_resolution=structure_resolution, principal_investigator=principal_investigator,
                               publication_year=publication_year, pw_info=pw_info_ordered, pw_list=pw_sorted,
                               pw_tertiary=pw_lr_ordered, rp_contacts=rp_contacts_ordered, release_id=nr_release,
                               ec_id=ec_id, chain_info=chain_info_ordered)
