from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
import cv2
from tqdm import trange


def get_font(font: str | None = None, size: int = 45) -> ImageFont.FreeTypeFont:
    if font is None:
        font = ImageFont.load_default(size=size)
    else:
        font = ImageFont.truetype(font=font, size=size)
    return font


def get_character_density(
    text: str, font: str | None = None, grid_size: int = 50, font_size: int = 45
) -> float:
    image = Image.new(mode="1", size=(grid_size, grid_size), color="white")
    draw = ImageDraw.Draw(image)
    draw.text(xy=(0, 0), text=text, fill=(0), font=get_font(font, font_size))
    image = np.asarray(image, dtype=np.float32)
    area = grid_size**2
    return float((area - image.sum()) / area)


def sorted_characters(
    characters: str,
    font: str | None = None,
) -> list[str]:
    density = [
        get_character_density(x, font=font, grid_size=50, font_size=45)
        for x in characters
    ]
    return [
        x[0] for x in sorted(zip(characters, density), key=lambda x: x[1], reverse=True)
    ]


def image2matrix(
    image: Image.Image | np.ndarray,
    characters: str,
    grid_size=50,
) -> list[list[str]]:
    length = len(characters)
    image = np.array(image, dtype=np.uint8)
    matrix = [
        [
            float(
                np.sum(image[i : i + grid_size, j : j + grid_size])
                / (grid_size**2 * 255)
            )
            for j in range(0, image.shape[1], grid_size)
        ]
        for i in range(0, image.shape[0], grid_size)
    ]
    # print(matrix)
    txt_matrix = [[characters[int((length - 1) * x)] for x in row] for row in matrix]
    return txt_matrix


def matrix2image(
    txt_matrix: list[list[str]],
    font: str | None = None,
    grid_size=50,
    font_size: int = 45,
):
    width = len(txt_matrix[0]) * grid_size
    height = len(txt_matrix) * grid_size
    image = Image.new(mode="L", size=(width, height), color="white")
    draw = ImageDraw.Draw(image)
    font = get_font(font=font, size=font_size)
    for i, row in enumerate(txt_matrix):
        for j, item in enumerate(row):
            draw.text(
                xy=(j * grid_size, i * grid_size),
                text=item,
                fill=(0),
                font=font,
            )
    return image


def image2characters(
    image_path: str | Path,
    characters: str,
    font=None,
    grid_size=50,
    font_size: int = 45,
):
    image = Image.open(image_path).convert("L")
    characters = sorted_characters(characters, font=font)
    matrix = image2matrix(image, characters, grid_size=grid_size)
    return matrix2image(matrix, font, grid_size, font_size).resize(image.size)


def video2characters(
    video_path: str | Path,
    output_path: str | Path,
    characters: str,
    font=None,
    grid_size=50,
    font_size: int = 45,
    fourcc: str = "mp4v",
):
    characters = sorted_characters(characters, font=font)
    capture = cv2.VideoCapture(video_path)
    frame_cnt = int(capture.get(7))
    width = int(capture.get(3))
    height = int(capture.get(4))
    fps = int(capture.get(5))
    f = cv2.VideoWriter_fourcc(*fourcc)
    writer = cv2.VideoWriter(output_path, f, fps, (width, height), isColor=False)
    if capture.isOpened():
        for _ in trange(frame_cnt):
            ret, img_src = capture.read()
            if not ret:
                break
            img_src = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
            matrix = image2matrix(img_src, characters, grid_size=grid_size)
            img_out = matrix2image(matrix, font, grid_size, font_size).resize(
                (width, height)
            )
            img_out = np.asarray(img_out)
            writer.write(img_out)
    else:
        raise BufferError("视频打开失败！")
    writer.release()
