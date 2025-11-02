{% if site.data.year-2026.photos %} 

<ul class="photos">
{% for photo in site.data.year-2026.photos %}
    <li class="photos__item">
        <img src="{{photo.image}}" alt="" class="photos__image">
    </li>
{% endfor %} 
</ul>

{% endif %}