'use strict';
angular.module("ngLocale", [], ["$provide", function($provide) {
var PLURAL_CATEGORY = {ZERO: "zero", ONE: "one", TWO: "two", FEW: "few", MANY: "many", OTHER: "other"};
function getDecimals(n) {
  n = n + '';
  var i = n.indexOf('.');
  return (i == -1) ? 0 : n.length - i - 1;
}

function getVF(n, opt_precision) {
  var v = opt_precision;

  if (undefined === v) {
    v = Math.min(getDecimals(n), 3);
  }

  var base = Math.pow(10, v);
  var f = ((n * base) | 0) % base;
  return {v: v, f: f};
}

$provide.value("$locale", {
  "DATETIME_FORMATS": {
    "AMPMS": [
      "AM",
      "PM"
    ],
    "DAY": [
      "Sabbiiti",
      "Balaza",
      "Lwakubiri",
      "Lwakusatu",
      "Lwakuna",
      "Lwakutaano",
      "Lwamukaaga"
    ],
    "ERANAMES": [
      "Kulisito nga tannaza",
      "Bukya Kulisito Azaal"
    ],
    "ERAS": [
      "BC",
      "AD"
    ],
    "MONTH": [
      "Janwaliyo",
      "Febwaliyo",
      "Marisi",
      "Apuli",
      "Maayi",
      "Juuni",
      "Julaayi",
      "Agusito",
      "Sebuttemba",
      "Okitobba",
      "Novemba",
      "Desemba"
    ],
    "SHORTDAY": [
      "Sab",
      "Bal",
      "Lw2",
      "Lw3",
      "Lw4",
      "Lw5",
      "Lw6"
    ],
    "SHORTMONTH": [
      "Jan",
      "Feb",
      "Mar",
      "Apu",
      "Maa",
      "Juu",
      "Jul",
      "Agu",
      "Seb",
      "Oki",
      "Nov",
      "Des"
    ],
    "fullDate": "EEEE, d MMMM y",
    "longDate": "d MMMM y",
    "medium": "d MMM y h:mm:ss a",
    "mediumDate": "d MMM y",
    "mediumTime": "h:mm:ss a",
    "short": "dd/MM/y h:mm a",
    "shortDate": "dd/MM/y",
    "shortTime": "h:mm a"
  },
  "NUMBER_FORMATS": {
    "CURRENCY_SYM": "UGX",
    "DECIMAL_SEP": ".",
    "GROUP_SEP": ",",
    "PATTERNS": [
      {
        "gSize": 3,
        "lgSize": 3,
        "maxFrac": 3,
        "minFrac": 0,
        "minInt": 1,
        "negPre": "-",
        "negSuf": "",
        "posPre": "",
        "posSuf": ""
      },
      {
        "gSize": 3,
        "lgSize": 3,
        "maxFrac": 2,
        "minFrac": 2,
        "minInt": 1,
        "negPre": "-",
        "negSuf": "\u00a4",
        "posPre": "",
        "posSuf": "\u00a4"
      }
    ]
  },
  "id": "lg",
  "pluralCat": function(n, opt_precision) {  var i = n | 0;  var vf = getVF(n, opt_precision);  if (i == 1 && vf.v == 0) {    return PLURAL_CATEGORY.ONE;  }  return PLURAL_CATEGORY.OTHER;}
});
}]);
