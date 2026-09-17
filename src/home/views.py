from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.contrib.staticfiles import finders
from common.utils import fetch_quote

from favorites.models import Favorite
from home.models import SharedQuote

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

# List of tags can be a module-level constant if you like
all_tags = [
    "Anxiety","Change","Choice","Confidence","Courage","Death","Dreams",
    "Excellence","Failure","Fairness","Fear","Forgiveness","Freedom",
    "Future","Happiness","Inspiration","Kindness","Leadership","Life",
    "Living","Love","Pain","Past","Success","Time","Today","Truth","Work"
]

def index(request):
    """
    Main page view. If GET parameters include 'keyword' or 'author',
    fetch a quote and pass it to the template.
    """
    popular_tags = all_tags[:8]
    keyword = request.GET.get('keyword')
    author = request.GET.get('author')
    quote = fetch_quote(keyword=keyword, author=author)

    is_favorited = False

    if request.user.is_authenticated and quote:
        is_favorited = Favorite.objects.filter(
            user=request.user,
            quote_text=quote.get('q'),
            author=quote.get('a')
        ).exists()

    context = {
        'tags': popular_tags,
        'quote': quote,
        'is_favorited': is_favorited,
        'error_message': None if quote else ("No quote found matching your criteria" if keyword or author else None)
    }

    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        context["user_favorites"] = {
            (f.quote_text, f.author) for f in favorites
        }
    else:
        context["user_favorites"] = set()

    return render(request, "home/index.html", context)


def quote_partial(request):
    keyword = request.GET.get("keyword")
    quotes = fetch_quote(keyword=keyword, limit=10)

    return render(
        request, 
        "home/partials/_quote_card.html",
        {
            "quote": quotes[0] if quotes else None, 
            "quotes_json": quotes,
            "active_tag": keyword,
            "error_message": None if quotes else "No quote found"
        },
    )


def inspire(request):
    quote = fetch_quote(use_cache=False)  # Force fetch a new quote, bypassing cache

    return render(
        request,
        "home/partials/_quote_card.html",
        {
            "quote": quote,
            "error_message": None if quote else "No quote found",
        },
    )


