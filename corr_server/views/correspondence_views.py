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


@blueprint.route('/correspondence/<method>/<selection>')
# @response(template_file='packages/details.html')
def correspondence_geometric(method, selection):
    if method == 'geometric':
        query_list = pi.input_type(selection)
        query_type = pi.check_query(query_list)
        query_ife, query_units = qs.get_query_units(query_type, query_list)
        rejected_members, ec_members = em.get_ec_members(query_ife)
        corr_complete, corr_std = cs.get_correspondence(query_units, ec_members)
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
                               coord=coord_ordered, ifes=ifes_ordered, maxDisc=max_disc, p2=percentile,
                               data=heatmap_data, trna_occupancy=trna_occupancy, functional_state=functional_state,
                               factors_bound=factors_bound, reported_rotation=reported_intersubunit,
                               calculated_rotation=calculated_intersubunit, reported_head=reported_head,
                               calculated_head=calculated_head, antibiotic_bound=antibiotic_bound,
                               pw_info=pw_info_ordered, pw_list=pw_sorted)
    else:
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
@blueprint.route('/correspondence_test/<selection>', methods=["POST"])
def correspondence_test(selection):
    if request.method == 'POST':
        return selection
"""
