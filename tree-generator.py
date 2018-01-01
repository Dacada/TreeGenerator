#!/usr/bin/python3
# -*- encoding:utf-8 -*-

import math
import random
import argparse
from PIL import Image, ImageDraw

"""Create pretty or awful trees."""

def draw_line(draw, start, angle, length, width, color):
    """
    Draw a line on an image starting at the given point with the given
    angle (radians) and of the given length and width. Return point at
    which line ends.
    """
    d1 = int(round(math.sin(angle) * length))
    d2 = int(round(math.cos(angle) * length))
    stop = (start[0] + d1, start[1] + d2)
    draw.line(start+stop, fill=color, width=width)
    return stop

def draw_tree(draw, root, angle, length, width, total_length, p):
    if total_length >= p['max_length']:
        return

    if width < p['min_width']:
        return

    if length < p['min_length']:
        return
        
    leaf = draw_line(draw, root, angle, length, width, p['foreground_color'])
    total_length += length

    branches = int(abs(round(random.gauss(*p['branch_chance']))))
    for __ in range(branches):
        new_angle = random.gauss(angle, p['angle_variance'])
        
        if new_angle < p['min_angle']:
            new_angle = p['min_angle']
            
        if new_angle > p['max_angle']:
            new_angle = p['max_angle']
            
        new_length = length - random.gauss(*p['shortening'])
        new_width = int(round(width - random.gauss(*p['thinning'])))
        draw_tree(draw, leaf, new_angle, new_length, new_width, total_length, p)

def get_parameters():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--background_color', default="white", help="Color of the background")
    parser.add_argument('--foreground_color', default="black", help="Color of the tree")
    parser.add_argument('--size_x', default=1024, help="X dimension of the image (pixels)", type=int)
    parser.add_argument('--size_y', default=512, help="Y dimension of the image (pixels)", type=int)
    parser.add_argument('--starting_angle', default=180, help="Starting angle of the tree in degrees. 180 is standing upwards like a normal tree", type=float)
    parser.add_argument('--starting_length', default=100, help="Length of the trunk. Branches get smaller with each generation. In pixels.", type=int)
    parser.add_argument('--starting_width', default=30, help="Width of the trunk. Branches get thinner with each generation. In pixels.", type=int)
    parser.add_argument('--max_length', default=400, help="Maximum length from the base to each leaf. Branches longer than this will never be created", type=int)
    parser.add_argument('--branch_chance_mu', default=3, help="Average number of new branches spawned from a branch", type=float)
    parser.add_argument('--branch_chance_sigma', default=1, help="Standard deviation of new branches spawned from a branch", type=float)
    parser.add_argument('--angle_variance', default=30, help="Standard deviation for the angle of new branches. It's the previous angle deviated.", type=float)
    parser.add_argument('--shortening_mu', default=15, help="Average shortening with each generation", type=float)
    parser.add_argument('--shortening_sigma', default=1, help="Standard deviation for shortening", type=int)
    parser.add_argument('--thinning_mu', default=5, help="Average thinning with each generation", type=float)
    parser.add_argument('--thinning_sigma', default=1, help="Standard deviation for thinning", type=int)
    parser.add_argument('--min_width', default=5, help="Minimum width for branches. Branches becoming thinner than this will stop appearing", type=int)
    parser.add_argument('--min_length', default=0, help="Minimum length for branches. Branches becoming shorter than this will stop appearing", type=int)
    parser.add_argument('--min_angle', default=90, help="Minimum angle for branches. Branches twisting lower than this will be forced to this value", type=float)
    parser.add_argument('--max_angle', default=270, help="Maximum angle for branches. Branches twisting higher than this will be forced to this value", type=float)

    args = parser.parse_args()
    
    return {
        'background_color' : args.background_color,
        'foreground_color' : args.foreground_color,
        'size_x' : args.size_x,
        'size_y' : args.size_y,
        'starting_angle' : math.radians(args.starting_angle),
        'starting_length' : args.starting_length,
        'starting_width' : args.starting_width,
        'max_length' : args.max_length,
        'branch_chance' : (args.branch_chance_mu, args.branch_chance_sigma),
        'angle_variance' : math.radians(args.angle_variance),
        'shortening' : (args.shortening_mu, args.shortening_sigma),
        'thinning' : (args.thinning_mu, args.thinning_sigma),
        'min_width' : args.min_width,
        'min_length' : args.min_length,
        'min_angle' : math.radians(args.min_angle),
        'max_angle' : math.radians(args.max_angle)
    }

def get_tree(parameters):
    im = Image.new('RGB',
                   (parameters['size_x'], parameters['size_y']),
                   parameters['background_color'])
    
    root = (parameters['size_x']/2, parameters['size_y'])
    angle = parameters['starting_angle']
    length = parameters['starting_length']
    width = parameters['starting_width']
    
    draw_tree(ImageDraw.Draw(im), root, angle, length, width, 0, parameters)
    
    return im

def main():
    parameters = get_parameters()
    im = get_tree(parameters)
    im.show()

if __name__ == '__main__':
    main()
