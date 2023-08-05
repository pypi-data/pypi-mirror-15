from spinn_front_end_common.utilities import exceptions
from spinn_front_end_common.interface.buffer_management.buffer_models\
    .abstract_receive_buffers_to_host import AbstractReceiveBuffersToHost
from spinn_machine.utilities.progress_bar import ProgressBar


class FrontEndCommonBufferExtractor(object):
    """ Extracts data in between runs
    """

    def __call__(
            self, partitioned_graph, placements, buffer_manager, ran_token):

        if not ran_token:
            raise exceptions.ConfigurationException(
                "The ran token has not been set")

        # Count the regions to be read
        n_regions_to_read = 0
        for vertex in partitioned_graph.subvertices:
            if isinstance(vertex, AbstractReceiveBuffersToHost):
                n_regions_to_read += len(vertex.get_buffered_regions())

        progress_bar = ProgressBar(
            n_regions_to_read, "Extracting buffers from the last run")

        # Read back the regions
        for vertex in partitioned_graph.subvertices:
            if isinstance(vertex, AbstractReceiveBuffersToHost):
                placement = placements.get_placement_of_subvertex(vertex)
                state_region = vertex.get_buffered_state_region()
                for region in vertex.get_buffered_regions():
                    buffer_manager.get_data_for_vertex(
                        placement, region, state_region)
                    progress_bar.update()
        progress_bar.end()
