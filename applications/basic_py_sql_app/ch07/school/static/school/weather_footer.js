/**
 * Footer hava durumu — Open-Meteo (CORS, API key gerekmez).
 * #weather-footer üzerinde data-latitude, data-longitude, data-city (opsiyonel)
 */
(function ($) {
  "use strict";

  function wmoTr(code) {
    var m = {
      0: "Açık",
      1: "Çoğunlukla açık",
      2: "Parçalı bulutlu",
      3: "Bulutlu",
      45: "Sis",
      48: "Sis",
      51: "Hafif çiseleme",
      53: "Çiseleme",
      55: "Yoğun çiseleme",
      61: "Hafif yağmur",
      63: "Yağmur",
      65: "Kuvvetli yağmur",
      71: "Hafif kar",
      73: "Kar",
      75: "Yoğun kar",
      80: "Sağanak",
      81: "Kuvvetli sağanak",
      82: "Şiddetli sağanak",
      95: "Gök gürültülü",
      96: "Dolu ile fırtına",
      99: "Şiddetli dolu",
    };
    return m[code] !== undefined ? m[code] : "Güncel";
  }

  function loadWeather($el) {
    var lat = parseFloat(String($el.attr("data-latitude")), 10);
    var lon = parseFloat(String($el.attr("data-longitude")), 10);
    var city = $el.attr("data-city") || "Konum";

    if (isNaN(lat) || isNaN(lon)) {
      $el.html('<span class="text-warning">Konum ayarlanmadı</span>');
      return;
    }

    var url =
      "https://api.open-meteo.com/v1/forecast?latitude=" +
      encodeURIComponent(lat) +
      "&longitude=" +
      encodeURIComponent(lon) +
      "&current=temperature_2m,relative_humidity_2m,weather_code" +
      "&timezone=" +
      encodeURIComponent("Europe/Istanbul");

    $.ajax({
      url: url,
      dataType: "json",
      timeout: 12000,
    })
      .done(function (data) {
        if (!data || !data.current) {
          $el.html('<span class="text-warning">Veri alınamadı</span>');
          return;
        }
        var c = data.current;
        var temp = c.temperature_2m;
        var hum = c.relative_humidity_2m;
        var code = c.weather_code;
        var label = wmoTr(code);
        var unit = (data.current_units && data.current_units.temperature_2m) || "°C";
        $el.html(
          '<span class="weather-line">' +
            '<strong>' +
            city +
            "</strong> · " +
            label +
            " · " +
            '<span class="text-primary fw-semibold">' +
            temp +
            unit +
            "</span>" +
            (hum != null ? " · nem %" + hum : "") +
            "</span>"
        );
      })
      .fail(function () {
        $el.html('<span class="text-danger">Hava durumu yüklenemedi</span>');
      });
  }

  $(function () {
    var $w = $("#weather-footer");
    if ($w.length) {
      loadWeather($w);
    }
  });
})(jQuery);
