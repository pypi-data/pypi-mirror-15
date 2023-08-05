from jinja2 import Environment, FileSystemLoader

from moban.utils import open_yaml, load_external_engine
from moban.constants import DEFAULT_TEMPLATE_TYPE

MESSAGE_TEMPLATING = "Templating %s to %s"


class EngineFactory(object):
    @staticmethod
    def get_engine(template_type):
        if template_type == DEFAULT_TEMPLATE_TYPE:
            return Engine
        else:
            try:
                external_engine = load_external_engine(template_type)
            except ImportError:
                raise NotImplementedError("No such template support")
            return external_engine.get_engine(template_type)


class Engine(object):
    def __init__(self, template_dirs, context_dirs):
        template_loader = FileSystemLoader(template_dirs)
        self.jj2_environment = Environment(
            loader=template_loader,
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True)
        self.context = Context(context_dirs)

    def render_to_file(self, template_file, data_file, output_file):
        template = self.jj2_environment.get_template(template_file)
        data = self.context.get_data(data_file)
        print(MESSAGE_TEMPLATING % (template_file, output_file))
        apply_template(template, data, output_file)

    def render_to_files(self, array_of_param_tuple):
        sta = Strategy(array_of_param_tuple)
        sta.process()
        choice = sta.what_to_do()
        if choice == Strategy.DATA_FIRST:
            self._render_with_finding_data_first(sta.data_file_index)
        else:
            self._render_with_finding_template_first(sta.template_file_index)

    def _render_with_finding_template_first(self, template_file_index):
        for (template_file, data_output_pairs) in template_file_index.items():
            template = self.jj2_environment.get_template(template_file)
            for (data_file, output) in data_output_pairs:
                print(MESSAGE_TEMPLATING % (template_file, output))
                data = self.context.get_data(data_file)
                apply_template(template, data, output)

    def _render_with_finding_data_first(self, data_file_index):
        for (data_file, template_output_pairs) in data_file_index.items():
            data = self.context.get_data(data_file)
            for (template_file, output) in template_output_pairs:
                print(MESSAGE_TEMPLATING % (template_file, output))
                template = self.jj2_environment.get_template(template_file)
                apply_template(template, data, output)


class Context(object):
    def __init__(self, context_dirs):
        self.context_dirs = context_dirs

    def get_data(self, file_name):
        return open_yaml(self.context_dirs, file_name)


def apply_template(jj2_template, data, output_file):
    """
    write templated result
    """
    with open(output_file, 'wb') as output:
        rendered_content = jj2_template.render(**data)
        output.write(rendered_content.encode('utf-8'))


class Strategy(object):
    DATA_FIRST = 1
    TEMPLATE_FIRST = 2

    def __init__(self, array_of_param_tuple):
        self.data_file_index = {}
        self.template_file_index = {}
        self.tuples = array_of_param_tuple

    def process(self):
        for (template_file, data_file, output_file) in self.tuples:
            _append_to_array_item_to_dictionary_key(
                self.data_file_index,
                data_file,
                (template_file, output_file)
            )
            _append_to_array_item_to_dictionary_key(
                self.template_file_index,
                template_file,
                (data_file, output_file)
            )

    def what_to_do(self):
        choice = Strategy.DATA_FIRST
        if self.data_file_index == {}:
            choice = Strategy.TEMPLATE_FIRST
        elif self.template_file_index != {}:
            data_files = len(self.data_file_index)
            template_files = len(self.template_file_index)
            if data_files > template_files:
                choice = Strategy.TEMPLATE_FIRST
        return choice


def _append_to_array_item_to_dictionary_key(adict, key, array_item):
    if key not in adict:
        adict[key] = []
    adict[key].append(array_item)
