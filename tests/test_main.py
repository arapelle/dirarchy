import io
import sys

from main import Dirarchy
from tests.test_dirarchy_base import TestDirarchyBase


class TestDirarchy(TestDirarchyBase):
    def test_simple_dirtree(self):
        self._test_dirarchy_file("simple_dirtree")

    def test_simple_fdirtree(self):
        self._test_dirarchy_file("simple_fdirtree", stdin_str='arba\ncore')
