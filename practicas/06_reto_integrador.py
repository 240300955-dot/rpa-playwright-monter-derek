"""Reto: consulta, valida, descarga y conserva evidencia."""

from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PORTAL = "http://127.0.0.1:8000"
MATRICULA = "IAI0003"
EVIDENCIAS = ROOT / "evidencias"
DESCARGAS = ROOT / "descargas"
EVIDENCIAS.mkdir(exist_ok=True)
DESCARGAS.mkdir(exist_ok=True)

print("=== INICIANDO RETO INTEGRADOR ===")

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=400)
    page = browser.new_page()

    try:
        print("1. Navegando al portal...")
        page.goto(PORTAL)
        print("   Portal cargado")

        print("2. Llenando matrícula...")
        page.get_by_label("Matrícula").fill(MATRICULA)
        page.get_by_role("button", name="Buscar").click()
        print("   Búsqueda realizada")

        print("3. Leyendo panel de resultados...")
        panel = page.get_by_test_id("result-panel")
        texto = panel.inner_text()
        print("   Texto del panel:")
        print(texto)

        if "no encontrado" in texto.lower() or "no existe" in texto.lower():
            print("→ EXCEPCIÓN DE NEGOCIO")
            page.screenshot(path=str(EVIDENCIAS / f"excepcion_{MATRICULA}.png"), full_page=True)
        else:
            print("→ ÉXITO - Descargando kárdex...")
            with page.expect_download() as download_info:
                page.get_by_role("button", name="Descargar kárdex").click()
            download = download_info.value
            ruta = DESCARGAS / f"kardex-{MATRICULA}.pdf"
            download.save_as(ruta)
            page.screenshot(path=str(EVIDENCIAS / f"exito_{MATRICULA}.png"), full_page=True)
            print("   PDF guardado en:", ruta)

        print("Esperando 6 segundos...")
        page.wait_for_timeout(6000)

    except Exception as e:
        print("ERROR:", e)
        try:
            page.screenshot(path=str(EVIDENCIAS / f"error_{MATRICULA}.png"), full_page=True)
        except:
            pass

    finally:
        browser.close()
        print("=== FIN ===")
    
        
