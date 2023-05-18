var link = document.getElementById("theme-link");

var currTheme = link.getAttribute("href");

a = localStorage.getItem('Dark')

if (a == 'True') {
	$('.switch-btn').toggleClass('switch-on');
}



$('.switch-btn').click(function(){
  $(this).toggleClass('switch-on');
  if ($(this).hasClass('switch-on')) {
    $(this).trigger('on.switch');
  } else {
    $(this).trigger('off.switch');
  }
});

$('.switch-btn').on('on.switch', function(){
  currTheme = darkTheme;
  link.setAttribute("href", currTheme);
  localStorage.setItem('Dark', 'True');
});
$('.switch-btn').on('off.switch', function(){
  currTheme = '';
  link.setAttribute("href", currTheme);
  localStorage.setItem('Dark', 'False');
});

function viewSearch(){
  document.getElementById("popup-search").style.display = "block";
};

function closeSearch(){
  document.getElementById("popup-search").setAttribute('style', 'display:none !important');;
};

