
# common front end imports
from spinn_front_end_common.interface.spinnaker_main_interface import \
    SpinnakerMainInterface

# graph front end imports
from spinnaker_graph_front_end.utilities.xml_interface import XMLInterface
from spinnaker_graph_front_end.utilities.conf import config

# general imports
import logging


logger = logging.getLogger(__name__)


class SpiNNaker(SpinnakerMainInterface):

    def __init__(
            self, executable_finder, host_name=None, graph_label=None,
            database_socket_addresses=None, dsg_algorithm=None,
            n_chips_required=None):

        # dsg algorithm store for user defined algorithms
        self._user_dsg_algorithm = dsg_algorithm

        # create xml path for where to locate GFE related functions when
        # using auto pause and resume
        extra_xml_path = list()

        extra_mapping_inputs = dict()
        extra_mapping_inputs["CreateAtomToEventIdMapping"] = config.getboolean(
            "Database", "create_routing_info_to_atom_id_mapping")

        SpinnakerMainInterface.__init__(
            self, config, graph_label=graph_label,
            executable_finder=executable_finder,
            database_socket_addresses=database_socket_addresses,
            extra_algorithm_xml_paths=extra_xml_path,
            extra_mapping_inputs=extra_mapping_inputs,
            n_chips_required=n_chips_required)

        # set up machine targeted data
        self._machine_time_step = config.getint("Machine", "machineTimeStep")
        self.set_up_machine_specifics(host_name)

        self._time_scale_factor = 1
        logger.info("Setting time scale factor to {}."
                    .format(self._time_scale_factor))

        logger.info("Setting appID to %d." % self._app_id)

        # get the machine time step
        logger.info("Setting machine time step to {} micro-seconds."
                    .format(self._machine_time_step))

    def read_partitionable_graph_xml_file(self, file_path):
        """

        :param file_path:
        :return:
        """
        xml_interface = XMLInterface(file_path)
        self._partitionable_graph = xml_interface.read_in_file()

    def read_partitioned_graph_xml_file(self, file_path):
        """

        :param file_path:
        :return:
        """
        xml_interface = XMLInterface(file_path)
        self._partitioned_graph = xml_interface.read_in_file()

    def get_machine_dimensions(self):
        """ Get the machine dimensions
        :return:
        """
        machine = self.machine

        return {'x': machine.max_chip_x, 'y': machine.max_chip_y}

    @staticmethod
    @property
    def is_allocated_machine():
        return (
            config.get("Machine", "spalloc_server") != "None" or
            config.get("Machine", "remote_spinnaker_url") != "None"
        )

    def add_socket_address(self, socket_address):
        """ Add a socket address to the list to be checked by the\
            notification protocol

        :param socket_address: the socket address
        :type socket_address:
        :return:
        """
        self._add_socket_address(socket_address)

    def run(self, run_time):

        # set up the correct dsg algorithm
        if self._user_dsg_algorithm is None:
            if len(self._partitioned_graph.subvertices) != 0:
                self.dsg_algorithm = \
                    "FrontEndCommonPartitionedGraphDataSpecificationWriter"
            elif len(self._partitionable_graph.vertices) != 0:
                self.dsg_algorithm = \
                    "FrontEndCommonPartitionableGraphDataSpecificationWriter"
        else:
            self.dsg_algorithm = self._user_dsg_algorithm

        # run normal procedure
        SpinnakerMainInterface.run(self, run_time)

    def __repr__(self):
        return "SpiNNaker Graph Front End object for machine {}"\
            .format(self._hostname)
