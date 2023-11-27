from main import Dirarchy
from tests.test_dirarchy_base import TestDirarchyBase


class TestDirarchy(TestDirarchyBase):
    def test_simple_dirtree(self):
        project_root_dir = "simple_dirtree"
        dirarchy = Dirarchy(self._ut_context_argv + ['--', f'input/{project_root_dir}.xml'])
        dirarchy.run()
        self.compare_output_and_expected(project_root_dir)
