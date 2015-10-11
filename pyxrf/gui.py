# ######################################################################
# Copyright (c) 2014, Brookhaven Science Associates, Brookhaven        #
# National Laboratory. All rights reserved.                            #
#                                                                      #
# Redistribution and use in source and binary forms, with or without   #
# modification, are permitted provided that the following conditions   #
# are met:                                                             #
#                                                                      #
# * Redistributions of source code must retain the above copyright     #
#   notice, this list of conditions and the following disclaimer.      #
#                                                                      #
# * Redistributions in binary form must reproduce the above copyright  #
#   notice this list of conditions and the following disclaimer in     #
#   the documentation and/or other materials provided with the         #
#   distribution.                                                      #
#                                                                      #
# * Neither the name of the Brookhaven Science Associates, Brookhaven  #
#   National Laboratory nor the names of its contributors may be used  #
#   to endorse or promote products derived from this software without  #
#   specific prior written permission.                                 #
#                                                                      #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS  #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT    #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS    #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE       #
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,           #
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES   #
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR   #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)   #
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,  #
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OTHERWISE) ARISING   #
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
# POSSIBILITY OF SUCH DAMAGE.                                          #
########################################################################
from __future__ import absolute_import
__author__ = 'Li Li'
import enaml
from enaml.qt.qt_application import QtApplication

import os
import numpy as np
import logging

from .model.fileio import FileIOModel
from .model.lineplot import LinePlotModel #, SettingModel
from .model.guessparam import GuessParamModel
from .model.draw_image import DrawImageAdvanced
from .model.draw_image_rgb import DrawImageRGB
from .model.fit_spectrum import Fit1D
from .model.setting import SettingModel
from .model.param_data import param_data
import json

with enaml.imports():
    from .view.main_window import XRFGui


def get_defaults():

    sub_folder = 'data_analysis'  # + '/xspress3'
    working_directory = os.path.join(os.path.expanduser('~'),
                                     sub_folder)
    output_directory = working_directory

    # grab the default parameter file
    # current_dir = os.path.dirname(os.path.realpath(__file__))
    # temp = current_dir.split('/')[:-1]
    # temp.append('configs')
    # param_dir = '/'.join(temp)
    # default_parameter_file = os.path.join(
    #     param_dir, 'xrf_parameter.json')
    # with open(default_parameter_file, 'r') as json_data:
    #     default_parameters = json.load(json_data)
    default_parameters = param_data
    defaults = {'working_directory': working_directory,
                #'output_directory': output_directory,
                'default_parameters': default_parameters}
    return defaults


def run():
    LOG_F = 'log_example.out'
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO,
                        #filename=LOG_F,
                        filemode='w')

    app = QtApplication()
    defaults = get_defaults()

    io_model = FileIOModel(**defaults)
    param_model = GuessParamModel(**defaults)
    plot_model = LinePlotModel()
    fit_model = Fit1D(**defaults)
    setting_model = SettingModel(**defaults)
    img_model_adv = DrawImageAdvanced()
    img_model_rgb = DrawImageRGB()

    # send working directory changes to different models
    io_model.observe('working_directory', fit_model.result_folder_changed)
    io_model.observe('selected_file_name', fit_model.data_title_update)
    io_model.observe('selected_file_name', plot_model.exp_label_update)

    # send the same file to fit model, as fitting results need to be saved
    io_model.observe('file_name', fit_model.filename_update)
    io_model.observe('file_name', plot_model.plot_exp_data_update)

    # send exp data to different models
    io_model.observe('data', plot_model.exp_data_update)
    io_model.observe('data', param_model.exp_data_update)
    io_model.observe('data', fit_model.exp_data_update)
    io_model.observe('data_all', fit_model.exp_data_all_update)

    # send img dict to img_model for visualization
    io_model.observe('img_dict', img_model_adv.data_dict_update)
    io_model.observe('img_dict', img_model_rgb.data_dict_update)

    # set default parameters
    #io_model.observe('default_parameters', plot_model.parameters_update)
    #param_model.observe('param_new', plot_model.parameters_update)
    #fit_model.observe('param_dict', param_model.param_changed)

    xrfview = XRFGui(io_model=io_model,
                     param_model=param_model,
                     plot_model=plot_model,
                     fit_model=fit_model,
                     setting_model=setting_model,
                     img_model_adv=img_model_adv,
                     img_model_rgb=img_model_rgb)

    xrfview.show()
    app.start()


if __name__ == "__main__":
    run()
