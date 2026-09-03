"""Reto: consulta, valida, descarga y conserva evidencia.
Adapta el flujo para procesar dos casos consecutivos (válido + inexistente).
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PORTAL = "http://127.0.0.1:8000"
EVIDENCIAS = ROOT / "evidencias"
DESCARGAS = ROOT / "descargas"
EVIDENCIAS.mkdir(exist_ok=True)
DESCARGAS.mkdir(exist_ok=True)

# Casos obligatorios según la guía de entrega
CASOS = ["IAI0002", "IAI9999"]

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page()

    try:
        page.goto(PORTAL)

        for matricula in CASOS:
            print(f"\n--- Procesando matrícula: {matricula} ---")

            # 1 y 2: completar campo y pulsar Buscar
            page.get_by_label("Matrícula").fill(matricula)
            page.get_by_role("button", name="Buscar").click()

            # 3: leer el resultado
            panel = page.get_by_test_id("result-panel")
            texto = panel.inner_text().strip()
            print("Texto del panel:", texto)

            # 4: clasificar
            texto_lower = texto.lower()
            if "no encontrado" in texto_lower or "no existe" in texto_lower or "inexistente" in texto_lower:
                clasificacion = "Excepción de negocio: matrícula inexistente"
                # 6: captura de excepción
                page.screenshot(path=str(EVIDENCIAS / "excepcion-negocio.png"), full_page=True)
                print(f"{matricula} -> {clasificacion}")
            else:
                clasificacion = "Éxito"
                # 5: descargar solo si es válida
                with page.expect_download() as download_info:
                    page.get_by_role("button", name="Descargar kárdex").click()
                download = download_info.value
                ruta_pdf = DESCARGAS / f"kardex-{matricula}.pdf"
                download.save_as(ruta_pdf)

                # 6: captura de éxito
                page.screenshot(path=str(EVIDENCIAS / "consulta-exitosa.png"), full_page=True)
                print(f"{matricula} -> {clasificacion} -> {ruta_pdf}")

        print("\n=== Ejecución completada ===")
      

    except Exception as error:
        print("Error técnico:", error)
        page.screenshot(path=str(EVIDENCIAS / f"error_tecnico.png"), full_page=True)

    finally:
        browser.close()
    
        
