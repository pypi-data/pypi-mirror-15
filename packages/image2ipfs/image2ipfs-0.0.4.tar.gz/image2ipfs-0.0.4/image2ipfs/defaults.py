# Copyright 2016 Julian Vassev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

import os

VERSION='0.0.4'

_VERBOSE=True

try:
    with open(os.path.join(os.path.dirname(__file__), 'git-revision')) as f:
        DEBUG_VERSION = VERSION + '/' + f.read().strip()
except Exception as e:
    print e
    DEBUG_VERSION = VERSION + '/unknown'
