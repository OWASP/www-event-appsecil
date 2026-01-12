{% if site.data.year-2026.photos %} 

<div class="gallery-wrapper">

<div class="gallery">
<ul class="gallery__slides">
{% for photo in site.data.year-2026.photos %}
    <li class="gallery__slide">
        <img src="{{photo.image}}" alt="">
        <div class="gallery__slide-textbox">
        {% if photo.title %} 
          <h3 class="gallery__slide-title">{{photo.title}}</h3>
        {% endif %}
        {% if photo.text %}
          <p class="gallery__slide-text">{{photo.text}}</p>
        {% endif %}
        </div>
    </li>
{% endfor %} 
</ul>

</div>
    <button type="button" class="gallery__btn gallery__btn_type_prev" aria-label="previous"></button>
    <button type="button" class="gallery__btn gallery__btn_type_next" aria-label="next"></button>
</div>

{% endif %}