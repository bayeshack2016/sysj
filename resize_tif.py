from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--scale", "-s", type=int,
    help="How much to scale down the image by"
)
parser.add_argument(
    "--scale-width", "-sw", type=int, default=2,
    help="How much to scale down the width by"
)
parser.add_argument(
    "--scale-height", "-sh", type=int, default=2,
    help="How much to scale down the height by"
)
parser.add_argument("infile")
parser.add_argument("outfile")
args = parser.parse_args()

# SEE: http://effbot.org/imagingbook/image.htm#resize
# NOTE: Image.ANTIALIAS doesn't seem to work well
filter_type = Image.BILINEAR

width_scale = args.scale or args.width_scale
height_scale = args.scale or args.height_scale
image = Image.open(args.infile)
resized_image = image.resize((image.width / width_scale, image.height / height_scale), filter_type)
resized_image.save(args.outfile)
