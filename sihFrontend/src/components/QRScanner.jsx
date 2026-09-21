import React, { useEffect, useRef, useState } from "react";
import {
  ScanLine,
  RefreshCw,
  X,
  AlertCircle,
  CheckCircle2,
} from "lucide-react";
import { Html5Qrcode } from "html5-qrcode";

const QR_READER_ID = "jagruk-swadesh-qr-reader";

export default function QRScanner({ onScanSuccess, onClose }) {
  const scannerRef = useRef(null);
  const isScanningRef = useRef(false);
  const isScannedRef = useRef(false);

  const [error, setError] = useState("");
  const [isStarting, setIsStarting] = useState(true);
  const [isScanned, setIsScanned] = useState(false);


  /* =========================================================
     FORCE CAMERA LAYOUT
  ========================================================= */

  const fixCameraLayout = () => {
    const reader = document.getElementById(QR_READER_ID);

    if (!reader) return;

    /* Main reader */

    reader.style.setProperty("width", "100%", "important");
    reader.style.setProperty("height", "600px", "important");
    reader.style.setProperty("min-height", "600px", "important");
    reader.style.setProperty("max-height", "600px", "important");
    reader.style.setProperty("position", "relative", "important");
    reader.style.setProperty("overflow", "hidden", "important");
    reader.style.setProperty("background", "#000", "important");


    /* Scan region */

    const scanRegion = document.getElementById(
      `${QR_READER_ID}__scan_region`
    );

    if (scanRegion) {
      scanRegion.style.setProperty("width", "100%", "important");
      scanRegion.style.setProperty("height", "600px", "important");
      scanRegion.style.setProperty("min-height", "600px", "important");
      scanRegion.style.setProperty("max-height", "600px", "important");
      scanRegion.style.setProperty("position", "absolute", "important");
      scanRegion.style.setProperty("left", "0", "important");
      scanRegion.style.setProperty("top", "0", "important");
      scanRegion.style.setProperty("border", "none", "important");
      scanRegion.style.setProperty("overflow", "hidden", "important");
    }


    /* Camera video */

    const videos = reader.querySelectorAll("video");

    videos.forEach((video) => {
      video.style.setProperty(
        "position",
        "absolute",
        "important"
      );

      video.style.setProperty(
        "left",
        "0",
        "important"
      );

      video.style.setProperty(
        "top",
        "0",
        "important"
      );

      video.style.setProperty(
        "width",
        "100%",
        "important"
      );

      video.style.setProperty(
        "height",
        "600px",
        "important"
      );

      video.style.setProperty(
        "min-width",
        "100%",
        "important"
      );

      video.style.setProperty(
        "min-height",
        "600px",
        "important"
      );

      video.style.setProperty(
        "max-width",
        "none",
        "important"
      );

      video.style.setProperty(
        "max-height",
        "600px",
        "important"
      );

      video.style.setProperty(
        "object-fit",
        "cover",
        "important"
      );

      video.style.setProperty(
        "display",
        "block",
        "important"
      );

      video.style.setProperty(
        "background",
        "#000",
        "important"
      );
    });


    /* Hide html5-qrcode dashboard */

    const dashboard = document.getElementById(
      `${QR_READER_ID}__dashboard`
    );

    if (dashboard) {
      dashboard.style.setProperty(
        "display",
        "none",
        "important"
      );
    }
  };


  /* =========================================================
     STOP SCANNER
     
     Centralized cleanup prevents multiple camera instances.
  ========================================================= */

  const stopScanner = async () => {
    if (!scannerRef.current) {
      return;
    }

    try {
      if (isScanningRef.current) {
        await scannerRef.current.stop();
      }

      await scannerRef.current.clear();
    } catch (cleanupError) {
      console.warn(
        "QR scanner cleanup warning:",
        cleanupError
      );
    }

    scannerRef.current = null;
    isScanningRef.current = false;
  };


  /* =========================================================
     START SCANNER
  ========================================================= */

  const startScanner = async () => {
    setError("");
    setIsStarting(true);
    setIsScanned(false);

    isScannedRef.current = false;

    try {
      /* -------------------------------------------------------
         STOP PREVIOUS SCANNER
      ------------------------------------------------------- */

      await stopScanner();


      /* -------------------------------------------------------
         CLEAR READER CONTAINER
      ------------------------------------------------------- */

      const reader = document.getElementById(QR_READER_ID);

      if (reader) {
        reader.innerHTML = "";
      }


      /* -------------------------------------------------------
         CREATE NEW SCANNER
      ------------------------------------------------------- */

      const scanner = new Html5Qrcode(QR_READER_ID);

      scannerRef.current = scanner;


      /* -------------------------------------------------------
         START CAMERA
      ------------------------------------------------------- */

      await scanner.start(
        {
          facingMode: "environment",
        },

        {
          fps: 10,

          qrbox: {
            width: 350,
            height: 350,
          },

          disableFlip: false,
        },


        /* -----------------------------------------------------
           QR DETECTED
        ----------------------------------------------------- */

        async (decodedText) => {
          /*
           * Prevent multiple callbacks from the same QR code.
           */
          if (isScannedRef.current) {
            return;
          }

          isScannedRef.current = true;

          setIsScanned(true);


          /*
           * Stop camera immediately after successful scan.
           */
          try {
            if (scannerRef.current) {
              await scannerRef.current.stop();
            }
          } catch (stopError) {
            console.warn(
              "QR scanner stop warning:",
              stopError
            );
          }

          isScanningRef.current = false;


          /*
           * Send decoded QR value to ProductDetails.
           *
           * Example:
           *
           * QR-PROD-001
           *
           * ProductDetails then performs:
           *
           * dummyProducts["QR-PROD-001"]
           */
          if (onScanSuccess) {
            onScanSuccess(decodedText);
          }
        },


        /* -----------------------------------------------------
           QR NOT DETECTED
        ----------------------------------------------------- */

        () => {
          /*
           * html5-qrcode continuously calls this callback
           * when no QR code is detected.
           *
           * Intentionally ignored.
           */
        }
      );


      /* -------------------------------------------------------
         CAMERA STARTED
      ------------------------------------------------------- */

      isScanningRef.current = true;

      setIsStarting(false);


      /* -------------------------------------------------------
         APPLY CAMERA SIZE
         
         html5-qrcode creates its video elements asynchronously,
         therefore layout is applied multiple times.
      ------------------------------------------------------- */

      fixCameraLayout();

      setTimeout(fixCameraLayout, 100);
      setTimeout(fixCameraLayout, 300);
      setTimeout(fixCameraLayout, 700);
      setTimeout(fixCameraLayout, 1200);

    } catch (err) {
      console.error("QR scanner error:", err);

      isScanningRef.current = false;

      setIsStarting(false);

      const errorName = err?.name || "";
      const errorMessage =
        err?.message?.toLowerCase() || "";


      /* Camera permission */

      if (
        errorName === "NotAllowedError" ||
        errorMessage.includes("permission")
      ) {
        setError(
          "Camera permission was denied. Please allow camera access and try again."
        );

      /* No camera */

      } else if (
        errorName === "NotFoundError"
      ) {
        setError(
          "No camera was found on this device."
        );

      /* Camera already in use */

      } else if (
        errorName === "NotReadableError"
      ) {
        setError(
          "The camera is already being used by another application."
        );

      /* Generic camera error */

      } else {
        setError(
          "Unable to start the camera. Please check your browser permissions and try again."
        );
      }
    }
  };


  /* =========================================================
     INITIALIZE SCANNER
  ========================================================= */

  useEffect(() => {
    startScanner();

    return () => {
      stopScanner();
    };
  }, []);


  /* =========================================================
     RETRY
  ========================================================= */

  const handleRetry = async () => {
    await startScanner();
  };


  /* =========================================================
     CLOSE SCANNER
  ========================================================= */

  const handleClose = async () => {
    await stopScanner();

    if (onClose) {
      onClose();
    }
  };


  /* =========================================================
     UI
  ========================================================= */

  return (
    <div
      className="
        fixed
        inset-0
        z-[100]
        flex
        items-center
        justify-center
        bg-black/80
        px-4
        py-5
        backdrop-blur-xl
      "
    >

      {/* =====================================================
          MAIN CARD
      ===================================================== */}

      <div
        className="
          relative
          flex
          h-[95vh]
          w-full
          max-w-5xl
          flex-col
          overflow-hidden
          rounded-3xl
          border
          border-white/10
          bg-black/70
          shadow-2xl
          backdrop-blur-2xl
        "
      >

        {/* ===================================================
            HEADER
        =================================================== */}

        <div
          className="
            flex
            shrink-0
            items-center
            justify-between
            border-b
            border-white/10
            px-6
            py-5
          "
        >

          <div className="flex items-center gap-4">

            <div
              className="
                flex
                h-12
                w-12
                items-center
                justify-center
                rounded-2xl
                border
                border-emerald-400/20
                bg-emerald-400/10
              "
            >
              <ScanLine
                size={25}
                className="text-emerald-300"
              />
            </div>


            <div>

              <h2 className="text-xl font-semibold text-white">
                Scan Product QR
              </h2>

              <p className="mt-1 text-sm text-white/50">
                Verify product information
              </p>

            </div>

          </div>


          {/* Close */}

          <button
            type="button"
            onClick={handleClose}
            aria-label="Close QR scanner"
            className="
              flex
              h-11
              w-11
              items-center
              justify-center
              rounded-xl
              border
              border-white/10
              bg-white/5
              text-white/60
              transition
              hover:bg-white/10
              hover:text-white
            "
          >
            <X size={21} />
          </button>

        </div>


        {/* ===================================================
            CAMERA
        =================================================== */}

        <div
          className="
            relative
            flex
            flex-1
            items-center
            justify-center
            overflow-hidden
            p-6
          "
        >

          <div
            className="
              relative
              h-[600px]
              min-h-[600px]
              w-full
              max-w-4xl
              overflow-hidden
              rounded-3xl
              border
              border-white/10
              bg-black
            "
          >

            {/* =================================================
                CAMERA
            ================================================= */}

            <div
              id={QR_READER_ID}
              className="
                absolute
                inset-0
                h-[600px]
                min-h-[600px]
                w-full
                overflow-hidden
                bg-black
              "
            />


            {/* =================================================
                SCANNING FRAME
            ================================================= */}

            {!error &&
              !isScanned &&
              !isStarting && (

                <div
                  className="
                    pointer-events-none
                    absolute
                    inset-0
                    z-20
                  "
                >

                  <div
                    className="
                      absolute
                      left-1/2
                      top-1/2
                      h-[350px]
                      w-[350px]
                      -translate-x-1/2
                      -translate-y-1/2
                    "
                  >

                    {/* Top Left */}

                    <div
                      className="
                        absolute
                        left-0
                        top-0
                        h-12
                        w-12
                        border-l-[3px]
                        border-t-[3px]
                        border-emerald-400
                      "
                    />


                    {/* Top Right */}

                    <div
                      className="
                        absolute
                        right-0
                        top-0
                        h-12
                        w-12
                        border-r-[3px]
                        border-t-[3px]
                        border-emerald-400
                      "
                    />


                    {/* Bottom Left */}

                    <div
                      className="
                        absolute
                        bottom-0
                        left-0
                        h-12
                        w-12
                        border-b-[3px]
                        border-l-[3px]
                        border-emerald-400
                      "
                    />


                    {/* Bottom Right */}

                    <div
                      className="
                        absolute
                        bottom-0
                        right-0
                        h-12
                        w-12
                        border-b-[3px]
                        border-r-[3px]
                        border-emerald-400
                      "
                    />


                    {/* Scan Line */}

                    <div
                      className="
                        absolute
                        left-4
                        right-4
                        top-1/2
                        h-[3px]
                        -translate-y-1/2
                        animate-pulse
                        bg-emerald-400
                        shadow-[0_0_20px_rgba(52,211,153,0.95)]
                      "
                    />

                  </div>

                </div>
              )}


            {/* =================================================
                STARTING
            ================================================= */}

            {isStarting && !error && (

              <div
                className="
                  absolute
                  inset-0
                  z-30
                  flex
                  flex-col
                  items-center
                  justify-center
                  bg-black/80
                "
              >

                <div
                  className="
                    mb-5
                    flex
                    h-16
                    w-16
                    items-center
                    justify-center
                    rounded-full
                    border
                    border-emerald-400/20
                    bg-emerald-400/10
                  "
                >

                  <ScanLine
                    size={30}
                    className="animate-pulse text-emerald-300"
                  />

                </div>

                <p className="text-base text-white/80">
                  Starting camera...
                </p>

              </div>
            )}


            {/* =================================================
                ERROR
            ================================================= */}

            {error && (

              <div
                className="
                  absolute
                  inset-0
                  z-40
                  flex
                  flex-col
                  items-center
                  justify-center
                  bg-black/90
                  px-8
                  text-center
                "
              >

                <div
                  className="
                    mb-5
                    flex
                    h-16
                    w-16
                    items-center
                    justify-center
                    rounded-full
                    border
                    border-red-400/20
                    bg-red-400/10
                  "
                >

                  <AlertCircle
                    size={30}
                    className="text-red-300"
                  />

                </div>


                <h3 className="mb-2 text-xl font-semibold text-white">
                  Camera unavailable
                </h3>


                <p className="max-w-md text-sm leading-6 text-white/60">
                  {error}
                </p>


                <button
                  type="button"
                  onClick={handleRetry}
                  className="
                    mt-7
                    inline-flex
                    items-center
                    gap-2
                    rounded-xl
                    border
                    border-emerald-400/20
                    bg-emerald-400/10
                    px-6
                    py-3
                    text-sm
                    font-medium
                    text-emerald-300
                    transition
                    hover:bg-emerald-400/20
                  "
                >

                  <RefreshCw size={17} />

                  Try Again

                </button>

              </div>
            )}


            {/* =================================================
                SUCCESS
            ================================================= */}

            {isScanned && (

              <div
                className="
                  absolute
                  inset-0
                  z-40
                  flex
                  flex-col
                  items-center
                  justify-center
                  bg-black/75
                  backdrop-blur-md
                "
              >

                <div
                  className="
                    mb-5
                    flex
                    h-20
                    w-20
                    items-center
                    justify-center
                    rounded-full
                    border
                    border-emerald-400/30
                    bg-emerald-400/10
                  "
                >

                  <CheckCircle2
                    size={40}
                    className="text-emerald-300"
                  />

                </div>


                <h3 className="text-xl font-semibold text-white">
                  QR Code Scanned
                </h3>


                <p className="mt-2 text-sm text-white/50">
                  Looking up product information...
                </p>

              </div>
            )}

          </div>

        </div>


        {/* ===================================================
            INSTRUCTIONS
        =================================================== */}

        {!error && !isScanned && (

          <div
            className="
              shrink-0
              border-t
              border-white/10
              px-6
              py-4
              text-center
            "
          >

            <p className="text-sm font-medium text-white/80">
              Position the product QR code inside the frame
            </p>

            <p className="mt-1 text-xs text-white/40">
              Keep the QR code steady and clearly visible
            </p>

          </div>

        )}


        {/* ===================================================
            FOOTER
        =================================================== */}

        <div
          className="
            shrink-0
            border-t
            border-white/10
            px-6
            py-3
          "
        >

          <div
            className="
              flex
              items-center
              justify-center
              gap-2
              text-xs
              text-white/40
            "
          >

            <div
              className="
                h-1.5
                w-1.5
                rounded-full
                bg-emerald-400
              "
            />

            <span>
              BIS Product Verification
            </span>

          </div>

        </div>

      </div>

    </div>
  );
}