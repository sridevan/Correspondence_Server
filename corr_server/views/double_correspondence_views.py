import flask
from flask import render_template
import json
import services.correspondence_service as cs
import services.query_service as qs
import services.equivalence_class_service as em
import services.rotation_service as rs
import services.center_service as ccs
import services.pairwise_int_service as ps
import infrastructure.process_input as pi
import infrastructure.utility as ui
from definitions import members_SSU, members_LSU, ribosome_subunits

blueprint = flask.Blueprint('double', __name__, template_folder='templates')


@blueprint.route('/double/relative/<selection>')
def index(selection):
    query_list = pi.input_type(selection)
    query_type = pi.check_query(query_list)
    core_units, query_units = qs.get_query_units_double(query_type, query_list)
    core_complete = cs.get_correspondence_core(core_units, members_LSU)
    core_complete_dict = ui.create_dict(core_complete)
    corr_complete, corr_std = cs.get_correspondence(query_units, members_SSU)
    corr_complete_dict = ui.create_dict(corr_complete)
    complete_units = ui.merge_double(ribosome_subunits, core_complete_dict, corr_complete_dict)
    lsu_list, ssu_list, coord_data = ui.build_coord_double(complete_units, len(core_units))
    # Get the pairwise annotation for the instances in the EC
    pw_info, pw_sorted = ps.get_pairwise_annotation(corr_complete, query_units, ssu_list)
    # Get the center data for calculating discrepancy
    center_data = ccs.get_center(complete_units)
    # Calculate discrepancy using the geometric method
    discrepancy_data = ui.calculate_relative_disc(lsu_list, center_data, len(core_units), len(query_units))
    # Order the instances by similarity
    ifes_ordered, coord_ordered = ui.get_ordering(lsu_list, discrepancy_data, coord_data)
    # Get discrepancy statistics and build the heatmap data for display
    max_disc, percentile, heatmap_data = ui.build_heatmap_data(discrepancy_data, ifes_ordered)
    # Get all the annotation from the definition file
    trna_occupancy, functional_state, factors_bound, antibiotic_bound, reported_intersubunit, \
    calculated_intersubunit, reported_head, calculated_head = ui.get_annotation_double(ifes_ordered)
    # Reorder the pairwise annotation based on the new ordering
    pw_info_ordered = ui.reorder_pw_double(ifes_ordered, pw_info)
    return render_template("correspondence_display.html", query_nts=query_units,
                           coord=coord_ordered, ifes=ifes_ordered, maxDisc=max_disc, p2=percentile,
                           data=heatmap_data, trna_occupancy=trna_occupancy, functional_state=functional_state,
                           factors_bound=factors_bound, reported_rotation=reported_intersubunit,
                           calculated_rotation=calculated_intersubunit, reported_head=reported_head,
                           calculated_head=calculated_head, antibiotic_bound=antibiotic_bound,
                           pw_info=pw_info_ordered, pw_list=pw_sorted)

    '''
    # Reorder the pairwise annotation based on the new ordering
    pw_info_ordered = ui.reorder_pw(ifes_ordered, pw_info)
    return render_template("correspondence_display.html", query_nts=query_units,
                           coord=coord_ordered, ifes=ifes_ordered, maxDisc=max_disc, p2=percentile,
                           data=heatmap_data, trna_occupancy=trna_occupancy, functional_state=functional_state,
                           factors_bound=factors_bound, reported_rotation=reported_intersubunit,
                           calculated_rotation=calculated_intersubunit, reported_head=reported_head,
                           calculated_head=calculated_head, antibiotic_bound=antibiotic_bound,
                           pw_info=pw_info_ordered, pw_list=pw_sorted)
    '''

    '''
    # Get the pairwise annotation for the instances in the EC
    pw_info, pw_sorted = ps.get_pairwise_annotation(corr_complete, query_units, ife_list)
    # Get the center data for calculating discrepancy
    center_data = ccs.get_center(complete_units)
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
    '''

    '''
    corr_complete_large, corr_std_large = cs.get_correspondence(query_units, members_SSU)
    complete_units = ui.merge_double(core_complete_large, corr_complete_large)
    ife_list, coord_data = ui.build_coord(complete_units)
    # Get the pairwise annotation for the instances in the EC
    pw_info, pw_sorted = ps.get_pairwise_annotation(corr_std_large, query_units, ife_list)
    # Get the center data for calculating discrepancy
    center_data = ccs.get_center(complete_units)
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
    '''
