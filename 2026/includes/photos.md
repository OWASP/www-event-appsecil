{% if site.data.year-2025.photos %} 

<ul class="gallery__slides">
{% for photo in site.data.year-2025.photos %}
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
<div class="gallery__nav">
    <button type="button" class="button button_type_main gallery__btn gallery__btn_type_prev">Back</button>
    <button type="button" class="button button_type_main gallery__btn gallery__btn_type_next">Next</button>
</div>

{% endif %}