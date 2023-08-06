InvisibleRoads Uploads
======================
Add basic file upload functionality to your Pyramid app.

Use
---
Prepare environment. ::

    export VIRTUAL_ENV=~/.virtualenvs/crosscompute
    virtualenv ${VIRTUAL_ENV}
    source ${VIRTUAL_ENV}/bin/activate

    export NODE_PATH=${VIRTUAL_ENV}/lib/node_modules
    npm install -g browserify uglify-js

Install package. ::

    cd ~/Projects/invisibleroads-uploads
    python setup.py develop
    bash refresh.sh

Configure views. ::

    config.include('invisibleroads_uploads')

Call template macro. ::

    {% from 'invisibleroads_uploads:templates/parts.jinja2' import render_upload_button %}
    {{ render_upload_button(id='xyz-upload', text='Browse for xyz') }}

Add script. ::

    $('#abc-upload').on('uploaded.ir.upload', function(d) {
        console.log('Uploaded xyz');
        console.log(d);
    });
