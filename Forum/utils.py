import re
from bleach.sanitizer import Cleaner

def convert_media_links_to_embed(text):
    # Regex for YouTube and Spotify URLs
    patterns = {
        'youtube': (
            re.compile(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)(?P<id>[a-zA-Z0-9_-]{11})'),
            '<div class="responsive-iframe"><iframe src="https://www.youtube.com/embed/{id}" frameborder="0" allowfullscreen></iframe></div>',
        ),
        'spotify': (
            re.compile(r'https?://open.spotify.com/(?P<type>track|playlist|album|artist)/(?P<id>[a-zA-Z0-9]+)'),
            '<div class="responsive-iframe"><iframe src="https://open.spotify.com/embed/{type}/{id}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe></div>',
        ),

    }

    def replace_with_embed(match, platform):
        return patterns[platform][1].format(**match.groupdict())

    for platform, (pattern, _) in patterns.items():
        text = pattern.sub(lambda match: replace_with_embed(match, platform), text)

    return text

def clean_html(text):
    # Configuration for bleach
    allowed_tags = ['div', 'iframe']
    allowed_attributes = {'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen', 'allowtransparency', 'allow'], 'div': ['class']}
    cleaner = Cleaner(tags=allowed_tags, attributes=allowed_attributes, strip=True)
    return cleaner.clean(text)
