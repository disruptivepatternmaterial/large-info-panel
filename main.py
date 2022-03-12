import argparse
import time
import sys

from data import Data
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from views.controllers.main import MainController


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--led-rows",
        action="store",
        help="Display rows. 16 for 16x32, 32 for 32x32. (Default: 16)",
        default=16,
        type=int,
    )
    parser.add_argument(
        "--led-cols",
        action="store",
        help="Panel columns. Typically 32 or 64. (Default: 32)",
        default=32,
        type=int,
    )
    parser.add_argument(
        "--led-brightness",
        action="store",
        help="Sets brightness level. Range: 1..100. (Default: 100)",
        default=100,
        type=int,
    )
    parser.add_argument(
        "--led-scan-mode",
        action="store",
        help="Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)",
        default=1,
        choices=range(2),
        type=int,
    )
    parser.add_argument(
        "--led-show-refresh",
        action="store_true",
        help="Shows the current refresh rate of the LED panel.",
    )
    parser.add_argument(
        "--led-slowdown-gpio",
        action="store",
        help="Slow down writing to GPIO. Range: 0..4. (Default: 2)",
        default=2,
        choices=range(5),
        type=int,
    )
    return parser.parse_args()


def get_rgb_matrix_options(args: object) -> RGBMatrixOptions:
    options = RGBMatrixOptions()
    options.rows = args.led_rows
    options.cols = args.led_cols
    options.brightness = args.led_brightness
    if args.led_show_refresh:
        options.show_refresh_rate = 1
    if args.led_slowdown_gpio != None:
        options.gpio_slowdown = args.led_slowdown_gpio
    return options


# Parse arguments
args = parse_args()

# Start fetching data
Data.start_all_data_threads()

# Initialize the RGB matrix
options = get_rgb_matrix_options(args=args)
rgb_matrix = RGBMatrix(options=options)

# Start the main controller - CTRL-C to exit
print(f"Running sunrise-alarm-clock-({rgb_matrix.height}x{rgb_matrix.width})")
main_controller = MainController(rgb_matrix=rgb_matrix)
main_controller.start()
try:
    print("Press CTRL-C to stop running.")
    main_controller.join()
except KeyboardInterrupt:
    print("\nExiting.\n")
    main_controller.stop()
    main_controller.join()
    sys.exit(0)