def _wrap_text(draw, text, font, max_width):
    """Word-wrap text to fit max_width, measuring actual rendered width per line."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _fit_quote_font(draw, text, font_path, max_width, max_height, start_size=76, min_size=32):
    """Shrink font size until the wrapped quote fits the available box."""
    size = start_size
    while size >= min_size:
        font = ImageFont.truetype(font_path, size)
        lines = _wrap_text(draw, text, font, max_width)
        line_height = int(size * 1.35)
        if line_height * len(lines) <= max_height:
            return font, lines, line_height
        size -= 4
    font = ImageFont.truetype(font_path, min_size)
    lines = _wrap_text(draw, text, font, max_width)
    return font, lines, int(min_size * 1.35)


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def share_card_image(request):
    """
    Renders a shareable 1080x1350 (4:5) PNG quote card server-side, so the
    result is deterministic across every device/browser (unlike a
    client-side canvas approach) and reusable for Stage 3's OG-image
    previews on public quote links (see quote_detail below).
    """
    quote_text = request.GET.get("q", "").strip()
    author = request.GET.get("a", "").strip()

    if not quote_text:
        return HttpResponseBadRequest("Missing quote text")

    W, H = 1080, 1350

    # Base diagonal gradient, matching the live card's dark surface tones
    top_color = _hex_to_rgb("#101d22")
    bottom_color = _hex_to_rgb("#192d33")
    base = Image.new("RGB", (W, H))
    base_draw = ImageDraw.Draw(base)
    for y in range(H):
        t = y / H
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        base_draw.line([(0, y), (W, y)], fill=(r, g, b))
    base = base.convert("RGBA")

    # Soft blurred blobs, same colors/composition family as quote-card-bg.svg,
    # rebalanced for the 4:5 canvas so the bottom third isn't left flat
    blobs = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    blob_draw = ImageDraw.Draw(blobs)

    def blob(cx, cy, radius, hex_color, opacity):
        rgb = _hex_to_rgb(hex_color)
        blob_draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            fill=rgb + (int(255 * opacity),),
        )

    blob(220, 240, 340, "#13b6ec", 0.55)
    blob(900, 175, 270, "#233f48", 0.6)
    blob(860, 1150, 420, "#f6a35b", 0.35)
    blob(190, 1180, 340, "#13b6ec", 0.3)
    blob(560, 640, 320, "#f6f8f8", 0.12)

    blobs = blobs.filter(ImageFilter.GaussianBlur(100))
    canvas = Image.alpha_composite(base, blobs)

    # Bottom gradient fade for text legibility, echoing the live card's overlay
    fade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fade_draw = ImageDraw.Draw(fade)
    surface_dark = _hex_to_rgb("#192d33")
    for y in range(H):
        t = max(0, (y - H * 0.35) / (H * 0.65))
        fade_draw.line([(0, y), (W, y)], fill=surface_dark + (int(200 * t),))
    canvas = Image.alpha_composite(canvas, fade)

    draw = ImageDraw.Draw(canvas)

    bold_font_path = finders.find("home/fonts/Inter-Bold.ttf")
    regular_font_path = finders.find("home/fonts/Inter-Regular.ttf")

    margin = 90
    max_text_width = W - (margin * 2)

    # Height budget tightened from an earlier 0.55 to 0.42 — the original
    # value only shrank text that would actually overflow, so a 6-line
    # quote rendered near max size and looked overly dense. 0.42 forces
    # longer quotes to scale down for better visual balance.
    quote_font, lines, line_height = _fit_quote_font(
        draw, quote_text, bold_font_path, max_text_width, H * 0.42
    )

    author_font = ImageFont.truetype(regular_font_path, 34)
    author_text = f"— {author}" if author else ""
    author_height = 50 if author_text else 0

    block_height = (line_height * len(lines)) + author_height
    start_y = (H - block_height) // 2

    y = start_y
    for line in lines:
        draw.text((margin, y), line, font=quote_font, fill=(255, 255, 255, 255))
        y += line_height

    if author_text:
        draw.text(
            (margin, y + 16),
            author_text,
            font=author_font,
            fill=(255, 255, 255, 180),
        )

    # Wordmark + domain, bottom-left. The domain line makes the link travel
    # with the image itself (like a TikTok watermark) so it survives even
    # when a caption/URL sent alongside the share doesn't.
    wordmark_font = ImageFont.truetype(bold_font_path, 30)
    domain_font = ImageFont.truetype(regular_font_path, 22)
    bar_x = margin
    bar_y = H - 118
    draw.rounded_rectangle(
        [bar_x, bar_y, bar_x + 10, bar_y + 34],
        radius=3,
        fill=_hex_to_rgb("#13b6ec"),
    )
    draw.text(
        (bar_x + 24, bar_y - 2),
        "Inspirobot",
        font=wordmark_font,
        fill=(255, 255, 255, 255),
    )
    draw.text(
        (bar_x + 24, bar_y + 38),
        "inspirobot.onrender.com",
        font=domain_font,
        fill=(255, 255, 255, 160),
    )

    buffer = io.BytesIO()
    canvas.convert("RGB").save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def share_link(request):
    """
    Lazily creates (or reuses) a permalink for a specific quote+author,
    the first time it's actually shared — not pre-seeded from ZenQuotes.
    Returns JSON with the absolute public URL for that quote.
    """
    quote_text = request.GET.get("q", "").strip()
    author = request.GET.get("a", "").strip()

    if not quote_text:
        return JsonResponse({"error": "Missing quote text"}, status=400)

    shared, _ = SharedQuote.objects.get_or_create(
        quote_text=quote_text,
        author=author,
    )

    url = request.build_absolute_uri(
        reverse("home:quote-detail", args=[shared.short_id])
    )
    return JsonResponse({"url": url})


def quote_detail(request, short_id):
    """
    Public page for a shared quote. Renders proper Open Graph tags
    pointing at share_card_image above, so link previews (WhatsApp,
    Twitter, etc.) show the same branded card that was actually shared.
    """
    shared = get_object_or_404(SharedQuote, short_id=short_id)

    og_image_url = request.build_absolute_uri(
        f"{reverse('home:share-card')}?q={shared.quote_text}&a={shared.author}"
    )

    return render(
        request,
        "home/quote_detail.html",
        {
            "shared": shared,
            "og_image_url": og_image_url,
        },
    )
