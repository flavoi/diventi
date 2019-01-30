import os, tempfile, time, logging
from subprocess import Popen, PIPE, check_output, STDOUT

from django.conf import settings
from django.http import HttpResponse

from django.template.loader import get_template


DEFAULT_INTERPRETER = 'lualatex'

logger = logging.getLogger(__name__)


class TexError(Exception):
    pass


def run_tex(source):
    with tempfile.TemporaryDirectory() as tempdir:
        latex_interpreter = getattr(settings, 'LATEX_INTERPRETER', DEFAULT_INTERPRETER)
        for i in range(2):
            latex_command = [latex_interpreter, '-output-directory', tempdir]    
            process = Popen(latex_command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            # process.communicate(source.encode('utf-8'))
            output = process.communicate(source.encode('utf-8'))[0]
            if process.returncode == 1:
                 logger.error(output)
                 raise TexError(source)
            filepath = os.path.join(tempdir, 'texput.pdf')
            print(filepath)
        with open(filepath, 'rb') as pdf_file:
            pdf = pdf_file.read()
    return pdf

def compile_template_to_pdf(template_name, context):
    source = render_template_with_context(template_name, context)
    return run_tex(source)

def render_template_with_context(template_name, context):
    template = get_template(template_name)
    return template.render(context)

def get_template(template_name):
    return get_template(template_name)


class PDFResponse(HttpResponse):

    def __init__(self, content, filename=None):
        super(PDFResponse, self).__init__(content_type='application/pdf')
        self['Content-Disposition'] = 'filename="{}"'.format(filename)
        self.write(content)


def render_to_pdf(template_name, context, filename=None):
    pdf = compile_template_to_pdf(template_name, context)
    return PDFResponse(pdf, filename=filename)

def render_to_tex(request, template_name, context):
    tex = render_template_with_context(template_name, context)
    raise TexError(tex)