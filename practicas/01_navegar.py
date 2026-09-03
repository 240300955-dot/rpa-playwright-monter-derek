"""Práctica 1: abre el portal y recupera información de la página."""

from playwright.sync_api import sync_playwright

# Centralizar la URL evita repetir valores de configuración en el flujo.
PORTAL = "http://127.0.0.1:8000"

# El administrador de contexto inicia y detiene Playwright automáticamente.
with sync_playwright() as playwright:
    # TODO 1: iniciar Chromium en modo visible y con slow_mo=300.
    browser = playwright.chromium.launch(headless=False, slow_mo=300)

    # TODO 2: crear una página y navegar a PORTAL.
    page = browser.new_page()
    page.goto(PORTAL)

    # TODO 3: imprimir el título y la URL.
    print("Título:", page.title())
    print("URL:", page.url)

    # TODO 4: cerrar el navegador.
    browser.close()
