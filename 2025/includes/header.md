<header class="header">
    <div class="header__inner">
            <a href="{{ './' | relative_url }}" class="logo header__logo" style="background-image: url({{ site.data.year-2025.config.logoUrl }})"></a>

        <nav class="mainmenu header__menu">
            <ul>
                {% for menu in site.data.year-2025.menus %}
                <li>
                    <a href="{{ menu.url }}">{{menu.title}}</a>
                </li>
                {% endfor %}
            </ul>
        </nav>
    </div>
</header>
