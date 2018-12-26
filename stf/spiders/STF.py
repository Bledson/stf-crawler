# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
import time

dec_mono = pd.read_excel("decisoes_monocraticas_lista_presidente_2013.xlsx",
                         header=0, dtype={"Número": str})


class StfSpider(scrapy.Spider):
    name = "STF"
    allowed_domains = ["stf.jus.br"]

    def start_requests(self):
        start = time.time()
        ids = dec_mono.loc[:, ["Classe", "Número"]]
        for row in ids.itertuples():
            yield scrapy.Request(
                "http://stf.jus.br/portal/diarioJustica/listarDiarioJustica.asp"
                + "?tipoPesquisaDJ=AP&classe=" + row[1] + "&numero=" + row[2],
                callback=self.parse, meta={"id": row[1] + "-" + row[2]})
        end = time.time()
        print(end - start)

    def parse(self, response):
        decisoes = response.css(
            "div.boxDiarioJustica > div > a::attr(href)").extract()
        for dec in decisoes:
            yield response.follow(
                dec.replace("\r\n", "").lstrip(),
                callback=self.parse_decisao, meta={"id": response.meta["id"]})

    def parse_decisao(self, response):
        decisao = response.xpath(
            "//div[@id=\"abaAcompanhamentoConteudoResposta\"]/div"
        ).extract_first()
        yield {
            response.meta["id"]: decisao
        }
