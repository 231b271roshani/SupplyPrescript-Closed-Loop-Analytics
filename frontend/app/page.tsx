
"use client";

import { useState } from "react";

type Prediction = {
  predicted_delay_days: number;
  recommended_action: string;
};

export default function Home() {
 
const [form, setForm] = useState({
  supplier_reliability: "",
  distance_km: "",
  weather_severity: "",
  customs_delay_days: "",
  inventory_level: "",
  shipping_mode: "",
});


  const [result, setResult] = useState<Prediction | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function updateField(name: string, value: string) {
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function predictDelay(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8001/predict-delay", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          supplier_reliability: Number(form.supplier_reliability),
          distance_km: Number(form.distance_km),
          weather_severity: Number(form.weather_severity),
          customs_delay_days: Number(form.customs_delay_days),
          inventory_level: Number(form.inventory_level),
          shipping_mode: form.shipping_mode,
        }),
      });

      if (!response.ok) {
        throw new Error("API_ERROR");
      }

      setResult(await response.json());
    } catch {
      setError(
        "Could not get prediction. Check the backend server and API configuration."
      );
    } finally {
      setLoading(false);
    }
  }

  const fields = [
    {
      name: "supplier_reliability",
      label: "Supplier Reliability",
      hint: "Range: 0 to 1",
      min: "0",
      max: "1",
      step: "0.1",
    },
    {
      name: "distance_km",
      label: "Shipping Distance",
      hint: "Distance in kilometres",
      min: "1",
      step: "1",
    },
    {
      name: "weather_severity",
      label: "Weather Severity",
      hint: "Range: 0 to 10",
      min: "0",
      max: "10",
      step: "1",
    },
    {
      name: "customs_delay_days",
      label: "Customs Delay",
      hint: "Delay in days",
      min: "0",
      step: "1",
    },
    {
      name: "inventory_level",
      label: "Inventory Level",
      hint: "Available inventory units",
      min: "0",
      step: "1",
    },
  ] as const;

  return (
    <main className="min-h-screen bg-[#080d18] text-slate-100">
      <nav className="border-b border-slate-800 bg-[#0b1220]">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-400 font-black text-slate-950">
              SP
            </div>
            <div>
              <h1 className="text-xl font-bold">
                Supply<span className="text-cyan-400">Prescript</span>
              </h1>
              <p className="text-xs text-slate-400">
                Prescriptive Supply Chain Intelligence
              </p>
            </div>
          </div>
          <span className="rounded-full border border-emerald-800 bg-emerald-950/50 px-3 py-1.5 text-xs text-emerald-300">
            ● ML Dashboard
          </span>
        </div>
      </nav>

      <div className="mx-auto max-w-7xl px-6 py-10">
        <section className="mb-9">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-400">
            Decision Support Platform
          </p>
          <h2 className="mt-3 text-3xl font-bold tracking-tight md:text-5xl">
            Predict delays. <span className="text-cyan-400">Act smarter.</span>
          </h2>
          <p className="mt-4 max-w-2xl leading-7 text-slate-400">
            Analyze shipment conditions, estimate delivery delays using your
            trained machine learning model, and get recommended next actions.
          </p>
        </section>

        <section className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-800 bg-[#101827] p-5">
            <p className="text-sm text-slate-400">Prediction Engine</p>
            <p className="mt-2 text-xl font-bold">Random Forest</p>
            <p className="mt-2 text-xs text-slate-500">
              Trained shipment delay model
            </p>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-[#101827] p-5">
            <p className="text-sm text-slate-400">Analytics</p>
            <p className="mt-2 text-xl font-bold">Delay Estimation</p>
            <p className="mt-2 text-xs text-slate-500">
              Based on shipment input features
            </p>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-[#101827] p-5 sm:col-span-2 lg:col-span-1">
            <p className="text-sm text-slate-400">Decision Output</p>
            <p className="mt-2 text-xl font-bold">Action Recommendations</p>
            <p className="mt-2 text-xs text-slate-500">
              Risk-based guidance for planning
            </p>
          </div>
        </section>

        <section className="grid items-start gap-6 lg:grid-cols-2">
          <form
            onSubmit={predictDelay}
            className="rounded-2xl border border-slate-800 bg-[#101827] p-6 md:p-8"
          >
            <div className="mb-7">
              <h3 className="text-xl font-bold">Shipment Configuration</h3>
              <p className="mt-2 text-sm text-slate-400">
                Enter the details for the shipment you want to analyze.
              </p>
            </div>

            <div className="grid gap-x-5 gap-y-5 sm:grid-cols-2">
              {fields.map((field) => (
                <label key={field.name} className="block">
                  <span className="text-sm font-medium text-slate-200">
                    {field.label}
                  </span>
                  <input
                    required
                    type="number"
                    min={field.min}
                    max={"max" in field ? field.max : undefined}
                    step={field.step}
                    value={form[field.name]}
                    onChange={(e) =>
                      updateField(field.name, e.target.value)
                    }
                    className="mt-2 w-full rounded-xl border border-slate-700 bg-[#080d18] px-4 py-3 outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/10"
                  />
                  <span className="mt-1.5 block text-xs text-slate-500">
                    {field.hint}
                  </span>
                </label>
              ))}

              <label className="block">
                <span className="text-sm font-medium text-slate-200">
                  Shipping Mode
                </span>
                
<select
  required
  value={form.shipping_mode}
  onChange={(e) =>
    updateField("shipping_mode", e.target.value)
  }
  className="mt-2 w-full rounded-xl border border-slate-700 bg-[#080d18] px-4 py-3 outline-none focus:border-cyan-400"
>
  <option value="" disabled>
    Select shipping mode
  </option>
  <option value="Air">Air</option>
  <option value="Road">Road</option>
  <option value="Sea">Sea</option>
  <option value="Rail">Rail</option>
</select>

                <span className="mt-1.5 block text-xs text-slate-500">
                  Select the transport method
                </span>
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-8 w-full rounded-xl bg-cyan-400 px-5 py-4 font-bold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Analyzing Shipment..." : "Predict Delay →"}
            </button>

            <p className="mt-4 text-center text-xs text-slate-500">
              Predictions depend on your trained model and input data.
            </p>
          </form>

          <section className="rounded-2xl border border-slate-800 bg-[#101827] p-6 md:p-8">
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-cyan-400">
              Prediction Report
            </p>
            <h3 className="mt-2 text-2xl font-bold">Shipment Analysis</h3>
            <p className="mt-2 text-sm text-slate-400">
              Your model output and recommended action will appear here.
            </p>

            {error && (
              <div className="mt-7 rounded-xl border border-red-900 bg-red-950/40 p-4 text-sm leading-6 text-red-300">
                {error}
              </div>
            )}

            {!result && !error && (
              <div className="mt-7 flex min-h-64 flex-col items-center justify-center rounded-xl border border-dashed border-slate-700 p-6 text-center">
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-cyan-950 text-3xl">
                  ↗
                </div>
                <p className="mt-5 font-semibold">Awaiting shipment data</p>
                <p className="mt-2 max-w-xs text-sm leading-6 text-slate-500">
                  Fill in the shipment form and select Predict Delay to generate
                  an estimate.
                </p>
              </div>
            )}

            {result && (
              <div className="mt-7 space-y-5">
                <div className="rounded-xl border border-cyan-900 bg-cyan-950/30 p-6">
                  <p className="text-sm text-slate-400">
                    Predicted Shipment Delay
                  </p>
                  <p className="mt-3 text-5xl font-bold text-cyan-300">
                    {result.predicted_delay_days}
                    <span className="ml-2 text-base font-medium text-slate-400">
                      days
                    </span>
                  </p>
                </div>

                <div className="rounded-xl border border-slate-700 bg-[#080d18] p-5">
                  <p className="text-sm font-semibold text-emerald-300">
                    Recommended Action
                  </p>
                  <p className="mt-3 text-sm leading-7 text-slate-300">
                    {result.recommended_action}
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() => setResult(null)}
                  className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800"
                >
                  New Prediction
                </button>
              </div>
            )}
          </section>
        </section>

        <footer className="mt-10 border-t border-slate-800 py-6 text-center text-xs text-slate-500">
          SupplyPrescript · Closed-Loop Prescriptive Analytics · ML-powered
          decision support
        </footer>
      </div>
    </main>
  );
}
