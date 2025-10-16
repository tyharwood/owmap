import argparse, sys
import owmap.genmap as genmap

def build_parser():
    parser = argparse.ArgumentParser(
        description="Generate Old World maps from terrain, height, and vegetation data",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'maps', nargs='*',
        help='Map images in order: [height] [terrain] [vegetation]'
    )

    parser.add_argument(
        '--mapname', '-o', default="newmap.xml", 
        help='Output map name (default: map.xml)'
    )

    parser.add_argument(
        '--heightmap','-e',
        help='Height map '
    )

    parser.add_argument(
        '--terrainmap', '-t',
        help='Terrain map',
    )

    parser.add_argument(
        '--vegmap', '-v',
        help='Vegetation map'
    )

    parser.add_argument(
        '--example', action='store_true',
        default=False,
        help='Generate an example image-set'
    )

    parser.add_argument(
        '--genpalettes', '-p',
        action='store_true', default=False,
        help='Generate a small image of the current palette used'
    )

    return parser

# TODO: Make all layers optional in CLI
# TODO: Add palette gen command in CLI
# TODO: Add testmap gen command in CLI
def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.example:
        genmap.generate_donut_map('./docs/')

    if args.genpalettes:
        genmap.generate_height_palette()
        genmap.generate_terrain_palette()
        genmap.generate_veg_palette()

    expected_args = ['height', 'terrain', 'veg']
    argdict = {
        'height': str(),
        'terrain':str(),
        'veg': str()
    }

    for i in range(min(len(args.maps), len(expected_args))):
        argdict[expected_args[i]] = args.maps[i]

    if args.heightmap:    argdict['height'] = args.heightmap
    if args.terrainmap:   argdict['terrain'] = args.terrainmap
    if args.vegmap:       argdict['veg'] = args.vegmap

    if not all([argdict['height'], argdict['terrain'], argdict['veg']]):
        parser.print_usage()
        parser.exit(2)

    genmap.process_map_images(
        argdict['height'], argdict['terrain'], argdict['veg'], args.mapname
    )

if __name__ == "__main__":
    main()