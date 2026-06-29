from scraper.scraper import  WebScraper, BBVAScraperStrategy

if __name__ == "__main__":
    urls_to_scrape = [        
        "https://www.davibank.com/",
        "https://www.davibank.com/personas/tarjeta-de-credito",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-one",
        "https://www.davibank.com/personas/tarjeta-de-credito/lifemiles",
        "https://www.davibank.com/personas/tarjeta-de-credito/especializadas/cencosud",
        "https://www.davibank.com/personas/tarjeta-de-credito/terpel",
        "https://www.davibank.com/personas/tarjeta-de-credito/especializadas/pricesmart"
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-propias/cashback",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-propias/light",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-propias/infinite",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-propias/visa-signature",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-propias/platinum",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-propias/american-express-black",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-propias/mastercard-black",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-propias/oro",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-propias/clasica",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-propias/metal",
        "https://www.davibank.com/personas/cuentas-e-inversion",
        "https://www.davibank.com/personas/cuentas-e-inversion/cuentas-de-ahorro-transaccionales/cuenta-digital-cero",
        "https://www.davibank.com/personas/cuentas-e-inversion/cuentas-de-ahorro-transaccionales/cuenta-de-ahorros-cuenta-nomina",
        "https://www.davibank.com/personas/cuentas-e-inversion/cuentas-de-ahorro-transaccionales/cuenta-ahorro",
        "https://www.davibank.com/personas/cuentas-e-inversion/cuentas-de-ahorro-transaccionales/mesada-pensional",
        "https://www.davibank.com/personas/cuentas-e-inversion/cuenta-bolsillo",
        "https://www.davibank.com/cdt",
        "https://www.davibank.com/personas/cuentas-e-inversion/cuentas-corrientes/tradicional",
        "https://www.davibank.com/personas/hipotecario",
        "https://www.davibank.com/personas/hipotecario/compra-de-inmuebles/compra-de-vivienda",
        "https://www.davibank.com/personas/hipotecario/compra-de-inmuebles/compra-de-cartera",
        "https://www.davibank.com/personas/hipotecario/otras-lineas-con-garantia/libre-inversion",
        "https://www.davibank.com/personas/hipotecario/compra-de-inmuebles/vivienda-residentes-en-el-exterior",
        "https://www.davibank.com/personas/prestamos",
        "https://www.davibank.com/personas/prestamos/sin-garantia/compra-de-cartera-tc",
        "https://www.davibank.com/personas/prestamos/sin-garantia/consumo-unificacion-de-deudas",
        "https://www.davibank.com/personas/prestamos/sin-garantia/libre-inversion",
        "https://www.davibank.com/personas/prestamos/sin-garantia/credito-rotativo",
        "https://www.davibank.com/personas/seguros",
        "https://www.davibank.com/Personas/seguros/vida",
        "https://www.davibank.com/Personas/seguros/desempleo",
        "https://www.davibank.com/Personas/seguros/fraude",
        "https://www.davibank.com/personas/seguros/todo-riesgo-automoviles?_gl=1*1ychf2a*_gcl_au*MTM0MTA3MTMxMy4xNzgyNjc4NjE4*_ga*MTI1MzY3MTU4LjE3ODI2Nzg2MTg.*_ga_SDTSNW5N1C*czE3ODI3NTM1MTUkbzUkZzEkdDE3ODI3NTU0NjkkajUzJGwwJGgw*_ga_HBL945RPW6*czE3ODI3NTM1MTUkbzUkZzEkdDE3ODI3NTU0NzIkajUwJGwwJGgxMTI2Njg4MjQx",
        "https://www.davibank.com/personas/seguros/soat?_gl=1*dkeakm*_gcl_au*MTM0MTA3MTMxMy4xNzgyNjc4NjE4*_ga*MTI1MzY3MTU4LjE3ODI2Nzg2MTg.*_ga_SDTSNW5N1C*czE3ODI3NTM1MTUkbzUkZzEkdDE3ODI3NTU0NjUkajU3JGwwJGgw*_ga_HBL945RPW6*czE3ODI3NTM1MTUkbzUkZzEkdDE3ODI3NTU0NjYkajU2JGwwJGgxMTI2Njg4MjQx",
        "https://www.davibank.com/personas/seguros/asistencias",
        "https://www.davibank.com/personas/seguros/asistencias/premium",
        "https://www.davibank.com/personas/seguros/asistencias/integral",
        "https://www.davibank.com/personas/seguros/asistencias/mascotas",                        
        "https://www.davibank.com/personas/seguros/asistencias/hogar",
        "https://www.davibank.com/personas/seguros/asistencias/motos"

    ]

    # Instanciamos el contexto pasándole la estrategia concreta
    scraper = WebScraper(strategy=BBVAScraperStrategy())
    scraper.execute_and_save(urls_to_scrape)