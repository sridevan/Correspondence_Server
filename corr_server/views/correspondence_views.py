import flask
from flask import render_template, request
import json
import services.correspondence_service as cs
import services.query_service as qs
import services.equivalence_class_service as em
import services.rotation_service as rs
import services.center_service as ccs
import services.pairwise_int_service as ps
import infrastructure.process_input as pi
import infrastructure.utility as ui

blueprint = flask.Blueprint('correspondence', __name__, template_folder='templates')

ife_trna = [('4V50', 'AA'), ('4V50', 'CA'), ('4V9D', 'AA'), ('4V9D', 'BA'), ('5MDZ', '2'), ('6BU8', 'A'), ('6GWT', 'a'),
            ('6GXM', 'a'), ('6GXN', 'a'), ('6GXO', 'a'), ('4V9C', 'AA'), ('4V9C', 'CA'), ('4WOI', 'AA'), ('4WOI', 'DA'),
            ('5KCR', '1a'), ('5KCS', '1a'), ('3J9Y', 'a'), ('3JCD', 'a'), ('3JCE', 'a'), ('5UYK', 'A'),
            ('5UYL', 'A'), ('5UYM', 'A'), ('5UYN', 'A'), ('5UYP', 'A'), ('5UYQ', 'A'), ('5WDT', 'a'), ('5WE4', 'a'),
            ('5WE6', 'a'), ('5WF0', 'a'), ('5WFS', 'a'), ('3J9Z', 'SA'), ('3JA1', 'SA'), ('3JCJ', 'g'),
            ('6DNC', 'A'), ('5NP6', 'D'), ('6H4N', 'a'), ('5H5U', 'h'), ('5MDV', '2'), ('5MDW', '2'), ('5MDY', '2'),
            ('5MGP', 'a'), ('5U4I', 'a'), ('5U4J', 'a'), ('5U9F', 'A'), ('5U9G', 'A'), ('6ENF', 'a'), ('6ENJ', 'a'),
            ('6ENU', 'a'), ('6C4I', 'a'), ('3JBU', 'A'), ('3JBV', 'A'), ('5JTE', 'AA'), ('5JU8', 'AA'), ('5NWY', '0'),
            ('5O2R', 'a'), ('5LZD', 'a'), ('5IQR', '2'), ('5KPS', '27'), ('5KPW', '26'), ('5KPX', '26'),
            ('5L3P', 'a'), ('4V6D', 'AA'), ('4V6D', 'CA'), ('4V6E', 'AA'), ('4V6E', 'CA'), ('4V55', 'AA'),
            ('4V55', 'CA'), ('4V9P', 'BA'), ('4V9P', 'DA'), ('4V9P', 'FA'), ('4V9P', 'HA'),
            ('4V9O', 'BA'), ('4V9O', 'DA'), ('4V9O', 'FA'), ('4V9O', 'HA'), ('4V85', 'AA'), ('4V89', 'AA'),
            ('4V54', 'AA'), ('4V54', 'CA')]

