#!/usr/bin/env python3
"""Build the 26 November 2026 one-page newspaper image.

Deterministic: no network, no randomness, no clock. Running this
script twice produces a byte-identical PNG.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "artwork", "entry.png")

W = 1024
H = 1024
MARGIN = 36
CONTENT_RIGHT = W - MARGIN
CONTENT_W = CONTENT_RIGHT - MARGIN

PAPER = (250, 246, 236)
BLACK = (0, 0, 0)
RED = (178, 34, 34)
DARK_GREY = (70, 70, 70)
GREY = (110, 110, 110)
LIGHT_LINE = (190, 184, 172)
NAVY = (22, 50, 79)
CREAM = (250, 246, 236)
GOLD = (201, 162, 39)
PALE_BLUE_GREY = (168, 186, 203)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def fit_serif_bold(text, start_size):
    """Shrink a bold serif font until *text* fits the content width."""
    size = start_size
    while size > 10:
        f = font("LiberationSerif-Bold.ttf", size)
        if f.getlength(text) <= CONTENT_W:
            return f, size
        size -= 1
    return font("LiberationSerif-Bold.ttf", 10), 10


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def line_height(draw, text, fnt):
    ascent, descent = fnt.getmetrics()
    return ascent + descent


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- Top rules -----------------------------------------------------
    draw.rectangle([MARGIN, 26, CONTENT_RIGHT, 28], fill=BLACK)
    draw.rectangle([MARGIN, 32, CONTENT_RIGHT, 32], fill=BLACK)

    # --- Masthead ------------------------------------------------------
    mast_font, _ = fit_serif_bold("THE WORLD TODAY", 84)
    y = 38
    draw.text((W // 2, y), "THE WORLD TODAY", font=mast_font,
              fill=BLACK, anchor="ma")
    box = draw.textbbox((W // 2, y), "THE WORLD TODAY",
                        font=mast_font, anchor="ma")
    y = box[3] + 8

    # --- Date bar ------------------------------------------------------
    draw.rectangle([MARGIN, y, CONTENT_RIGHT, y + 32], fill=BLACK)
    date_font = font("LiberationSans-Bold.ttf", 21)
    mid = y + 16
    draw.text((MARGIN + 14, mid), "THURSDAY, 26 NOVEMBER 2026",
              font=date_font, fill=(255, 255, 255), anchor="lm")
    draw.text((CONTENT_RIGHT - 14, mid), "THE WORLD IN ONE PAGE",
              font=date_font, fill=(255, 255, 255), anchor="rm")
    y += 32 + 9

    # --- Kicker --------------------------------------------------------
    kicker_font = font("LiberationSans-Bold.ttf", 22)
    draw.text((MARGIN, y), "LEAD STORY  \u2022  TRADE  \u2022  WASHINGTON",
              font=kicker_font, fill=RED, anchor="la")
    y += line_height(draw, "LEAD STORY", kicker_font) + 5

    # --- Headline, two lines -------------------------------------------
    head_font = font("LiberationSerif-Bold.ttf", 58)
    for headline_line in ("U.S. PROPOSES NEW TARIFFS",
                          "ON 14 TRADING PARTNERS"):
        draw.text((MARGIN, y), headline_line, font=head_font,
                  fill=BLACK, anchor="la")
        y += line_height(draw, headline_line, head_font) + 2
    y += 2

    # --- Subhead --------------------------------------------------------
    sub_font = font("LiberationSerif-Bold.ttf", 29)
    sub_text = "China faces the highest rate, at 20%."
    draw.text((MARGIN, y), sub_text, font=sub_font, fill=RED, anchor="la")
    y += line_height(draw, sub_text, sub_font) + 5

    # --- Standfirst ------------------------------------------------------
    stand_font = font("LiberationSerif-Regular.ttf", 24)
    stand_text = ("Washington says the duties fight excess factory "
                  "capacity. The European Union faces 15%. They would "
                  "take effect after a January hearing.")
    for stand_line in wrap(draw, stand_text, stand_font, CONTENT_W):
        draw.text((MARGIN, y), stand_line, font=stand_font,
                  fill=BLACK, anchor="la")
        y += line_height(draw, stand_line, stand_font) + 3
    y += 7

    # --- Chart panel -----------------------------------------------------
    panel_top = y
    panel_h = 156
    draw.rectangle([MARGIN, panel_top, CONTENT_RIGHT, panel_top + panel_h],
                   fill=NAVY, outline=BLACK, width=2)
    title_font = font("LiberationSans-Bold.ttf", 20)
    draw.text((MARGIN + 16, panel_top + 12),
              "PROPOSED CAPPED TARIFF RATES",
              font=title_font, fill=CREAM, anchor="la")

    label_font = font("LiberationSans-Bold.ttf", 20)
    value_font = font("LiberationSerif-Bold.ttf", 28)
    bar_x = MARGIN + 16
    track_len = 520
    rows = [
        ("CHINA", 20, GOLD, panel_top + 42),
        ("EUROPEAN UNION", 15, CREAM, panel_top + 94),
    ]
    for label, pct, colour, row_y in rows:
        draw.text((bar_x, row_y), label, font=label_font,
                  fill=CREAM, anchor="la")
        bar_top = row_y + 27
        filled = int(round(track_len * pct / 25.0))
        draw.rectangle([bar_x, bar_top, bar_x + filled, bar_top + 18],
                       fill=colour)
        value = "%d%%" % pct
        draw.text((bar_x + filled + 10, bar_top + 9), value,
                  font=value_font, fill=colour, anchor="lm")

    # Right-hand panel summary, past a thin vertical divider.
    divider_x = 748
    draw.line([(divider_x, panel_top + 14),
               (divider_x, panel_top + panel_h - 14)],
              fill=CREAM, width=1)
    right_cx = (divider_x + CONTENT_RIGHT) // 2
    big_font = font("LiberationSerif-Bold.ttf", 58)
    draw.text((right_cx, panel_top + 18), "14", font=big_font,
              fill=GOLD, anchor="ma")
    big_box = draw.textbbox((right_cx, panel_top + 18), "14",
                            font=big_font, anchor="ma")
    partners_font = font("LiberationSans-Bold.ttf", 20)
    draw.text((right_cx, big_box[3] + 4), "PARTNERS NAMED",
              font=partners_font, fill=CREAM, anchor="ma")
    partners_box = draw.textbbox((right_cx, big_box[3] + 4),
                                 "PARTNERS NAMED", font=partners_font,
                                 anchor="ma")
    hearing_font = font("LiberationSans-Regular.ttf", 19)
    draw.text((right_cx, partners_box[3] + 6), "Hearing in January",
              font=hearing_font, fill=PALE_BLUE_GREY, anchor="ma")

    y = panel_top + panel_h + 8

    # --- Divider under the panel -----------------------------------------
    draw.rectangle([MARGIN, y, CONTENT_RIGHT, y + 1], fill=BLACK)
    y += 9

    # --- Five supporting stories -----------------------------------------
    stories = [
        ("EGYPT", (140, 40, 40),
         "Cairo ring-road fire kills at least 31",
         "A vehicle carrying fuel overturned and caught fire in Giza, "
         "the Health Ministry says."),
        ("SAUDI ARABIA", (90, 60, 20),
         "Houthis say they hit biggest Saudi refinery",
         "Riyadh says drones were intercepted; no direct hit confirmed "
         "at Ras Tanura."),
        ("SPACE", (30, 70, 110),
         "Pakistan's first astronaut reaches Tiangong",
         "Muhammad Zeeshan Ali docks aboard Shenzhou-24, the station's "
         "first foreign visitor."),
        ("COLOMBIA", (20, 90, 60),
         "All hostages freed in Cartagena siege",
         "Security forces storm a supermarket after about 17 hours; "
         "shoppers and staff held."),
        ("NORTH KOREA", (110, 40, 90),
         "Pyongyang expels Swiss diplomat",
         "Envoy ordered out within 48 hours in a sanctions row, weeks "
         "after the office opened."),
    ]
    chip_font = font("LiberationSans-Bold.ttf", 17)
    story_head_font = font("LiberationSerif-Bold.ttf", 28)
    story_sum_font = font("LiberationSerif-Regular.ttf", 20)
    for index, (tag, colour, headline, summary) in enumerate(stories):
        if index:
            draw.line([(MARGIN, y - 5), (CONTENT_RIGHT, y - 5)],
                      fill=LIGHT_LINE, width=1)
        tag_w = int(draw.textlength(tag, font=chip_font)) + 20
        chip_top = y
        draw.rectangle([MARGIN, chip_top, MARGIN + tag_w, chip_top + 23],
                       fill=colour)
        draw.text((MARGIN + 10, chip_top + 11), tag, font=chip_font,
                  fill=(255, 255, 255), anchor="lm")
        head_x = MARGIN + tag_w + 14
        draw.text((head_x, chip_top + 11), headline,
                  font=story_head_font, fill=BLACK, anchor="lm")
        sum_top = chip_top + 27
        draw.text((MARGIN, sum_top), summary, font=story_sum_font,
                  fill=DARK_GREY, anchor="la")
        y = sum_top + line_height(draw, summary, story_sum_font) + 9

    # --- Footer ------------------------------------------------------------
    footer_font = font("LiberationSans-Regular.ttf", 17)
    footer_text = ("Stories first reported 25\u201326 November 2026  "
                   "\u2022  Reuters  \u2022  CNN  \u2022  BBC  \u2022  Nature")
    draw.text((W // 2, H - 48), footer_text, font=footer_font,
              fill=GREY, anchor="ma")
    draw.rectangle([MARGIN, H - 22, CONTENT_RIGHT, H - 19], fill=BLACK)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    img.save(OUT_PATH, format="PNG", optimize=True)
    print(OUT_PATH)


if __name__ == "__main__":
    main()
