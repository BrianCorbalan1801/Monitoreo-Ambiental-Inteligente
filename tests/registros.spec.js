const { test, expect } = require("@playwright/test");

test.beforeEach(async ({ page }) => {
  await page.goto("http://localhost:8501/");
});

test.describe("Registros Historicos", () => {
  test("test", async ({ page }) => {
    await expect(page.locator("#filtros")).toContainText("Filtros");
    await expect(
      page.getByTestId("stMainBlockContainer").getByTestId("stSelectbox")
    ).toBeVisible();
    await expect(page.getByText("Desde:Press the down arrow")).toBeVisible();
    await expect(page.getByText("Hasta:Press the down arrow")).toBeVisible();
  });
});
