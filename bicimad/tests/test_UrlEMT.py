import io

import pytest
from UrlEMT.UrlEMT import UrlEMT

get_links_test_cases = [
    (
        (
            '<ul class="ficheros"><li style="margin-bottom: 6px;margin-left: 12px;list-style-'
            'type: none;display: list-item;">\r\n  <img src="/Imagenes/Extensiones-de-archivo'
            's/zip_logo.aspx"/><a target="_blank" href="/getattachment/7a88cb04-9007-4520-88c'
            '5-a94c71a0b925/trips_23_02_February-csv.aspx" title="Datos de uso de febrero de '
            '2023. Nueva ventana" > Datos de uso de febrero de 2023</a>\r\n</li><li style="ma'
            'rgin-bottom: 6px;margin-left: 12px;list-style-type: none;display: list-item;">\r'
            '\n  <img src="/Imagenes/Extensiones-de-archivos/zip_logo.aspx"/><a target="_blan'
            'k" href="/getattachment/20b8509b-97a8-4831-b9d2-4900322e1714/trips_23_01_January'
            '-csv.aspx" title="Datos de uso de enero de 2023. Nueva ventana" > Datos de uso d'
            'e enero de 2023</a>\r\n</li><li style="margin-bottom: 6px;margin-left: 12px;list'
            '-style-type: none;display: list-item;">\r\n  <img src="/Imagenes/Extensiones-de-'
            'archivos/zip_logo.aspx"/><a target="_blank" href="/getattachment/5e3af49b-083b-4'
            'df5-a27a-961d9ea04049/202212-json.aspx" title="Situaci&#243;n estaciones bicimad'
            ' por d&#237;a y hora de Diciembrede 2022. Nueva ventana" > Situaci&#243;n estaci'
            'ones bicimad por d&#237;a y hora de Diciembrede 2022</a>\r\n</li><li style="marg'
            'in-bottom: 6px;margin-left: 12px;list-style-type: none;display: list-item;">\r\n'
            '  <img src="/Imagenes/Extensiones-de-archivos/zip_logo.aspx"/><a target="_blank"'
            ' href="/getattachment/34b933e4-4756-4fed-8d5b-2d44f7503ccc/trips_22_12_December-'
            'csv.aspx" title="Datos de uso de diciembre de 2022. Nueva ventana" > Datos de us'
            'o de diciembre de 2022</a>\r\n</li><li style="margin-bottom: 6px;margin-left: 12'
            'px;list-style-type: none;display: list-item;">\r\n  <img src="/Imagenes/Extensio'
            'nes-de-archivos/zip_logo.aspx"/><a target="_blank" href="/getattachment/7364d043'
            '-54a0-4f00-9137-337be1593b6c/202211-json.aspx" title="Situaci&#243;n estaciones '
            'bicimad por d&#237;a y hora de Noviembrede 2022. Nueva ventana" > Situaci&#243;n'
            " estaciones bicimad por d&#237;a y hora de Noviembrede 2022</a>\r\n</li><li styl"
            'e"="margin-bottom: 6px;margin-left: 12px;list-style-type: none;display: list-ite'
            'm;">\r\n  <img src="/Imagenes/Extensiones-de-archivos/zip_logo.aspx"/><a target='
            '"_blank" href="/getattachment/45f51cef-9296-4afe-b42e-d8d5bca3c548/trips_22_11_N'
            'ovember-csv.aspx" title="Datos de uso de noviembre de 2022. Nueva ventana" > Dat'
            'os de uso de noviembre de 2022</a>\r\n</li><li style="margin-bottom: 6px;margin-'
            'left: 12px;list-style-type: none;display: list-item;">\r\n  <img src="/Imagenes/'
            'Extensiones-de-archivos/zip_logo.aspx"/><a target="_blank" href="/getattachment/'
            'f1176321-b683-4cc1-8743-d38fefed0abd/202210-json.aspx" title="Situaci&#243;n est'
            'aciones bicimad por d&#237;a y hora de Octubre de 2022. Nueva ventana" >'
        ),
        {
            "23_02": (
                "https://opendata.emtmadrid.es/getattachment/7a88cb04-9007-4520-88c5-"
                "a94c71a0b925/trips_23_02_February-csv.aspx"
            ),
            "23_01": (
                "https://opendata.emtmadrid.es/getattachment/20b8509b-97a8-4831-b9d2-"
                "4900322e1714/trips_23_01_January-csv.aspx"
            ),
            "22_12": (
                "https://opendata.emtmadrid.es/getattachment/34b933e4-4756-4fed-8d5b-"
                "2d44f7503ccc/trips_22_12_December-csv.aspx"
            ),
            "22_11": (
                "https://opendata.emtmadrid.es/getattachment/45f51cef-9296-4afe-b42e-"
                "d8d5bca3c548/trips_22_11_November-csv.aspx"
            ),
        },
    ),
    (
        (
            'title="Datos de uso de Julio de 2017. Nueva ventana" > Datos de uso de Julio de 2017</'
            '>\r\n</li><li style="margin-bottom: 6px;margin-left: 12px;list-style-type: none;displa'
            ': list-item;">\r\n  <img src="/Imagenes/Extensiones-de-archivos/zip_logo.aspx"/><a tar'
            'et="_blank" href="/getattachment/c3a71f16-490a-42f9-b02e-384e08ceac2a/201706_Usage_Bic'
            'mad.aspx" title="Datos de uso de Junio de 2017. Nueva ventana" > Datos de uso de Junio'
            'de 2017</a>\r\n</li><li style="margin-bottom: 6px;margin-left: 12px;list-style-type: n'
            'ne;display: list-item;">\r\n  <img src="/Imagenes/Extensiones-de-archivos/zip_logo.asp'
            '"/><a target="_blank" href="/getattachment/11054216-35d1-4003-b76b-8421c4a46eb4/201705'
            'Usage_Bicimad.aspx" title="Datos de uso de Mayo de 2017. Nueva ventana" > Datos de uso'
            'de Mayo de 2017</a>\r\n</li><li style="margin-bottom: 6px;margin-left: 12px;list-style'
            'type: none;display: list-item;">\r\n  <img src="/Imagenes/Extensiones-de-archivos/zip_'
            'ogo.aspx"/><a target="_blank" href="/getattachment/8bb73c41-eab0-4e6a-ac92-80c8c68aacc'
            '/201704_Usage_Bicimad.aspx" title="Datos de uso de Abril de 2017. Nueva ventana" > Dat'
            's de uso de Abril de 2017</a>\r\n</li></ul>r\n</div>\n<div id="p_lt_ctl05_pageplacehol'
            'erHeader_p_lt_ctl01_repeaterContenidoGeneral_repItems_ctl00_ctl00_pnlMetadatos" class='
            'metadatos">\r\n\t\n'
        ),
        {},
    ),
    ("", {}),
    (None, TypeError),
    (12, TypeError),
    (True, TypeError),
    (45.5, TypeError),
    ("afwqgtq3g", {}),
]


