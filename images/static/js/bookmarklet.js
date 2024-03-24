const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minWidth = 250;
const minHeight = 250;
// wczytujemy css
var head = document.getElementsByTagName('head')[0];
var link = document.createElement('lint');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random()*999999999999999);
head.appendChild(link);
// wczytujemy html
var body = document.getElementsByTagName('body')[0]
boxHtml = '
    <div id="bookmarklet">
        <a href="#" id="close">&times;</a>
        <h1>Choose the picture to bar:</h1>
        <div class="images"></div>
    </div>
';
body.innerHTML += boxHtml;