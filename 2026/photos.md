---
layout: custom-2026
title: Photo album
startSection: lblue
---

<section class="page-section page-section_lblue">
<div class="page-section__inner">
<div class="text text_type_narrow" markdown="1">

# AppSec Israel 2026 photo album

{% assign album_files = site.static_files | where_exp: 'file', "file.path contains '/assets/img/2026/album/'" | sort: 'path' %}
{% assign image_extensions = '.jpg,.jpeg,.png,.gif,.webp,.avif' | split: ',' %}
{% assign photo_count = 0 %}
{% capture album_items %}
{% for photo in album_files %}
{% assign extension = photo.extname | downcase %}
{% if image_extensions contains extension %}
{% assign photo_count = photo_count | plus: 1 %}
{% assign description = photo.name | remove: photo.extname | replace: '_', ' ' | replace: '-', ' ' %}
<li>
  <a class="photo-album__link" href="{{ photo.path | relative_url | uri_escape | escape }}" aria-label="Open photo {{ photo_count }}: {{ description | escape }}">
    <img src="{{ photo.path | relative_url | uri_escape | escape }}" alt="{{ description | escape }}" loading="lazy" decoding="async">
  </a>
</li>
{% endif %}
{% endfor %}
{% endcapture %}
{% if photo_count > 0 %}
Select a thumbnail to view the full photo. Use the arrows to browse, or press Escape to close.
{% else %}
Photos from AppSec Israel 2026 will be added here soon. Check back after the event!
{% endif %}

</div>
{% if photo_count > 0 %}
<ul class="photo-album" aria-label="Conference photos">
{{ album_items }}
</ul>
{% endif %}
</div>
</section>
