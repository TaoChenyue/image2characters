from image2characters import image2characters


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Image to characters")
    parser.add_argument(
        "--image",
        type=str,
        help="Path to the image file",
        default="assets/test.jpg",
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
        "-o",
        "--output",
        type=str,
        default="assets/output.png",
    )
    args = parser.parse_args()
    image = image2characters(
        image_path=args.image,
        characters=args.characters,
        font=args.font,
        grid_size=args.grid_size,
        font_size=args.font_size,
    )
    image.save(args.output)
