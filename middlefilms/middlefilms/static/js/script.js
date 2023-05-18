link = document.getElementById("theme-link");

currTheme = link.getAttribute("href");

a = localStorage.getItem('Dark')

switch_btn = $('.switch-btn')

if (a === 'True') {
    switch_btn.toggleClass('switch-on');
}


switch_btn.click(function () {
    $(this).toggleClass('switch-on');
    if ($(this).hasClass('switch-on')) {
        $(this).trigger('on.switch');
    } else {
        $(this).trigger('off.switch');
    }
}).on('on.switch', function () {
    let currTheme = darkTheme;
    link.setAttribute("href", currTheme);
    localStorage.setItem('Dark', 'True');
}).on('off.switch', function () {
    let currTheme = '';
    link.setAttribute("href", currTheme);
    localStorage.setItem('Dark', 'False');
});

$('.nav-item a.nav-link').each(function () {
    let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
    let link = this.href;
    if (location === link) {
        $(this).parent().addClass('menu-active');
    }
});

$('.main-filter select options').each(function () {
    let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
    let link = this.href;
    if (location === link) {
        $(this).parent().addClass('menu-active');
    }
});
$(document).ready(function (){
    update_rating();
})

function set_rating(film_id, rating) {
    $.ajax({
        method: 'get',
        url: `/rating/${film_id}?rating=${rating}`,
        dataType: 'json',
        success: function (response) {
            rating = response.your_rating;
            avg_rating = String(response.avg_rating['rating__avg'].toFixed(1)).replace(".", ",")
            const div_your = document.querySelector(".your-rating");
            const rating_number = document.querySelector("#rating-number");
            div_your.innerHTML = rating;
            rating_number.innerHTML = avg_rating;
            update_rating();
        },
        error: function (response) {
            // предупредим об ошибке
            console.log(response.responseJSON.errors)
        },
        complete: function (response) {
            // предупредим об ошибке
            console.log('complete')
        }
    })
}

function get_ajax(url, type) {
    // создаем AJAX-вызов
    $.ajax({
        data: $(this).serialize(),
        method: 'get',
        url: url,
        dataType: 'json',
        success: function (response) {
            let html = ''
            let poster;
            let selector = '.chap-obj-' + type;
            const div = document.querySelector(selector);
            for (let film in response.films) {
                poster = response.films[film].poster
                html += '<div class="item col-lg-2 col-xl-2 col-md-3 col-sm-4 col-6">\n' +
                    `                            <a href=\' ${response.films[film].slug} \'>\n` +
                    '                                <div class="item-img"\n' +
                    `                                     style="background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, #000000 100%), url(\' /media/${response.films[film].poster} \') center no-repeat;background-size: cover;">\n` +
                    '                                    <div class="item-text">\n' +
                    `                                        <div class="item-title">${response.films[film].title} (${response.films[film].year})</div>\n` +
                    '                                        <div class="item-rating">\n' +
                    `                                            <div class="item-kp"><span class="kp">KP</span> ${String(response.films[film].rating_kp.toFixed(1)).replace(".", ",")}</div>\n` +
                    `                                            <div class="item-imdb"><span class="imdb">IMDB</span> ${String(response.films[film].rating_imdb.toFixed(1)).replace(".", ",")}\n` +
                    '                                            </div>\n' +
                    '                                        </div>\n' +
                    '                                    </div>\n' +
                    '                                </div>\n' +
                    '                                <div class="play-hov">\n' +
                    '                                    <i class="bi bi-play-circle-fill"></i>\n' +
                    '                                </div>\n' +
                    '                            </a>\n' +
                    '                        </div>'
            }
            div.innerHTML = html;
        },
        error: function (response) {
            // предупредим об ошибке
            console.log(response.responseJSON.errors)
        },
        complete: function (response) {
            // предупредим об ошибке
            console.log('complete')
        }
    });
    return false;
}