@pytest.mark.parametrize("html, expected", get_links_test_cases)
def test_get_links(html, expected):
    url_object = UrlEMT()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            url_object.get_links(html)
    else:
        result = url_object.get_links(html)
        assert result == expected


get_file_name_from_url_test_cases = [
    (
        (
            "https://opendata.emtmadrid.es/getattachment/7a88cb04-9007-4520-88c5-a94c71a0b925/trips"
            "_23_02_February-csv.aspx"
        ),
        "trips_23_02_February",
    ),
    ("", ""),
    ("testing get_file_name_from_url function", ""),
    (None, TypeError),
    (1, TypeError),
    (3.3, TypeError),
    ([], TypeError),
]


@pytest.mark.parametrize("url, expected", get_file_name_from_url_test_cases)
def test_get_file_name_from_url(url, expected):
    url_object = UrlEMT()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            url_object.get_file_name_from_url(url)
    else:
        result = url_object.get_file_name_from_url(url)
        assert result == expected


get_url_test_cases = [
    (2, 21, ValueError),
    (
        9,
        22,
        (
            "https://opendata.emtmadrid.es/getattachment/8d9ed4a4-6770-4307-92f8-6e34b6006eea/"
            "trips_22_09_September-csv.aspx"
        ),
    ),
    (15, 28, ValueError),
    (11, 27, ValueError),
    (-1, 22, ValueError),
    (None, 21, TypeError),
    ("3", "21", TypeError),
    (3, "21", TypeError),
    ([3, 22], None, TypeError),
]


@pytest.mark.parametrize("month, year, expected", get_url_test_cases)
def test_get_url(month, year, expected):
    url_object = UrlEMT()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            url_object.get_url(month, year)
    else:
        result = url_object.get_url(month, year)
        assert result == expected


get_csv_test_cases = [
    (3, 22, io.StringIO),
    (3, 21, ValueError),
    ("3", 21, TypeError),
    (133, 21, ValueError),
]


@pytest.mark.parametrize("month, year, expected", get_csv_test_cases)
def test_get_csv(month, year, expected):
    url_object = UrlEMT()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            url_object.get_csv(month, year)
    else:
        result = url_object.get_csv(month, year)
        assert isinstance(result, io.StringIO)
