const { test, expect } = require("@playwright/test");

test.beforeEach(async ({ page }) => {
  await page.goto("http://10.56.2.71:8501/");
});

test.describe("Registros Historicos", () => {
  test("Carga la seccion de registros", async ({ page }) => {
    await page.getByRole("heading", { name: "Registros historicos" }).click();
    await page
      .getByRole("heading", { name: "Datos de ETEC entre 2025-11-" })
      .click();
  });

  test("El panel se muestra", async ({ page }) => {
    await expect(page.getByRole("heading", { name: "Filtros" })).toBeVisible();
    await expect(page.getByText("Selecciona la zona:")).toBeVisible();
    await expect(page.getByText("Desde:")).toBeVisible();
    await expect(page.getByText("Hasta:")).toBeVisible();
  });

  test("Las estadisticas se muestran", async ({ page }) => {
    await expect(
      page.getByRole("heading", { name: "📊 Estadísticas del período" })
    ).toBeVisible();
    await expect(
      page.getByTestId("stMainBlockContainer").getByTestId("stVerticalBlock")
    ).toContainText("Temperatura máxima:");
    await expect(
      page.getByTestId("stMainBlockContainer").getByTestId("stVerticalBlock")
    ).toContainText("Temperatura promedio:");
    await expect(
      page.getByTestId("stMainBlockContainer").getByTestId("stVerticalBlock")
    ).toContainText("Temperatura mínima:");
    await expect(
      page.getByTestId("stMainBlockContainer").getByTestId("stVerticalBlock")
    ).toContainText("CO₂ promedio:");
  });

  test("Se grafican los datos", async ({ page }) => {
    await expect(page.getByRole("img", { name: "0" })).toBeVisible();
  });
});