ife_empty = [('4V4Q', 'AA'), ('4V4Q', 'CA'), ('4V5B', 'BA'), ('4V5B', 'DA'),
             ('4YBB', 'AA'), ('4YBB', 'BA'), ('5IT8', 'AA'), ('5IT8', 'BA'), ('5J5B', 'AA'), ('5J5B', 'BA'),
             ('5J7L', 'AA'), ('5J7L', 'BA'), ('5J88', 'AA'), ('5J88', 'BA'), ('5J8A', 'AA'), ('5J8A', 'BA'),
             ('5J91', 'AA'), ('5J91', 'BA'), ('5JC9', 'AA'), ('5JC9', 'BA'), ('6I7V', 'AA'), ('6I7V', 'BA'),
             ('4U1U', 'AA'), ('4U1U', 'CA'), ('4U1V', 'AA'), ('4U1V', 'CA'), ('4U20', 'AA'), ('4U20', 'CA'),
             ('4U24', 'AA'), ('4U24', 'CA'), ('4U25', 'AA'), ('4U25', 'CA'), ('4U26', 'AA'), ('4U26', 'CA'),
             ('4U27', 'AA'), ('4U27', 'CA'), ('4V4H', 'AA'), ('4V4H', 'CA'), ('4V52', 'AA'), ('4V52', 'CA'),
             ('4V53', 'AA'), ('4V53', 'CA'), ('4V56', 'AA'), ('4V56', 'CA'), ('4V57', 'AA'), ('4V57', 'CA'),
             ('4V64', 'AA'), ('4V64', 'CA'), ('4V7S', 'AA'), ('4V7S', 'CA'), ('4V7T', 'AA'), ('4V7T', 'CA'),
             ('4V7U', 'AA'), ('4V7U', 'CA'), ('4V7V', 'AA'), ('4V7V', 'CA'), ('4WF1', 'AA'), ('4WF1', 'CA'),
             ('4WWW', 'QA'), ('4WWW', 'XA'), ('4V6C', 'AA'), ('4V6C', 'CA')]


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
        corr_complete, corr_std = cs.get_correspondence(query_units, ife_trna)
        ife_list, coord_data = ui.build_coord(corr_std)
        # Get the pairwise annotation for the instances in the EC
        pw_info, pw_sorted = ps.get_pairwise_annotation(corr_complete, query_units, ife_list)
        # Get the rotation data for calculating discrepancy
        rotation_data = rs.get_rotation(corr_std)
        # Get the center data for calculating discrepancy
        center_data = ccs.get_center(corr_std)
        # Calculate discrepancy using the geometric method
        discrepancy_data = ui.calculate_geometric_disc(ife_list, rotation_data, center_data)
        # Order the instances by similarity
        ifes_ordered, coord_ordered = ui.get_ordering(ife_list, discrepancy_data, coord_data)
        # Get discrepancy statistics and build the heatmap data for display
        max_disc, percentile, heatmap_data = ui.build_heatmap_data(discrepancy_data, ifes_ordered)
        # Get all the annotation from the definition file
        trna_occupancy, functional_state, factors_bound, antibiotic_bound, reported_intersubunit, \
        calculated_intersubunit, reported_head, calculated_head = ui.get_annotation(ifes_ordered)
        # Reorder the pairwise annotation based on the new ordering
        pw_info_ordered = ui.reorder_pw(ifes_ordered, pw_info)
        return render_template("correspondence_display.html", query_nts=query_units,
                               coord=coord_ordered, coord_core=None, ifes=ifes_ordered, maxDisc=max_disc, p2=percentile,
                               data=heatmap_data, trna_occupancy=trna_occupancy, functional_state=functional_state,
                               factors_bound=factors_bound, reported_rotation=reported_intersubunit,
                               calculated_rotation=calculated_intersubunit, reported_head=reported_head,
                               calculated_head=calculated_head, antibiotic_bound=antibiotic_bound,
                               pw_info=pw_info_ordered, pw_list=pw_sorted, release_id=nr_release, ec_id=ec_id)
    elif method == 'relative' and core is not None:
        query_ife = ife
        query_list = pi.input_type(selection)
        query_type = pi.check_query(query_list)
        core_selection = core.split(",")
        query_units = qs.get_query_units(query_type, query_list, query_ife)
        core_units = qs.get_complete_units(core_selection, query_ife)
        rejected_members, ec_members, ec_id, nr_release = em.get_ec_members(query_ife)
        # Get correspondence for the query nts
        corr_complete, corr_std = cs.get_correspondence(query_units, ec_members)
        # Get correspondence for the core nts
        core_complete = cs.get_correspondence_core(core_units, ec_members)
        ife_list, coord_data = ui.build_coord_relative(core_complete, corr_complete)
        # Merge the correspondence between core nts and query nts
        corr_complete = ui.merge_list(core_complete, corr_std)
        # Get the pairwise annotation for the instances in the EC
        pw_info, pw_sorted = ps.get_pairwise_annotation(corr_std, query_units, ife_list)
        # Get the center data for calculating discrepancy
        center_data = ccs.get_center(corr_complete)
        # Calculate discrepancy using the geometric method
        discrepancy_data = ui.calculate_relative_disc(ife_list, center_data, len(core_units), len(query_units))
        # Order the instances by similarity
        ifes_ordered, coord_ordered = ui.get_ordering(ife_list, discrepancy_data, coord_data)
        # Get discrepancy statistics and build the heatmap data for display
        max_disc, percentile, heatmap_data = ui.build_heatmap_data(discrepancy_data, ifes_ordered)
        # Get all the annotation from the definition file
        trna_occupancy, functional_state, factors_bound, antibiotic_bound, reported_intersubunit, \
        calculated_intersubunit, reported_head, calculated_head = ui.get_annotation(ifes_ordered)
        # Reorder the pairwise annotation based on the new ordering
        pw_info_ordered = ui.reorder_pw(ifes_ordered, pw_info)
        return render_template("correspondence_display.html", query_nts=query_units,
                               coord=coord_ordered, ifes=ifes_ordered, maxDisc=max_disc,
                               p2=percentile, data=heatmap_data, trna_occupancy=trna_occupancy,
                               functional_state=functional_state,  factors_bound=factors_bound,
                               reported_rotation=reported_intersubunit, calculated_rotation=calculated_intersubunit,
                               reported_head=reported_head, calculated_head=calculated_head,
                               antibiotic_bound=antibiotic_bound, pw_info=pw_info_ordered, pw_list=pw_sorted)



