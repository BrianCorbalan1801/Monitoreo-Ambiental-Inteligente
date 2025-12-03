const { test, expect } = require("@playwright/test");

test.beforeEach(async ({ page }) => {
  await page.goto("http://localhost:8501/");
});

test.describe("Mapa interactivo", () => {
  test("test", async ({ page }) => {
    await page
      .getByTestId("stSidebarCollapsedControl")
      .getByTestId("stBaseButton-headerNoPadding")
      .click();
    await page
      .locator("div")
      .filter({ hasText: /^Inicio$/ })
      .first()
      .click();
    await page.getByText("Mapa interactivo").click();
    await page.getByRole("heading", { name: "Mapa interactivo" }).click();
    await page
      .locator('[data-testid="stIFrame"]')
      .contentFrame()
      .locator("iframe")
      .contentFrame()
      .locator("div")
      .first()
      .click();
    await page
      .locator('[data-testid="stIFrame"]')
      .contentFrame()
      .locator("iframe")
      .contentFrame()
      .getByText("Zona: ETEC Temperatura: 29.4")
      .click();
  });
});
