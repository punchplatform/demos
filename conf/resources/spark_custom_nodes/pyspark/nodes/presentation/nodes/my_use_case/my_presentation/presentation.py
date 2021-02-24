#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License Agreement
# This code is licensed under the outer restricted Tiss license:
#
#  Copyright [2014]-[2019] Thales Services under the Thales Inner Source Software License
#  (Version 1.0, InnerPublic -OuterRestricted the "License");
#
#  You may not use this file except in compliance with the License.
#
#  The complete license agreement can be requested at contact@punchplatform.com.
#
#  Refer to the License for the specific language governing permissions and limitations
#  under the License.

from punchline_python.core.holders.input_holder import InputHolder
from punchline_python.core.holders.output_holder import OutputHolder
from punchline_python.core.node import AbstractNode

__author__ = "Pierre"


class Presentation(AbstractNode):

    @staticmethod
    def unflat_tag(tags, elem):
        if (len(tags) == 1):
            return {tags[0]: elem}
        elif (len(tags) > 1):
            return {tags[0]: Presentation.unflat_tag(tags[1:], elem)}

    @staticmethod
    def unflat_dico(dico):
        to_return = {}
        for elem in dico:
            if dico[elem] == 'na':
                continue
            tags = elem.split('.')
            if len(tags) == 1:
                to_return[elem] = dico[elem]
            elif len(tags) > 1:
                to_return[tags[0]] = Presentation.unflat_tag(tags[1:], dico[elem])

        return to_return

    def __init__(self) -> None:
        super().__init__()

    def execute(self, input_data: InputHolder, output_data: OutputHolder) -> None:
        print('Begin presentation...')
        # Catch pandas dataframe
        df = input_data.get()
        df = df.fillna("na")
        output = []
        for elem in df.to_dict("records"):
            output.append(Presentation.unflat_dico(elem))
        output_data.set(value=output, alias="data")
        print("...End presentation")

