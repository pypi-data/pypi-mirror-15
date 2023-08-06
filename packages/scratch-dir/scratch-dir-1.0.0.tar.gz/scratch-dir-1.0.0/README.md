scratch-dir
===========

Unit test mixin which creates a scratch director. Sets `self.scratch_dir` on
initialization, and deletes it when finished.

```py
import unittest
from scratch_dir import ScratchDirMixin

class TestThing(CreateScratchDirectoryMixin, unittest.TestCase):
    def setUp(self):
        import json
        import os

        super(TestThing, self).setUp()

        self.local_json_file = self.get_tmp_path('example.json')
        json.dump({'a': 42}, self.local_json_file)

        print 'Example file written to scratch dir: {}'.format(self.scratch_dir)
```


Development
-----------

```sh
pip install -r requirements_dev.txt
rake lint
```


Contribute
----------

- Issue Tracker: https://github.com/bodylabs/scratch-dir/issues
- Source Code: https://github.com/bodylabs/scratch-dir

Pull requests welcome!


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the two-clause BSD license.