$('#film-popular').click(function () {
    get_ajax('/order-films?type=Фильм&order=-views', 'films');
    $(this).addClass('sort-active');
    $('#film-rating').removeClass('sort-active');
    $('#film-last').removeClass('sort-active');
});
$('#film-last').click(function () {
    get_ajax('/order-films?type=Фильм&order=-premiere', 'films');
    $(this).addClass('sort-active');
    $('#film-rating').removeClass('sort-active');
    $('#film-popular').removeClass('sort-active');
});
$('#film-rating').click(function () {
    get_ajax('/order-films?type=Фильм&order=-rating_kp', 'films');
    $(this).addClass('sort-active');
    $('#film-popular').removeClass('sort-active');
    $('#film-last').removeClass('sort-active');
});

$('#serial-popular').click(function () {
    get_ajax('/order-films?type=Сериал&order=-views', 'serials');
    $(this).addClass('sort-active');
    $('#serial-rating').removeClass('sort-active');
    $('#serial-last').removeClass('sort-active');
});
$('#serial-last').click(function () {
    get_ajax('/order-films?type=Сериал&order=-premiere', 'serials');
    $(this).addClass('sort-active');
    $('#serial-rating').removeClass('sort-active');
    $('#serial-popular').removeClass('sort-active');
});
$('#serial-rating').click(function () {
    get_ajax('/order-films?type=Сериал&order=-rating_kp', 'serials');
    $(this).addClass('sort-active');
    $('#serial-popular').removeClass('sort-active');
    $('#serial-last').removeClass('sort-active');
});

$('#mult-popular').click(function () {
    get_ajax('/order-films?type=Мультфильм&order=-views', 'mults');
    $(this).addClass('sort-active');
    $('#mult-rating').removeClass('sort-active');
    $('#mult-last').removeClass('sort-active');
});
$('#mult-last').click(function () {
    get_ajax('/order-films?type=Мультфильм&order=-premiere', 'mults');
    $(this).addClass('sort-active');
    $('#mult-rating').removeClass('sort-active');
    $('#mult-popular').removeClass('sort-active');
});
$('#mult-rating').click(function () {
    get_ajax('/order-films?type=Мультфильм&order=-rating_kp', 'mults');
    $(this).addClass('sort-active');
    $('#mult-popular').removeClass('sort-active');
    $('#mult-last').removeClass('sort-active');
});


function viewSearch() {
    document.getElementById("popup-search").style.display = "block";
    document.getElementById("search_input").focus();
}

function closeSearch() {
    document.getElementById("popup-search").setAttribute('style', 'display:none !important');
}
function update_rating() {
    rating = Math.round(parseFloat(document.getElementById('rating-number').innerHTML));

    if (rating === 5) {
        document.getElementById('star-5').style.color = "gold";
        document.getElementById('star-4').style.color = "gold";
        document.getElementById('star-3').style.color = "gold";
        document.getElementById('star-2').style.color = "gold";
        document.getElementById('star-1').style.color = "gold";

    } else if (rating === 4) {
        document.getElementById('star-5').style.color = "white";
        document.getElementById('star-4').style.color = "gold";
        document.getElementById('star-3').style.color = "gold";
        document.getElementById('star-2').style.color = "gold";
        document.getElementById('star-1').style.color = "gold";

    } else if (rating === 3) {
        document.getElementById('star-5').style.color = "white";
        document.getElementById('star-4').style.color = "white";
        document.getElementById('star-3').style.color = "gold";
        document.getElementById('star-2').style.color = "gold";
        document.getElementById('star-1').style.color = "gold";
    } else if (rating === 2) {
        document.getElementById('star-5').style.color = "white";
        document.getElementById('star-4').style.color = "white";
        document.getElementById('star-3').style.color = "white";
        document.getElementById('star-2').style.color = "gold";
        document.getElementById('star-1').style.color = "gold";
    } else if (rating === 1) {
        document.getElementById('star-5').style.color = "white";
        document.getElementById('star-4').style.color = "white";
        document.getElementById('star-3').style.color = "white";
        document.getElementById('star-2').style.color = "white";
        document.getElementById('star-1').style.color = "gold";
    }
}

function show_player2() {
    document.getElementById("player1").style.display = "none";
    document.getElementById("player2").style.display = "block";
    $('#show_player2').toggleClass('active');
    $('#show_player1').removeClass('active');
}

function show_player1() {
    document.getElementById("player2").style.display = "none";
    document.getElementById("player1").style.marginBottom = '0';
    document.getElementById("player1").style.display = "block";
    $('#show_player1').toggleClass('active');
    $('#show_player2').removeClass('active');
}

