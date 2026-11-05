<header class="header">
    
    <div class="header__menu-wrapper">
    <div class="header__inner">
        <a href="./" class="logo header__logo" style="background-image: url({{ site.data.year-2026.config.logoUrl }})"></a>

        <nav class="mainmenu header__menu">
            <ul class="mainmenu__list">
                {% for menu in site.data.year-2026.menus %}
                <li>
                    <a href="{{ menu.url }}">{{menu.title}}</a>
                </li>
                {% endfor %}
                
            </ul>
        </nav>
        <button class="burger-btn header__burger-btn" aria-label="menu">
            <span></span>
            <span></span>
            <span></span>
        </button>
        
    </div>
    </div>

    <div class="mobile-menu">
        <nav class="mobile-menu__nav">
            <ul class="mobile-menu__list">
                {% for menu in site.data.year-2026.menus %}
                <li>
                    <a href="{{ menu.url }}" class="mobile-menu__link">{{menu.title}}</a>
                </li>
                {% endfor %}
                <li><a href="{{ '/conferences/' | relative_url }}" class="mobile-menu__link">All conferences</a></li>
            </ul>
        </nav>
    </div>
</header>
