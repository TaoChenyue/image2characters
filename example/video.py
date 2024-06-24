import cv2
from image2characters import video2characters


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Image to characters")
    parser.add_argument(
        "--video",
        type=str,
        help="Path to the video file",
        default="assets/test.mp4",
    )
    parser.add_argument(
        "--characters",
        type=str,
        default="$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    )
    parser.add_argument(
        "--font",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--grid_size",
        type=int,
        default=20,
    )
    parser.add_argument(
        "--font_size",
        type=int,
        default=20,
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=20,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="assets/output.mp4",
    )
    args = parser.parse_args()
    video2characters(
        video_path=args.video,
        output_path=args.output,
        characters=args.characters,
        font=args.font,
        grid_size=args.grid_size,
        font_size=args.font_size,
    )
