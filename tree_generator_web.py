#!/usr/bin/python3
# -*- encoding:utf-8 -*-

import io
import math
import flask
import tree_generator

app = flask.Flask(__name__)

def get_parameters(form):
    return {
        'background_color': form['background_color'],
        'foreground_color': form['foreground_color'],
        'size_x': int(form['size_x']),
        'size_y': int(form['size_y']),
        'starting_angle': math.radians(float(form['starting_angle'])),
        'starting_length': int(form['starting_length']),
        'starting_width': int(form['starting_width']),
        'max_length': int(form['max_length']),
        'branch_chance': (float(form['branch_chance_mu']),
                          int(form['branch_chance_sigma'])),
        'angle_variance': math.radians(float(form['angle_variance'])),
        'shortening': (float(form['shortening_mu']),
                          int(form['shortening_sigma'])),
        'thinning': (float(form['thinning_mu']),
                     int(form['thinning_sigma'])),
        'min_width': int(form['min_width']),
        'min_length': int(form['min_length']),
        'min_angle': math.radians(float(form['min_angle'])),
        'max_angle': math.radians(float(form['max_angle'])),
    }

@app.route('/', methods=['GET', 'POST'])
def tree():
    if flask.request.method == 'GET':
        return app.send_static_file('form.html')
    else:
        params = get_parameters(flask.request.form)
        if params['branch_chance'][0] > 5:
            flask.abort(500)
        im = tree_generator.get_tree(params)
        output = io.BytesIO()
        im.save(output, format='png')
        output.seek(0)
        return flask.send_file(output, mimetype="image/png")

def main():
    app.run()

if __name__ == '__main__':
    main()
