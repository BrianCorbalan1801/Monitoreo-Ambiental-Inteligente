const { test, expect } = require("@playwright/test");

test.beforeEach(async ({ page }) => {
  await page.goto("http://10.56.2.71:8501/");
});

test.describe("Monitoreo Ambiental", () => {
  test("Carga de la aplicación", async ({ page }) => {
    await expect(
      page.getByText(
        "Los valores se actualizan automáticamente cada 30 segundos."
      )
    ).toBeVisible();
  });

  test("Las metricas existen", async ({ page }) => {
    await expect(page.getByText("🌡️ Temperatura")).toBeVisible();
    await expect(page.getByText("ºC")).toBeVisible();
    await expect(page.getByText("💧 Humedad")).toBeVisible();
    await expect(page.getByText("%")).toBeVisible();
    await expect(page.getByText("🌫 CO₂")).toBeVisible();
    await expect(page.getByText("ppm")).toBeVisible();
  });

  test("La Calidad del aire se muestra", async ({ page }) => {
    await expect(page.getByText("🟢 Bueno")).toBeVisible();
    await expect(page.getByText("🟠 Moderado")).toBeVisible();
    await expect(page.getByText("🔴 Malo")).toBeVisible();
  });
});
