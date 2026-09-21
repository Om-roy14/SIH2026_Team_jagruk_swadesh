import React, { useState } from "react";
import {
  ShieldCheck,
  Package,
  Factory,
  FileCheck2,
  CalendarDays,
  FlaskConical,
  MapPin,
  RefreshCw,
  AlertCircle,
  ScanLine,
} from "lucide-react";

import QRScanner from "./QRScanner";
import { dummyProducts } from "../data/dummyProducts";

export default function ProductDetails() {
  const [showScanner, setShowScanner] = useState(true);
  const [scannedCode, setScannedCode] = useState("");
  const [product, setProduct] = useState(null);
  const [notFound, setNotFound] = useState(false);

  const handleScanSuccess = (decodedText) => {
    const qrCode = decodedText.trim();

    console.log("SCANNED QR:", qrCode);

    // Save QR identifier
    setScannedCode(qrCode);

    // Close scanner
    setShowScanner(false);

    // IMPORTANT:
    // Use QR code as the key to find the product.
    const foundProduct = dummyProducts[qrCode];

    console.log("FOUND PRODUCT:", foundProduct);

    if (foundProduct) {
      setProduct(foundProduct);
      setNotFound(false);
    } else {
      setProduct(null);
      setNotFound(true);
    }
  };

  const scanAnother = () => {
    setScannedCode("");
    setProduct(null);
    setNotFound(false);
    setShowScanner(true);
  };

  return (
    <div className="min-h-screen px-6 pt-32 pb-20">

      {/* QR SCANNER */}
      {showScanner && (
        <QRScanner
          onScanSuccess={handleScanSuccess}
          onClose={() => setShowScanner(false)}
        />
      )}

      <div className="mx-auto max-w-5xl">

        {/* PAGE HEADER */}
        <div className="mb-10 text-center">

          <div className="mb-4 flex justify-center">
            <div className="rounded-2xl bg-emerald-500/20 p-4">
              <ScanLine className="h-8 w-8 text-emerald-300" />
            </div>
          </div>

          <h1 className="text-4xl font-bold text-white">
            Product Verification
          </h1>

          <p className="mt-3 text-white/60">
            Scan a product QR code to view its verification details.
          </p>

        </div>

        {/* SCANNED QR */}
        {scannedCode && (
          <div className="mb-6 rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl">

            <p className="text-sm text-white/40">
              SCANNED QR IDENTIFIER
            </p>

            <p className="mt-2 font-mono text-lg font-semibold text-emerald-300">
              {scannedCode}
            </p>

          </div>
        )}

        {/* ========================= */}
        {/* PRODUCT FOUND */}
        {/* ========================= */}

        {product && (

          <div className="overflow-hidden rounded-3xl border border-emerald-400/20 bg-black/30 shadow-2xl backdrop-blur-xl">

            {/* VERIFICATION HEADER */}
            <div className="flex flex-col gap-5 border-b border-white/10 p-6 md:flex-row md:items-center md:justify-between">

              <div>

                <p className="text-sm uppercase tracking-wider text-white/40">
                  Product Verification
                </p>

                <h2 className="mt-2 text-3xl font-bold text-white">
                  {product.productName}
                </h2>

              </div>

              <div className="flex w-fit items-center gap-2 rounded-full bg-emerald-500/15 px-4 py-2 text-emerald-300">

                <ShieldCheck className="h-5 w-5" />

                <span className="font-semibold">
                  {product.verificationStatus}
                </span>

              </div>

            </div>

            {/* PRODUCT DETAILS */}
            <div className="grid gap-4 p-6 md:grid-cols-2">

              <DetailCard
                icon={Package}
                label="Product ID"
                value={product.productId}
              />

              <DetailCard
                icon={FileCheck2}
                label="BIS Standard"
                value={product.standard}
              />

              <DetailCard
                icon={Factory}
                label="Manufacturer"
                value={product.manufacturer}
              />

              <DetailCard
                icon={FileCheck2}
                label="Licence Number"
                value={product.licenceNumber}
              />

              <DetailCard
                icon={CalendarDays}
                label="Manufacturing Date"
                value={product.manufacturingDate}
              />

              <DetailCard
                icon={CalendarDays}
                label="Testing Date"
                value={product.testDate}
              />

              <DetailCard
                icon={FlaskConical}
                label="Testing Laboratory"
                value={product.laboratory}
              />

              <DetailCard
                icon={MapPin}
                label="Laboratory Location"
                value={product.location}
              />

            </div>

            {/* LAST UPDATED */}
            <div className="border-t border-white/10 px-6 py-5">

              <p className="text-sm text-white/40">
                Last Updated
              </p>

              <p className="mt-1 text-white/80">
                {product.lastUpdated}
              </p>

            </div>

            {/* SCAN AGAIN */}
            <div className="border-t border-white/10 p-6">

              <button
                onClick={scanAnother}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-500 px-5 py-3 font-semibold text-black transition hover:bg-emerald-400"
              >

                <RefreshCw className="h-5 w-5" />

                Scan Another Product

              </button>

            </div>

          </div>

        )}

        {/* ========================= */}
        {/* PRODUCT NOT FOUND */}
        {/* ========================= */}

        {notFound && (

          <div className="rounded-3xl border border-red-400/20 bg-red-500/10 p-10 text-center backdrop-blur-xl">

            <div className="mb-5 flex justify-center">

              <div className="rounded-full bg-red-500/20 p-4">

                <AlertCircle className="h-8 w-8 text-red-400" />

              </div>

            </div>

            <h2 className="text-2xl font-bold text-white">
              Product Not Found
            </h2>

            <p className="mx-auto mt-3 max-w-lg text-white/60">
              No product information is available for this QR identifier.
            </p>

            <p className="mt-4 font-mono text-sm text-red-300">
              {scannedCode}
            </p>

            <button
              onClick={scanAnother}
              className="mt-6 inline-flex items-center gap-2 rounded-xl bg-white/10 px-6 py-3 font-semibold text-white transition hover:bg-white/20"
            >

              <RefreshCw className="h-5 w-5" />

              Scan Again

            </button>

          </div>

        )}

        {/* ========================= */}
        {/* READY TO SCAN */}
        {/* ========================= */}

        {!showScanner &&
          !product &&
          !notFound && (

            <div className="rounded-3xl border border-white/10 bg-white/5 p-10 text-center backdrop-blur-xl">

              <ScanLine className="mx-auto h-12 w-12 text-emerald-300" />

              <h2 className="mt-4 text-2xl font-bold text-white">
                Ready to Verify
              </h2>

              <p className="mt-2 text-white/50">
                Scan a product QR code to continue.
              </p>

              <button
                onClick={() => setShowScanner(true)}
                className="mt-6 rounded-xl bg-emerald-500 px-6 py-3 font-semibold text-black"
              >
                Open QR Scanner
              </button>

            </div>

          )}

      </div>

    </div>
  );
}


/* ================================= */
/* DETAIL CARD                       */
/* ================================= */

function DetailCard({ icon: Icon, label, value }) {

  return (

    <div className="rounded-2xl border border-white/10 bg-white/5 p-5 transition hover:bg-white/10">

      <div className="flex items-start gap-4">

        <div className="rounded-xl bg-emerald-500/10 p-3">

          <Icon className="h-5 w-5 text-emerald-300" />

        </div>

        <div className="min-w-0">

          <p className="text-sm text-white/40">
            {label}
          </p>

          <p className="mt-1 break-words font-medium text-white">
            {value}
          </p>

        </div>

      </div>

    </div>

  );
}