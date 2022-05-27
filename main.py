"""Project element of the Geiger random number generator. Code author: Arkadiusz Łęga"""
import datetime
import random
import time


class GeigerRandomNumberGenerator:
    """
    A class that intercepts the moments when radiation is extracted from a Geiger sensor.
    As a result of the radiation detection times taken and the permutations performed,
    a list of bits is generated. The sequence of bits can be used to generate numbers.
    """
    NUMBER_OF_TICKS = 3

    def __init__(self, number_of_bits=8):
        self.__number_of_bits = number_of_bits
        self.__random_bits = []
        self.__pulses_times = []

    @property
    def get_random_bits_number(self):
        """
        :return: Number of collected bits.
        """
        return len(self.__random_bits)

    @property
    def get_number_of_bits(self):
        return self.__number_of_bits

    def set_pulse_time(self):
        """
        Adds a new pulse time to the list, and then adds the bit to the list of bits
        in the string of numbers returned as a string of random numbers.
        :return: None
        """
        self.__remove_first_pulse_time()
        self.__pulses_times.append(datetime.datetime.now())

        self.__add_bit_to_list()

    def __remove_first_pulse_time(self):
        """
        Removes the first pulse reading time from the list.
        :return: None
        """
        if len(self.__pulses_times) == self.NUMBER_OF_TICKS:
            self.__pulses_times.pop(0)

    def __add_bit_to_list(self):
        """
        Adds a bit to the random bit string list as long as the bit limit is not exceeded.
        :return: None
        """
        self.__remove_bits_if_size_is_max()
        self.__append_bits_to_list()

    def __remove_bits_if_size_is_max(self):
        """
        Clears the bit list when the number of bits equals the reached limit.
        :return: None
        """
        if len(self.__random_bits) == self.__number_of_bits:
            self.__random_bits.clear()

    def __append_bits_to_list(self):
        """
        Adds a bit when the number of required ticks is reached.
        :return: None
        """
        if len(self.__pulses_times) == self.NUMBER_OF_TICKS:
            first_time = self.__pulses_times[1] - self.__pulses_times[0]
            second_time = self.__pulses_times[2] - self.__pulses_times[1]

            self.__random_bits.append((0x00, 0x01)[first_time > second_time])

    def get_int_number(self):
        """
        Convert bits from random bits to integer.
        :return: A decimal number calculated from the bits of the random bit list.
        """
        if len(self.__random_bits) > 0:
            all_random_bits = ''

            for bit in self.__random_bits:
                all_random_bits += str(bit)

            return int(all_random_bits, 2)

        return None


if __name__ == '__main__':
    geiger = GeigerRandomNumberGenerator(128)
    number = 1024
    counter = 0

    while counter < number:
        val = random.uniform(0, 0.00009)
        time.sleep(val)
        geiger.set_pulse_time()
        if geiger.get_random_bits_number == geiger.get_number_of_bits:
            print((str(geiger.get_int_number())))
        counter += 1
