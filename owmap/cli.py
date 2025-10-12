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

    return parser

# TODO: Finish CLI
# TODO: Make all layers optional in CLI
# TODO: Add palette gen command in CLI
# TODO: Add testmap gen command in CLI
def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.maps:
        if len(args.maps) != 3:
            parser.error(
                "\n\t3 positional arguments required: " \
                "[heightmap] [terrainmap] [vegmap]"
            )
        height, terrain, veg = args.maps

    else:
        height = args.heightmap
        terrain = args.terrainmap
        veg = args.vegmap

    if not all([height, terrain, veg]):
        parser.error(
            "\n\tMissing required arguments, 1 or more of: "\
            "[heightmap] [terrainmap] [vegmap]"
        )

    genmap.process_map_images(height, terrain, veg, args.mapname)

if __name__ == "__main__":
    main()