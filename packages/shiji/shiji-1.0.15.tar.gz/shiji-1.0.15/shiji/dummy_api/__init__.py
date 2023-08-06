# -*- coding: utf-8-*-
####################################################################
# FILENAME: ./dummy_api/__init__.py
# PROJECT: Shiji API
# DESCRIPTION: Dummy API
#
#
# $Id$
####################################################################
# (C)2015 DigiTar Inc.
# Licensed under the MIT License.
####################################################################

from shiji import urldispatch
import v1_0

# api_name, api_versions and version_router are required to be
# present for APIRouter to accept this module.

api_name = "dummy_api"
api_versions = { "1.0" : (r"1.0", v1_0) }

version_router = urldispatch.VersionRouter(api_versions)
