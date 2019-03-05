import pytest
import sys
import sqlite3
sys.path.append("..")
import talonQ as talon
from helper_fns import *
@pytest.mark.integration

class TestIdentifyFSM(object):

    def test_FSM_perfect(self):
        """ Example where the transcript is a perfect full splice match.
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        edge_dict = talon.make_edge_dict(cursor)
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)        
        transcript_dict = talon.make_transcript_dict(cursor, build)
        gene_starts, gene_ends = talon.make_gene_start_and_end_dict(cursor)

        edge_IDs = (1, 2, 3, 4, 5)
        vertex_IDs = (1, 2, 3, 4, 5, 6)
        v_novelty = (0, 0, 0, 0, 0, 0)

        gene_ID, transcript_ID, novelty = talon.process_FSM_or_ISM(edge_IDs, vertex_IDs,
                                                            transcript_dict, gene_starts, gene_ends,
                                                            run_info)

        correct_gene_ID = fetch_correct_ID("TG1", "gene", cursor) 
        correct_transcript_ID = fetch_correct_ID("TG1-001", "transcript", cursor)
        assert gene_ID == correct_gene_ID
        assert transcript_ID == correct_transcript_ID
        assert novelty == []
        conn.close()

    def test_FSM_end_diff(self):
        """ Example where the transcript is an FSM but has a difference on
            the ends large enough to be novel.
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        edge_dict = talon.make_edge_dict(cursor)
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)
        transcript_dict = talon.make_transcript_dict(cursor, build)
        gene_starts, gene_ends = talon.make_gene_start_and_end_dict(cursor)

        edge_IDs = (1, 2, 3, 4, 500) # Last edge is novel
        vertex_IDs = (1, 2, 3, 4, 5, 500) # Last vertex is novel
        v_novelty = (0, 0, 0, 0, 0, 1)
   
        gene_ID, transcript_ID, novelty = talon.process_FSM_or_ISM(edge_IDs, vertex_IDs,
                                                            transcript_dict, gene_starts, gene_ends,
                                                            run_info)

        correct_gene_ID = fetch_correct_ID("TG1", "gene", cursor)
        correct_transcript_ID = fetch_correct_ID("TG1-001", "transcript", cursor)
        assert gene_ID == correct_gene_ID
        conn.close()

    def test_no_match(self):
        """ Example with no FSM or ISM match """

        conn, cursor = get_db_cursor()
        build = "toy_build"
        edge_dict = talon.make_edge_dict(cursor)
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build)
        transcript_dict = talon.make_transcript_dict(cursor, build)
        gene_starts, gene_ends = talon.make_gene_start_and_end_dict(cursor)

        edge_IDs = (1, 200, 3) 
        vertex_IDs = (1, 2, 5, 6) 
        v_novelty = (0, 0, 0, 0)

        gene_ID, transcript_ID, novelty = talon.process_FSM_or_ISM(edge_IDs, vertex_IDs,
                                                            transcript_dict, gene_starts, gene_ends,
                                                            run_info)
        assert gene_ID == transcript_ID == None 
        conn.close()       

