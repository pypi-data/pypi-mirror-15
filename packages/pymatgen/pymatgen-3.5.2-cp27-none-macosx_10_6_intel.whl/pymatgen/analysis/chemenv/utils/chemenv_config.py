# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

from __future__ import division, unicode_literals

"""
This module contains the classes for configuration of the chemenv package.
"""

__author__ = "David Waroquiers"
__copyright__ = "Copyright 2012, The Materials Project"
__credits__ = "Geoffroy Hautier"
__version__ = "2.0"
__maintainer__ = "David Waroquiers"
__email__ = "david.waroquiers@gmail.com"
__date__ = "Feb 20, 2016"


from pymatgen.analysis.chemenv.utils.chemenv_errors import ChemenvError
from pymatgen.analysis.chemenv.utils.scripts_utils import strategies_class_lookup
from os.path import expanduser, exists
from os import makedirs
import json


class ChemEnvConfig():
    """
    Class used to store the configuration of the chemenv package :
     - Materials project access
     - ICSD database access
     - Default options (strategies, ...)
    """
    DEFAULT_PACKAGE_OPTIONS = {'default_strategy': {'strategy': 'SimplestChemenvStrategy',
                                                    'strategy_options': {'distance_cutoff': strategies_class_lookup['SimplestChemenvStrategy'].DEFAULT_DISTANCE_CUTOFF,
                                                                         'angle_cutoff': strategies_class_lookup['SimplestChemenvStrategy'].DEFAULT_ANGLE_CUTOFF,
                                                                         'additional_condition': strategies_class_lookup['SimplestChemenvStrategy'].DEFAULT_ADDITIONAL_CONDITION,
                                                                         'continuous_symmetry_measure_cutoff': strategies_class_lookup['SimplestChemenvStrategy'].DEFAULT_CONTINUOUS_SYMMETRY_MEASURE_CUTOFF}},
                               }

    def __init__(self, materials_project_configuration=None, package_options=None):
        self.materials_project_configuration = materials_project_configuration
        if package_options is None:
            self.package_options = self.DEFAULT_PACKAGE_OPTIONS
        else:
            self.package_options = package_options

    def setup(self):
        while True:
            print('\n=> Configuration of the ChemEnv package <=')
            print('Current configuration :')
            if self.has_materials_project_access:
                print(' - Access to materials project is configured (add test ?)')
            else:
                print(' - No access to materials project')
            print(' - Package options :')
            for key, val in self.package_options.items():
                print('     {}   :   {}'.format(str(key), str(val)))
            print('\nChoose in the following :')
            print(' <1> + <ENTER> : setup of the access to the materials project database')
            print(' <2> + <ENTER> : configuration of the package options (strategy, ...)')
            print(' <q> + <ENTER> : quit without saving configuration')
            test = raw_input(' <S> + <ENTER> : save configuration and quit\n ... ')
            if test == '1':
                self.setup_materials_project_configuration()
            elif test == '2':
                self.setup_package_options()
            elif test == 'q':
                break
            elif test == 'S':
                config_file = self.save()
                break
            else:
                print(' ... wrong key, try again ...')
            print('')
        if test == 'S':
            print('Configuration has been saved to file "{}"'.format(config_file))

    def setup_materials_project_configuration(self):
        api_key = raw_input('\nEnter your Materials Project API key : ')
        self.materials_project_configuration = {'api_key': api_key}

    @property
    def has_materials_project_access(self):
        return self.materials_project_configuration is not None

    def setup_package_options(self):
        self.package_options = self.DEFAULT_PACKAGE_OPTIONS
        print('Choose between the following strategies : ')
        strategies = list(strategies_class_lookup.keys())
        for istrategy, strategy in enumerate(strategies):
            print(' <{}> : {}'.format(str(istrategy + 1), strategy))
        test = raw_input(' ... ')
        self.package_options['default_strategy'] = {'strategy': strategies[int(test) - 1], 'strategy_options': {}}
        strategy_class = strategies_class_lookup[strategies[int(test) - 1]]
        if len(strategy_class.STRATEGY_OPTIONS) > 0:
            for option, option_dict in strategy_class.STRATEGY_OPTIONS.items():
                while True:
                    print('  => Enter value for option "{}" '
                          '(<ENTER> for default = {})\n'.format(option,
                                                                str(option_dict['default'])))
                    print('     Valid options are :\n')
                    print('       {}'.format(option_dict['type'].allowed_values))
                    test = raw_input('     Your choice : ')
                    if test == '':
                        self.package_options['default_strategy']['strategy_options'][option] = option_dict['type'](strategy_class.STRATEGY_OPTIONS[option]['default'])
                        break
                    try:
                        self.package_options['default_strategy']['strategy_options'][option] = option_dict['type'](test)
                        break
                    except ValueError:
                        print('Wrong input for option {}'.format(option))

    def package_options_description(self):
        out = 'Package options :\n'
        out += ' - Default strategy is "{}" :\n'.format(self.package_options['default_strategy']['strategy'])
        strategy_class = strategies_class_lookup[self.package_options['default_strategy']['strategy']]
        out += '{}\n'.format(strategy_class.STRATEGY_DESCRIPTION)
        out += '   with options :\n'
        for option, option_dict in strategy_class.STRATEGY_OPTIONS.items():
            out += '     - {} : {}\n'.format(option,
                                             self.package_options['default_strategy']['strategy_options'][option])
        return out

    def save(self, root_dir=None):
        if root_dir is None:
            home = expanduser("~")
            root_dir = '{}/.chemenv'.format(home)
        if not exists(root_dir):
            makedirs(root_dir)
        config_dict = {'materials_project_configuration': self.materials_project_configuration,
                       'package_options': self.package_options}
        config_file = '{}/config.json'.format(root_dir)
        if exists(config_file):
            test = raw_input('Overwrite existing configuration ? (<Y> + <ENTER> to confirm)')
            if test != 'Y':
                print('Configuration not saved')
                return config_file
        f = open(config_file, 'w')
        json.dump(config_dict, f)
        f.close()
        print('Configuration saved')
        return config_file

    @classmethod
    def auto_load(cls, root_dir=None):
        if root_dir is None:
            home = expanduser("~")
            root_dir = '{}/.chemenv'.format(home)
        config_file = '{}/config.json'.format(root_dir)
        try:
            f = open(config_file, 'r')
            config_dict = json.load(f)
            f.close()
            return ChemEnvConfig(materials_project_configuration=config_dict['materials_project_configuration'],
                                 package_options=config_dict['package_options'])
        except IOError:
            print('Unable to load configuration from file "{}" ...'.format(config_file))
            print(' ... loading default configuration')
            return ChemEnvConfig()

    @property
    def materials_project_api_key(self):
        if self.materials_project_configuration is None:
            raise ChemenvError('ChemEnvConfig', 'materials_project_api_key', 'No api_key saved')
        return self.materials_project_configuration['api_key']