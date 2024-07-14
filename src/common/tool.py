import io
import re

import base64
from typing import List

from PIL import Image


def change_body_in_depth(prebody: dict, info: str, depth: int = 0, max_depth: int = 15, public: str = '') -> dict:
    if depth == 0:
        body = prebody['body'].copy()
        public = prebody['public']
    else:
        body = prebody

    if public in body:
        body[public] += info  # noqa: WPS529
        return body

    print("body:", body)
    print("depth:", depth)
    assert depth < max_depth, "The max depth is overreached"

    args = [body[body['type']], info, depth + 1]
    body[body['type']] = change_body_in_depth(*args, public=public)
    return body


def load_and_resize_base64_image(path: str, size=(512, 512)):
    """
    Resize an image encoded as a Base64 string
    """
    with open(path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")
    # Decode the Base64 string
    img_data = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_data))

    # Resize the image
    resized_img = img.resize(size, Image.LANCZOS)

    # Save the resized image to a bytes buffer
    buffered = io.BytesIO()
    resized_img.save(buffered, format=img.format)

    # Encode the resized image to Base64
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def extract_parts(input_question: str, bodies: dict) -> List[dict]:
    tag_names = bodies['tags'].keys()
    pattern = re.compile(rf'<({"|".join(tag_names)})>(.*?)<\1>')

    parts = []
    last_end = 0

    for match in pattern.finditer(input_question):
        start, end = match.span()

        if start > last_end:
            text_part = input_question[last_end:start].strip()
            if text_part:
                text_part_body = change_body_in_depth(bodies['text'], text_part)
                parts.append(text_part_body)

        image = load_and_resize_base64_image(match.group(2))
        image_part_body = change_body_in_depth(bodies['tags'][match.group(1)], image)
        parts.append(image_part_body)

        last_end = end

    if last_end < len(input_question):
        text_part = input_question[last_end:].strip()
        if text_part:
            text_part_body = change_body_in_depth(bodies['text'], text_part)
            parts.append(text_part_body)

    return parts
