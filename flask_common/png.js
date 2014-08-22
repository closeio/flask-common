// PhantomJS program to generate a PNG based on stdin (e.g. SVG image)
// Example: curl http://upload.wikimedia.org/wikipedia/commons/f/fd/Ghostscript_Tiger.svg | phantomjs png.js > test.png && open test.png
/*
From Flask/Python:
    p = Popen(['phantomjs', '%s/png.js' % os.path.dirname(os.path.realpath(__file__))], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    out = p.communicate(input=svg.encode('utf-8'))[0]
    strIO = StringIO.StringIO()
    strIO.write(out)
    strIO.seek(0)
    return send_file(strIO, as_attachment=True, attachment_filename='file.png')
*/

var page = require('webpage').create(),
    system = require('system'),
    fs = require('fs');

page.content = fs.read('/dev/stdin');

window.setTimeout(function() {
    page.render('/dev/stdout', { format: 'png' });
    phantom.exit();
}, 1);

