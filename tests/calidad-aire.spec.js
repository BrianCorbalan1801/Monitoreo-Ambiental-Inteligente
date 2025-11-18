test.describe("Chequeo calidad aire", () => {
  test("Muestra diferentes niveles de calidad del aire", async () => {
    const mockResponses = [
      { calidad: "🟢 Bueno" },
      { calidad: "🟠 Moderado" },
      { calidad: "🔴 Malo" },
    ];

    let call = 0;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockResponses[call++]),
      })
    );

    render(<TuComponente />);

    expect(await screen.findByText(/Bueno/i)).toBeInTheDocument();
    expect(await screen.findByText(/Moderado/i)).toBeInTheDocument();
    expect(await screen.findByText(/Malo/i)).toBeInTheDocument();
  });
});
