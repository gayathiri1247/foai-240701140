document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loan-form");
  if (!form) return;
  const button = document.getElementById("submit-btn");
  const errorBox = document.getElementById("form-error");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorBox.classList.add("d-none");
    if (!form.reportValidity()) return;
    const payload = Object.fromEntries(new FormData(form).entries());
    for (const key of ["age", "service_years", "monthly_income", "annual_income", "existing_emi", "requested_amount", "property_value", "down_payment", "vehicle_price", "course_expenses", "tenure_months", "demo_annual_interest_rate"]) {
      if (payload[key] !== undefined && payload[key] !== "") payload[key] = Number(payload[key]);
    }
    button.disabled = true;
    button.textContent = "Evaluating…";
    try {
      const response = await fetch("/api/evaluate", {
        method: "POST", headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Unable to evaluate this application.");
      window.location.href = result.redirect_url;
    } catch (error) {
      errorBox.textContent = error.message || "A server error occurred. Please try again.";
      errorBox.classList.remove("d-none");
      button.disabled = false;
      button.textContent = "Evaluate eligibility";
    }
  });
});
