import os

def render_pdf(html):
    """mimerender helper to render a PDF from HTML using xhtml2pdf.

    Usage: http://philfreo.com/blog/render-a-pdf-from-html-using-xhtml2pdf-and-mimerender-in-flask/
    """
    from xhtml2pdf import pisa
    from cStringIO import StringIO
    pdf = StringIO()
    pisa.CreatePDF(StringIO(html.encode('utf-8')), pdf)
    resp = pdf.getvalue()
    pdf.close()
    return resp

def render_pdf_phantomjs(html):
    """mimerender helper to render a PDF from HTML using phantomjs."""
    # The 'makepdf.js' PhantomJS program takes HTML via stdin and returns PDF binary via stdout
    # https://gist.github.com/philfreo/5854629
    # Another approach would be to have PhantomJS do a localhost read of the URL, rather than passing html around.
    from subprocess import Popen, PIPE, STDOUT
    p = Popen(['phantomjs', '%s/pdf.js' % os.path.dirname(os.path.realpath(__file__))], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    return p.communicate(input=html.encode('utf-8'))[0]