"""
@blueprint.route('/correspondence/relative/<ife>/<core>/<selection>')
def correspondence_geometric(method, ife, core, selection):
    query_list = pi.input_type(selection)
    query_type = pi.check_query(query_list)
    query_units, query_ife = qs.get_query_units_relative(query_type, query_list)
    core_units, query_units = ui.partition_list(query_units)
    rejected_members, ec_members = em.get_ec_members(query_ife)
    # Get correspondence for the query nts
    corr_complete, corr_std = cs.get_correspondence(query_units, ec_members)
    # Get correspondence for the core nts
    core_complete = cs.get_correspondence_core(core_units, ec_members)
    ife_list, coord_data = ui.build_coord(corr_complete)
    # Merge the correspondence between core nts and query nts
    corr_complete = ui.merge_list(core_complete, corr_complete)
    # Get the pairwise annotation for the instances in the EC
    pw_info, pw_sorted = ps.get_pairwise_annotation(corr_std, query_units, ife_list)
    # Get the center data for calculating discrepancy
    center_data = ccs.get_center(corr_complete)
    # Calculate discrepancy using the geometric method
    discrepancy_data = ui.calculate_relative_disc(ife_list, center_data, len(core_units), len(query_units))
    # Order the instances by similarity
    ifes_ordered, coord_ordered = ui.get_ordering(ife_list, discrepancy_data, coord_data)
    # Get discrepancy statistics and build the heatmap data for display
    max_disc, percentile, heatmap_data = ui.build_heatmap_data(discrepancy_data, ifes_ordered)
    # Get all the annotation from the definition file
    trna_occupancy, functional_state, factors_bound, antibiotic_bound, reported_intersubunit, \
    calculated_intersubunit, reported_head, calculated_head = ui.get_annotation(ifes_ordered)
    # Reorder the pairwise annotation based on the new ordering
    pw_info_ordered = ui.reorder_pw(ifes_ordered, pw_info)
    return render_template("correspondence_display.html", query_nts=query_units,
                           coord=coord_ordered, ifes=ifes_ordered, maxDisc=max_disc, p2=percentile,
                           data=heatmap_data, trna_occupancy=trna_occupancy, functional_state=functional_state,
                           factors_bound=factors_bound, reported_rotation=reported_intersubunit,
                           calculated_rotation=calculated_intersubunit, reported_head=reported_head,
                           calculated_head=calculated_head, antibiotic_bound=antibiotic_bound,
                           pw_info=pw_info_ordered, pw_list=pw_sorted)
"""


