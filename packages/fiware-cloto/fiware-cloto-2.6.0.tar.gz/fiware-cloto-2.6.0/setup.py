#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#
from setuptools import setup, find_packages
from fiware_cloto.cloto_settings.settings import VERSION
from pip.req import parse_requirements
import os
from distutils.command.install import install as _install

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fiware_cloto.cloto_settings.settings")


def _post_install(dir):
    import django
    django.setup()
    from django.core.management import call_command

    call_command('makemigrations', 'cloto', verbosity=3, interactive=False)
    call_command('migrate', verbosity=3, interactive=False)


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Running post install task")

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=False)
# > requirements_list is a list of requirement; e.g. ['requests==2.6.0', 'Fabric==1.8.3']
requirements_list = [str(ir.req) for ir in install_reqs]

setup(
  name='fiware-cloto',
  packages=find_packages(exclude=['*tests*']),
  install_requires=requirements_list,
  package_data={
    'cloto_settings': ['*.cfg']
  },
  version=VERSION,
  description='This module is part of FI-WARE Policy Manager. It provides an API-REST to create rules associated '
            'to servers, subscribe servers to Context Broker to get information about resources consumption of that'
            ' servers and launch actions described in rules when conditions are given.',
  author='Fernando Lopez Aguilar, Guillermo Jimenez Prieto',
  author_email='fernando.lopezaguilar@telefonica.com, e.fiware.tid@telefonica.com',
  license='Apache 2.0',
  url='https://github.com/telefonicaid/fiware-cloto',
  download_url='https://github.com/telefonicaid/fiware-cloto/tarball/v%s' % VERSION,
  keywords=['fiware', 'policy', 'manager', 'cloud'],
  classifiers=[
        "License :: OSI Approved :: Apache Software License", ],
  cmdclass={'install': install},
)
