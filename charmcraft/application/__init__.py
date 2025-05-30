# Copyright 2023-2025 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For further info, check https://github.com/canonical/charmcraft
"""Craft-application based entrypoint for charmcraft.

This submodule contains what's needed to run charmcraft with the
craft-application framework, falling back to "classic" charmcraft when a command
is not available.

Help is (for now) handled by classic charmcraft.
"""

from charmcraft.application.main import APP_METADATA, Charmcraft, main, get_app_info

__all__ = ["APP_METADATA", "Charmcraft", "main", "get_app_info"]
