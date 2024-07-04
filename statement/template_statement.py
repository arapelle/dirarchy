import xml.etree.ElementTree as XMLTree
from pathlib import Path

from constants import names
from statement.abstract_dir_statement import AbstractDirStatement
from statement.abstract_statement import AbstractStatement
from statement.vars_statement import VarsStatement


class TemplateStatement(AbstractDirStatement):
    from temgen import Temgen

    STATEMENT_LABEL = "template"

    TEMGEN_LABEL = names.LOWER_PROGRAM_NAME
    TEMPLATE_FILEPATH_LABEL = "template_filepath"
    OUTPUT_DIRPATH_LABEL = "output_dirpath"

    def __init__(self, current_node: XMLTree.Element, caller_statement: AbstractStatement | None, **kargs):
        if current_node.tag != self.STATEMENT_LABEL:
            raise RuntimeError(f"Root node must be '{self.STATEMENT_LABEL}'!")
        self.__caller_statement = caller_statement
        parent_statement = None
        if self.__caller_statement is not None:
            parent_statement = self.__caller_statement.parent_statement()
            self.__parent_template_statement = parent_statement.template_statement()
            assert self.__parent_template_statement is not None
            self.__temgen = self.__parent_template_statement.temgen()
            self.__output_dirpath = parent_statement.current_dir_statement().current_output_dirpath()
        else:
            self.__parent_template_statement = None
            self.__temgen = kargs[TemplateStatement.TEMGEN_LABEL]
            self.__output_dirpath = kargs[TemplateStatement.OUTPUT_DIRPATH_LABEL]
        if self.__temgen.check_template_activated():
            self.__temgen.check_template(current_node)
        super().__init__(current_node, parent_statement, **kargs)
        assert self.parent_statement() == parent_statement
        self.__template_filepath = kargs.get(TemplateStatement.TEMPLATE_FILEPATH_LABEL, None)
        assert isinstance(self.__template_filepath, Path) or self.__template_filepath is None
        self.__current_child_statement = None
        self.__expected_statement = None
        ui = kargs.get("ui")
        if ui is not None:
            self.variables().update_vars_from_dict(self.temgen().call_ui(ui, self))

    def parent_template_statement(self):
        return self.__parent_template_statement

    def root_parent_template_statement(self):
        if self.__parent_template_statement is None:
            return self
        return self.__parent_template_statement.root_parent_template_statement()

    def temgen(self) -> Temgen:
        return self.__temgen

    def template_filepath(self):
        return self.__template_filepath

    def template_statement(self):
        return self

    def current_output_dirpath(self) -> Path:
        return self.__output_dirpath

    def current_main_statement(self):
        if self.parent_statement() is not None:
            return self.parent_statement().current_main_statement()
        return self

    def current_child_statement(self):
        return self.__current_child_statement

    def expected_statement(self):
        return self.__expected_statement

    def extract_expected_statement(self):
        expected_statement = self.__expected_statement
        self.__expected_statement = None
        return expected_statement

    def execute(self):
        if self.__template_filepath is not None:
            self.logger.info(f"Template file: {self.__template_filepath}")
        self.__check_temgen_version()
        self.treat_children_nodes()
        self.__current_child_statement = None

    def __check_temgen_version(self):
        from temgen import Temgen
        import semver
        min_version = self.current_node().get("temgen-min-version", None)
        max_version = self.current_node().get("temgen-max-version", None)
        if min_version is None and max_version is None:
            return
        if min_version is not None:
            min_version = semver.Version.parse(min_version)
            max_version = semver.Version.parse(max_version) if max_version is not None else Temgen.VERSION
        else:
            min_version = Temgen.VERSION
            max_version = semver.Version.parse(max_version)
        if min_version > max_version:
            raise RuntimeError("temgen-min-version should not be greater than temgen-max-version: "
                                f"min: {min_version}, max: {max_version}")
        if Temgen.VERSION < min_version:
            raise RuntimeError("temgen is not compatible with the expected min version: "
                               f"{Temgen.VERSION} (min: {min_version})")
        if Temgen.VERSION > max_version:
            raise RuntimeError("temgen is not compatible with the expected max version: "
                               f"{Temgen.VERSION} (max: {max_version})")

    def check_number_of_children_nodes_of(self, node: XMLTree.Element):
        if node == self.current_node():
            limit = 2 if node.find("vars") is not None else 1
            limit += len(node.findall("var"))
            if len(node) > limit:
                raise RuntimeError("Too many nodes under <template>.")

    def treat_child_node(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        if node == self.current_node():
            if self.__caller_statement is not None and child_node.tag != "vars" and child_node.tag != "var":
                expected_tag = self.__caller_statement.current_node().tag
                if child_node.tag != expected_tag:
                    raise RuntimeError(f"Unexpected node ({child_node.tag}) under <template>. "
                                       f"Expected: {expected_tag}.")
                if child_node.tag == "contents":
                    contents_statement = self._create_contents_statement(node, child_node, current_statement)
                    contents_statement.run()
                    self.__post_treat_child_node(node, child_node)
                    return
        super().treat_child_node(node, child_node, current_statement)
        self.__post_treat_child_node(node, child_node)

    def __post_treat_child_node(self, node, child_node):
        if node == self.current_node():
            assert self.__current_child_statement is not None
            if self.__caller_statement is not None and child_node.tag != "vars" and child_node.tag != "var":
                self.__expected_statement = self.__current_child_statement
            self.__current_child_statement = None

    def _create_dir_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        dir_statement = super()._create_dir_statement(node, child_node, current_statement)
        if node == self.current_node():
            self.__current_child_statement = dir_statement
        return dir_statement

    def _create_file_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        file_statement = super()._create_file_statement(node, child_node, current_statement)
        if node == self.current_node():
            self.__current_child_statement = file_statement
        return file_statement

    def _create_if_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        if_statement = super()._create_if_statement(node, child_node, current_statement)
        if node == self.current_node():
            self.__current_child_statement = if_statement
        return if_statement

    def _create_match_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        match_statement = super()._create_match_statement(node, child_node, current_statement)
        if node == self.current_node():
            self.__current_child_statement = match_statement
        return match_statement

    def _create_contents_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        from statement.contents_statement import ContentsStatement
        contents_statement = ContentsStatement(child_node, current_statement)
        if node == self.current_node():
            self.__current_child_statement = contents_statement
        return contents_statement

    def _create_exec_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        exec_statement = super()._create_exec_statement(node, child_node, current_statement)
        if node == self.current_node():
            self.__current_child_statement = exec_statement
        return exec_statement

    def _create_vars_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        vars_statement = super()._create_vars_statement(node, child_node, current_statement)
        if node == self.current_node():
            self.__current_child_statement = vars_statement
        return vars_statement

    def _create_var_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        vars_statement = super()._create_var_statement(node, child_node, current_statement)
        if node == self.current_node():
            self.__current_child_statement = vars_statement
        return vars_statement
