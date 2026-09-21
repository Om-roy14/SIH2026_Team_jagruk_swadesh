import { useCallback, useState } from "react";
import {
  Camera,
  Search,
  ShieldCheck,
  ArrowLeft,
  AlertCircle,
} from "lucide-react";

import QRScanner from "../components/QRScanner";
import ProductDetails from "../components/ProductDetails";
import { lookupProduct } from "../services/verificationApi";

export default function ProductVerification() {
  const [scannerOpen, setScannerOpen] = useState(false);
  const [manualValue, setManualValue] = useState("");

  const [loading, setLoading] = useState(false);
  const [product, setProduct] = useState(null);
  const [notFound, setNotFound] = useState(false);
  const [error, setError] = useState("");

  const handleLookup = async (qrData) => {
    if (!qrData?.trim()) return;

    setScannerOpen(false);
    setLoading(true);
    setError("");
    setNotFound(false);
    setProduct(null);

    try {
      const result = await lookupProduct(qrData);

      if (result.found && result.data) {
        setProduct(result.data);
      } else {
        setNotFound(true);
      }
    } catch (err) {
      console.error("Product lookup failed:", err);

      setError(
        err.message ||
          "Unable to fetch product information."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleScan = useCallback(
    (qrData) => {
      handleLookup(qrData);
    },
    []
  );

  const reset = () => {
    setProduct(null);
    setNotFound(false);
    setError("");
    setManualValue("");
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-black px-4 py-10 text-white">

      {/* Background glow */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute left-[15%] top-[10%] h-72 w-72 rounded-full bg-white/[0.025] blur-[100px]" />
        <div className="absolute bottom-[10%] right-[10%] h-80 w-80 rounded-full bg-white/[0.02] blur-[120px]" />
      </div>

      <div className="relative mx-auto max-w-5xl">

        {/* Header */}
        <div className="mb-10 text-center">

          <div className="mb-5 inline-flex h-14 w-14 items-center justify-center rounded-2xl border border-white/10 bg-white/[0.06] backdrop-blur-xl">
            <ShieldCheck size={27} />
          </div>

          <p className="mb-2 text-xs font-medium uppercase tracking-[0.3em] text-white/35">
            Jagruk Swadesh
          </p>

          <h1 className="text-3xl font-semibold tracking-tight md:text-4xl">
            Verify a Product
          </h1>

          <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-white/45">
            Scan the QR code on your product to view
            available BIS information.
          </p>
        </div>

        {/* Result */}
        {product ? (
          <ProductDetails
            product={product}
            onScanAgain={reset}
          />
        ) : (
          <div className="mx-auto max-w-xl">

            {/* Scanner card */}
            <div className="rounded-[2rem] border border-white/10 bg-white/[0.045] p-6 shadow-2xl backdrop-blur-2xl md:p-8">

              <div className="mb-6 flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/[0.07]">
                  <Camera size={19} />
                </div>

                <div>
                  <h2 className="text-sm font-semibold">
                    Scan Product QR
                  </h2>

                  <p className="text-xs text-white/40">
                    Use your camera to scan the QR code.
                  </p>
                </div>
              </div>

              <button
                onClick={() => {
                  setError("");
                  setNotFound(false);
                  setScannerOpen(true);
                }}
                className="group flex w-full items-center justify-center gap-3 rounded-2xl bg-white px-5 py-4 text-sm font-semibold text-black transition hover:bg-white/90"
              >
                <Camera
                  size={19}
                  className="transition-transform group-hover:scale-110"
                />

                Scan Product QR
              </button>

              {/* Divider */}
              <div className="my-7 flex items-center gap-4">
                <div className="h-px flex-1 bg-white/[0.08]" />

                <span className="text-[10px] uppercase tracking-[0.2em] text-white/25">
                  or
                </span>

                <div className="h-px flex-1 bg-white/[0.08]" />
              </div>

              {/* Manual input */}
              <div>
                <label className="mb-2 block text-xs text-white/45">
                  Enter QR value manually
                </label>

                <div className="flex gap-2">

                  <input
                    value={manualValue}
                    onChange={(e) =>
                      setManualValue(e.target.value)
                    }
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        handleLookup(manualValue);
                      }
                    }}
                    placeholder="Enter QR content..."
                    className="min-w-0 flex-1 rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-sm text-white outline-none placeholder:text-white/20 focus:border-white/20"
                  />

                  <button
                    onClick={() => handleLookup(manualValue)}
                    disabled={!manualValue.trim() || loading}
                    className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-white/10 bg-white/[0.07] text-white transition hover:bg-white/[0.12] disabled:cursor-not-allowed disabled:opacity-30"
                  >
                    <Search size={17} />
                  </button>

                </div>
              </div>

              {/* Loading */}
              {loading && (
                <div className="mt-6 rounded-2xl border border-white/10 bg-white/[0.035] px-4 py-4 text-center">

                  <div className="mx-auto mb-3 h-6 w-6 animate-spin rounded-full border-2 border-white/15 border-t-white" />

                  <p className="text-sm text-white/70">
                    Fetching product information...
                  </p>

                  <p className="mt-1 text-xs text-white/30">
                    Searching available BIS data
                  </p>
                </div>
              )}

              {/* Error */}
              {error && !loading && (
                <div className="mt-6 flex gap-3 rounded-2xl border border-white/10 bg-white/[0.035] p-4">

                  <AlertCircle
                    size={18}
                    className="mt-0.5 shrink-0 text-white/60"
                  />

                  <div>
                    <p className="text-sm font-medium text-white">
                      Unable to fetch information
                    </p>

                    <p className="mt-1 text-xs leading-5 text-white/40">
                      {error}
                    </p>
                  </div>
                </div>
              )}

              {/* Not found */}
              {notFound && !loading && !error && (
                <div className="mt-6 rounded-2xl border border-white/10 bg-white/[0.035] p-5 text-center">

                  <div className="mx-auto mb-3 flex h-10 w-10 items-center justify-center rounded-full bg-white/[0.06]">
                    <ShieldCheck size={19} />
                  </div>

                  <h3 className="text-sm font-medium">
                    Product Information Not Found
                  </h3>

                  <p className="mx-auto mt-2 max-w-sm text-xs leading-5 text-white/40">
                    We could not find product information
                    matching this QR code in the available
                    database.
                  </p>

                  <button
                    onClick={reset}
                    className="mt-4 inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/[0.06] px-4 py-2 text-xs text-white/70 transition hover:bg-white/[0.1]"
                  >
                    <ArrowLeft size={14} />
                    Try Again
                  </button>
                </div>
              )}
            </div>

            {/* Information */}
            <p className="mt-5 text-center text-[11px] leading-5 text-white/25">
              Product information is displayed from the
              available BIS data. An unavailable record does
              not by itself prove that a physical product is
              counterfeit.
            </p>
          </div>
        )}
      </div>

      {/* QR scanner modal */}
      {scannerOpen && (
        <QRScanner
          onScan={handleScan}
          onClose={() => setScannerOpen(false)}
        />
      )}
    </div>
  );
}