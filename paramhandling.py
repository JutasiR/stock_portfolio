#!/usr/bin/env python
# coding: utf-8

"""
@author: JutasiR
"""

import configparser

class ParamHandler():
    """
    'ParamHandler' class is created to pass on input parameter values and theirs descriptions to the 'mainmodule'.
    At initialization, the parameters are read from 'input_parameters.ini'.
    """
    def __init__(self):

        self.__parameters, self.__descriptions = self.__read_conf_file()
        
        params = []
        default_vals = []
        
        for param, value in self.__parameters.items():
            params.append(param)
            default_vals.append(value)
            
        self.nr_of_years = default_vals[0]
        self.stock_nr = default_vals[1]
        self.nr_of_modeled_portf = default_vals[2]
        self.nr_of_weights_per_portf = default_vals[3]
   
    def __read_conf_file(self):
        config = configparser.ConfigParser()

        try:
            config.read('input_parameters.ini')
        except FileNotFoundError:
            raise Exception("Missing file named 'input_parameters.ini'")

        params = config["Parameters"]
        send_inputs = {}
        send_desc = {}

        for key1, value1 in params.items():
            try:
                send_inputs[key1] = int(value1)
            except:
                raise Exception("All parameters must be a whole number")

        description = config["Description of Parameters"]
        for key2, value2 in description.items():
            send_desc[key2] = value2  

        return send_inputs, send_desc    

    def get_parameter_description(self):
        print("Parameter names and explications:")
        for key, exp in self.__descriptions.items():
            print(f"- {key}: {exp.capitalize()}")
        print("\nDefault values:")
        for key, value in self.__parameters.items():
            print(f"- {key}: {value}")

