
# spinn_machine imports
from spinn_machine.exceptions import SpinnMachineAlreadyExistsException

# general imports
from collections import OrderedDict


class Machine(object):
    """ A Representation of a Machine with a number of Chips.  Machine is also\
        iterable, providing ((x, y), chip) where:

            * x is the x-coordinate of a chip
            * y is the y-coordinate of a chip
            * chip is the chip with the given x, y coordinates
    """

    # current opinions is that the Ethernet connected chip can handle 10
    # UDP packets per millisecond
    MAX_BANDWIDTH_PER_ETHERNET_CONNECTED_CHIP = 10 * 256

    def __init__(self, chips):
        """
        :param chips: An iterable of chips in the machine
        :type chips: iterable of :py:class:`spinn_machine.chip.Chip`
        :raise spinn_machine.exceptions.SpinnMachineAlreadyExistsException: If\
                    any two chips have the same x and y coordinates
        """

        # The maximum chip x coordinate
        self._max_chip_x = 0

        # The maximum chip y coordinate
        self._max_chip_y = 0

        # The list of chips with Ethernet connections
        self._ethernet_connected_chips = list()

        # The dictionary of chips via their nearest Ethernet connected chip
        self._chips_by_local_ethernet = dict()

        # The dictionary of spinnaker links by "id" (int)
        self._spinnaker_links = dict()

        # The dictionary of chips
        self._chips = OrderedDict()
        self.add_chips(chips)

    def add_chip(self, chip):
        """ Add a chip to the machine

        :param chip: The chip to add to the machine
        :type chip: :py:class:`spinn_machine.chip.Chip`
        :return: Nothing is returned
        :rtype: None
        :raise spinn_machine.exceptions.SpinnMachineAlreadyExistsException: If\
                    a chip with the same x and y coordinates already exists
        """
        chip_id = (chip.x, chip.y)
        if chip_id in self._chips:
            raise SpinnMachineAlreadyExistsException("chip", "{}, {}"
                                                     .format(chip.x, chip.y))

        self._chips[chip_id] = chip

        if chip.x > self._max_chip_x:
            self._max_chip_x = chip.x
        if chip.y > self._max_chip_y:
            self._max_chip_y = chip.y

        if chip.ip_address is not None:
            self._ethernet_connected_chips.append(chip)

        chip_id = (chip.nearest_ethernet_x, chip.nearest_ethernet_y)
        if chip_id not in self._chips_by_local_ethernet:
            self._chips_by_local_ethernet[chip_id] = list()
        self._chips_by_local_ethernet[chip_id].append(chip)

    def get_chips_via_local_ethernet(self, local_ethernet_x, local_ethernet_y):
        """
        returns a list of chips which have the nearest Ethernet chip of x and y
        :param local_ethernet_x: the Ethernet chip x coord
        :param local_ethernet_y: the Ethernet chip y coord
        :return: list of chips
        """
        chip_id = (local_ethernet_x, local_ethernet_y)
        if chip_id not in self._chips_by_local_ethernet:
            return []
        else:
            return self._chips_by_local_ethernet[chip_id]

    def add_chips(self, chips):
        """ Add some chips to the machine

        :param chips: an iterable of chips
        :type chips: iterable of :py:class:`spinn_machine.chip.Chip`
        :return: Nothing is returned
        :rtype: None
        :raise spinn_machine.exceptions.SpinnMachineAlreadyExistsException: If\
                    a chip with the same x and y coordinates as one being\
                    added already exists
        """
        for next_chip in chips:
            self.add_chip(next_chip)

    @property
    def chips(self):
        """ An iterable of chips in the machine

        :return: An iterable of chips
        :rtype: iterable of :py:class:`spinn_machine.chip.Chip`
        :raise None: does not raise any known exceptions
        """
        return self._chips.itervalues()

    def __iter__(self):
        """ Get an iterable of the chip coordinates and chips

        :return: An iterable of tuples of ((x, y), chip) where:
                    * (x, y) is a tuple where:
                        * x is the x-coordinate of a chip
                        * y is the y-coordinate of a chip
                    * chip is a chip
        :rtype: iterable of ((int, int), :py:class:`spinn_machine.chip.Chip`)
        :raise None: does not raise any known exceptions
        """
        return self._chips.iteritems()

    def get_chip_at(self, x, y):
        """ Get the chip at a specific (x, y) location.\
            Also implemented as __getitem__((x, y))

        :param x: the x-coordinate of the requested chip
        :type x: int
        :param y: the y-coordinate of the requested chip
        :type y: int
        :return: the chip at the specified location, or None if no such chip
        :rtype: :py:class:`spinn_machine.chip.Chip`
        :raise None: does not raise any known exceptions
        """
        chip_id = (x, y)
        if chip_id in self._chips:
            return self._chips[chip_id]
        return None

    def __getitem__(self, x_y_tuple):
        """ Get the chip at a specific (x, y) location

        :param x_y_tuple: A tuple of (x, y) where:
                    * x is the x-coordinate of the chip to retrieve
                    * y is the y-coordinate of the chip to retrieve
        :type x_y_tuple: (int, int)
        :return: the chip at the specified location, or None if no such chip
        :rtype: :py:class:`spinn_machine.chip.Chip`
        :raise None: does not raise any known exceptions
        """
        x, y = x_y_tuple
        return self.get_chip_at(x, y)

    def is_chip_at(self, x, y):
        """ Determine if a chip exists at the given coordinates.\
            Also implemented as __contains__((x, y))

        :param x: x location of the chip to test for existence
        :type x: int
        :param y: y location of the chip to test for existence
        :type y: int
        :return: True if the chip exists, False otherwise
        :rtype: bool
        :raise None: does not raise any known exceptions
        """
        chip_id = (x, y)
        return chip_id in self._chips

    def __contains__(self, x_y_tuple):
        """ Determine if a chip exists at the given coordinates

        :param x_y_tuple: A tuple of (x, y) where:
                    * x is the x-coordinate of the chip to retrieve
                    * y is the y-coordinate of the chip to retrieve
        :type x_y_tuple: (int, int)
        :return: True if the chip exists, False otherwise
        :rtype: bool
        :raise None: does not raise any known exceptions
        """
        x, y = x_y_tuple
        return self.is_chip_at(x, y)

    @property
    def max_chip_x(self):
        """ The maximum x-coordinate of any chip in the board

        :return: The maximum x-coordinate
        :rtype: int
        """
        return self._max_chip_x

    @property
    def max_chip_y(self):
        """ The maximum y-coordinate of any chip in the board

        :return: The maximum y-coordinate
        :rtype: int
        """
        return self._max_chip_y

    @property
    def n_chips(self):
        """

        :return:
        """
        return len(self._chips)

    @property
    def ethernet_connected_chips(self):
        """ The chips in the machine that have an Ethernet connection

        :return: An iterable of chips
        :rtype: iterable of :py:class:`spinn_machine.chip.Chip`
        """
        return self._ethernet_connected_chips

    def add_spinnaker_link(self, spinnaker_link):
        """ Add a spinnaker link to the machine
        """
        if spinnaker_link.spinnaker_link_id in self._spinnaker_links:
            raise SpinnMachineAlreadyExistsException(
                "spinnaker_link", spinnaker_link.spinnaker_link_id)
        self._spinnaker_links[
            spinnaker_link.spinnaker_link_id] = spinnaker_link

    @property
    def spinnaker_links(self):
        """ The set of spinnaker links in the machine

        :return: An iterable of spinnaker links
        :rtype: iterable of\
            :py:class:`spinn_machine.spinnaker_link_data.SpinnakerLinkData`
        """
        return self._spinnaker_links.values()

    def get_spinnaker_link_with_id(self, spinnaker_link_id):
        """ Get a spinnaker link with a given id

        :param spinnaker_link_id: The id of the link
        :type spinnaker_link_id: int
        :rtype: :py:class:`spinn_machine.spinnaker_link_data.SpinnakerLinkData`
        """
        return self._spinnaker_links[spinnaker_link_id]

    def __str__(self):
        return "[Machine: max_x={}, max_y={}, chips={}]".format(
            self._max_chip_x, self._max_chip_y, self._chips.values())

    def __repr__(self):
        return self.__str__()

    def get_cores_and_link_count(self):
        """ Get the number of cores and links from the machine

        :return: tuple of (n_cores, n_links)
        """
        cores = 0
        total_links = dict()
        for chip_key in self._chips:
            chip = self._chips[chip_key]
            cores += len(list(chip.processors))
            for link in chip.router.links:
                key1 = (link.source_x, link.source_y, link.source_link_id)
                key2 = (link.destination_x, link.destination_y,
                        link.multicast_default_from)
                if key1 not in total_links and key2 not in total_links:
                    total_links[key1] = key1
        links = len(total_links.keys())
        return cores, links

    def cores_and_link_output_string(self):
        """ Get a string detailing the number of cores and links

        :rtype: str
        """
        cores, links = self.get_cores_and_link_count()
        return "{} cores and {} links".format(cores, links)
