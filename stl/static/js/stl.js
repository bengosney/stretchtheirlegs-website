!function(){var e=function(e){if(window.matchMedia&&!window.matchMedia("(prefers-reduced-motion: reduce)").matches){var n=document.createElement("script");n.src=e.url,n.async=!0,n.defer=!0,n.onload=e.onload,document.head.appendChild(n),document.body.classList.add("effect-".concat(e.name))}};(function(){var e,n=document.createElement("link");n.rel="prefetch",n.onload=function(){return n.removeAttribute("href")},document.head.appendChild(n);document.querySelectorAll("a[href]").forEach((function(t){t.origin==window.location.origin&&(["mouseover","touchstart"].forEach((function(o){t.addEventListener(o,(function(){return function(t){clearTimeout(e),e=setTimeout((function(){return n.href=t.href}),50)}(t)}),!0)})),["mouseout","touchend"].forEach((function(e){t.addEventListener(e,(function(){return n.removeAttribute("href")}),!0)})))}))})();var n,t=window;t.loadEffect=e,null!=(n=t.effect)&&"url"in n&&"name"in n&&e(t.effect)}();
//# sourceMappingURL=stl.js.map
