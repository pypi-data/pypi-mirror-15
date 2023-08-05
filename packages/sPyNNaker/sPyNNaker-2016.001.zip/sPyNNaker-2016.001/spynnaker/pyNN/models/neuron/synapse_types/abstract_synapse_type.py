from six import add_metaclass
from abc import ABCMeta
from abc import abstractmethod
import math


@add_metaclass(ABCMeta)
class AbstractSynapseType(object):
    """ Represents the synapse types supported
    """

    @abstractmethod
    def get_n_synapse_types(self):
        """ Get the number of synapse types supported

        :return: The number of synapse types supported
        :rtype: int
        """

    @abstractmethod
    def get_synapse_id_by_target(self, target):
        """ Get the id of a synapse given the name

        :param name: The name of the synapse
        :type name: str
        :return: The id of the synapse
        :rtype: int
        """

    @abstractmethod
    def get_synapse_targets(self):
        """ Get the target names of the synapse type

        :return: an array of strings
        :rtype: array of str
        """

    @abstractmethod
    def get_n_synapse_type_parameters(self):
        """ Get the number of synapse type parameters

        :return: the number of parameters
        :rtype: int
        """

    @abstractmethod
    def get_synapse_type_parameters(self):
        """ Get the synapse type parameters

        :return: The parameters
        :rtype: array of\
                :py:class:`spynnaker.pyNN.models.neural_properties.neural_parameter.NeuronParameter`
        """

    @abstractmethod
    def get_n_cpu_cycles_per_neuron(self):
        """ Get the total number of CPU cycles executed by\
            synapse_types_shape_input, synapse_types_add_neuron_input,\
            synapse_types_get_excitatory_input and \
            synapse_types_get_inhibitory_input

        :return: The number of CPU cycles
        :rtype: int
        """

    def get_n_synapse_type_bits(self):
        """ Get the number of bits required to represent the synapse types

        :return: the number of bits
        :rtype: int
        """
        return int(math.ceil(math.log(self.get_n_synapse_types(), 2)))

    def get_sdram_usage_per_neuron_in_bytes(self):
        """ Get the SDRAM usage of the synapse type per neuron in bytes

        :return: the number of bytes
        :rtype: int
        """
        return self.get_n_synapse_type_parameters() * 4

    def get_dtcm_usage_per_neuron_in_bytes(self):
        """ Get the DTCM usage of the synapse type per neuron in bytes

        :return: the number of bytes
        :rtype: int
        """
        return self.get_n_synapse_type_parameters() * 4
