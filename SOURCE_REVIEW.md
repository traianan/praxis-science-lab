# Source inventory — 8 September 2026

Praxis Science Lab · Public support: traiananghel@gmail.com

Scope: five distinct Android applications. `ceas-atomic-scaffold` is a scaffold of the clock, not a separate product. Web-only projects are excluded. No medical learning content was created. Existing uncommitted work in application repositories was preserved.

These are source observations, not signed-artifact or Google Play approvals.

## Scientific Calculator

Package: `com.traian64.calcstiintificcniorga`

Calculation history (up to 50 results), number formatting, angle and base preferences, and language are stored in app-private storage. Calculations run on the device. The app does not transmit these records to Praxis Science Lab. No accounts, advertising, analytics or crash-reporting service are implemented.

No camera, microphone, contacts or location permission is requested. The Android package declares Internet access through its framework, but the calculator has no application network requests and over-the-air updates are disabled. Opening the privacy or publisher link uses your browser.

Reviewed source paths:
- `calc-stiintific-cn-iorga/app.json` — SHA256 `91f024fc9bcc3819b4f543e4ae4ade42ab2222a889e15205bb77b8b42c4c7bdf`
- `calc-stiintific-cn-iorga/package.json` — SHA256 `ebc095090d72ebb6f27a5411a4c11010712565fab59c939ab85c86e2d55a4c4c`
- `calc-stiintific-cn-iorga/src/hooks/useCalculator.ts` — SHA256 `5f485c3d32f2d8733a7b8a207c2bb7f77f36cbadce7e2957c27be043ad120ea1`
- `calc-stiintific-cn-iorga/src/engine/session.ts` — SHA256 `0037f0fdbd2d3eb585e216b493b7c84854e713ccedba033a8a9505a3ab7bc0c5`
- `calc-stiintific-cn-iorga/src/components/modals/AboutModal.tsx` — SHA256 `a0015ec8a720b727c5329836dd6b6aea66f33e1e7a143dda266a286dc616b0b6`

Outstanding:
- Final upload-key-signed AAB and verification on a physical Android device are still required.
- Complete account verification, actual audience/IARC forms, and the closed test required by the account.

## Atomic Clock

Package: `app.physlab.ceas_atomic`

Server choice, synchronization settings, the last synchronization result and selected time zones are stored on your device. To synchronize, the app sends network time requests to the selected server and configured fallbacks. Recipients see your source IP address, request timing and protocol information. The HTTPS fallback also sends an app-identifying User-Agent. The app does not create an account or send a location-sensor reading, and has no advertising or analytics SDK.

Internet access is used for NTP and optional HTTPS synchronization. The default server is time.cloudflare.com. Fallbacks include NTP Pool hosts; Google Time, Apple Time and a custom host can also be selected. If a server fails, other configured providers may be contacted. NTP uses UDP and is not encrypted. The Cloudflare HTTPS fallback uses encrypted transport. Server operators process connection information under their own policies; a custom server is controlled by its operator.

Reviewed source paths:
- `ceas-atomic/pubspec.yaml` — SHA256 `d6d01f955312a4bf37cbeb16a47cad9e374239f522900617d17df461a39e71d5`
- `ceas-atomic/android/app/src/main/AndroidManifest.xml` — SHA256 `553c6b84301c42d579306021f6dd59ebc8c840df16c4484669aa9c343f6b986b`
- `ceas-atomic/lib/core/config/app_config.dart` — SHA256 `6757f0d43c74c3f09c5bb27554fc3bfc91621994c7b0fded4f0671fd2574f1ff`
- `ceas-atomic/lib/core/ntp/ntp_client.dart` — SHA256 `294dbdf900d99204bcaa434d0ce90d75d3dd36cde178d9bec16cd1ba05710feb`
- `ceas-atomic/lib/core/ntp/http_time_fallback.dart` — SHA256 `9b61d33b7edc355aa75684777d7038d39ed8f6cd71dddbaf68c670e499ceec91`

Outstanding:
- Data safety needs provider-level review of IP/request processing and retention. Do not submit an unqualified no-data-collected answer.
- NTP traffic is unencrypted: do not declare all transmitted data encrypted.
- Capture current-build screenshots and verify the final signed AAB, native libraries and device behavior.

## Frequency Sound Generator

Package: `app.physlab.frequency_generator`

Generator settings, language, presets and the last generator state are stored locally. Audio is synthesized on your device. Exported WAV files are written to a destination managed by the device. The app has no account, advertising SDK, analytics service or application backend and does not upload presets or generated audio to Praxis Science Lab.

The Android release does not request microphone access. A legacy write-storage permission is limited to Android API 28 and below for WAV export. Newer Android versions use the platform's file/media facilities. If you open or share an exported file with another service, that destination handles the file under its own policy.

Reviewed source paths:
- `frequency-generator/pubspec.yaml` — SHA256 `c28bf75c88ee76716d0773bcaa46507b175c333ad58608b44ad3c3afcf58256f`
- `frequency-generator/android/app/src/main/AndroidManifest.xml` — SHA256 `6440b1a05e432d689969031e4f99bbe2abbf9c3d3b9b52c77e3e0c32d73dc974`
- `frequency-generator/lib/core/config/app_config.dart` — SHA256 `b52a54b670903805fddbc364d12ce293c01075c49cda27ca3214e3a634bd6ac4`
- `frequency-generator/lib/core/services` (source directory)
- `frequency-generator/lib/state` (source directory)

Outstanding:
- Capture current-build screenshots and inspect final merged permissions, legacy export behavior, signed AAB and physical-device audio behavior.

## AudioLab

Package: `app.physlab.audiolab`

Live microphone samples and user-selected audio files are processed on your device. AudioLab stores preferences, session names and state, file references and numeric measurement records in its private local database. Microphone analysis is started by the user and stops when the app leaves the foreground. The app has no account, analytics, advertising or cloud service. The Android release removes Internet and network-state permissions.

RECORD_AUDIO is requested for live analysis. You can deny or revoke it in Android Settings and continue with features that do not need the microphone. Audio-file access is granted through the system picker. Exporting a chart, session or PDF writes the information you choose to a system-selected destination, which may be a cloud-backed document provider. Such a provider handles its copy under its own policy. The app does not automatically upload microphone audio.

Reviewed source paths:
- `audiolab/pubspec.yaml` — SHA256 `31e3cec413d8ad23a24e0d527cc8a2d9c834d6e4a6ec0aa651e4821e78d3e8ee`
- `audiolab/android/app/src/main/AndroidManifest.xml` — SHA256 `1bfe1024081ef4c10c73e4803e76f09b0217741325c1acbcab7894827401ea41`
- `audiolab/lib/data/store.dart` — SHA256 `5ad9858fde30592d6e90a8af958c25a211eb9e1f4a324100f45511127ab50e7d`
- `audiolab/lib/main.dart` — SHA256 `46cd37dfcb852f64dd716bdf5775f37531f42074ff8c6ec9a99563a1d2523456`
- `audiolab/android/app/src/main/kotlin` (source directory)

Outstanding:
- Verify microphone denial/revocation and foreground-only operation on the final signed build.
- Capture release screenshots and test native-library alignment, audio routes and exported-report accuracy on physical hardware.

## Medical Terminology Flashcards

Package: `ro.traiananghel.medicalterminology`

Study history, progress, favorites, preferences and ad frequency limits are stored in private device storage. Search text is used in memory, not stored as search history. No patient information, health records, microphone audio or location-sensor data is requested. The app has no account, application analytics, cloud synchronization or crash-reporting service. Studied terms and progress are not attached to advertising requests.

The current development release includes Google Mobile Ads Next-Gen 1.4.0 and User Messaging Platform 4.0.0, but blank production identifiers keep advertising and consent requests disabled. This policy covers that configuration. An advertising-enabled release requires an updated policy and Data safety declaration before distribution. Google ad services can process identifiers, approximate location inferred from IP, interactions and diagnostics. The package excludes the Android advertising-ID permission, which does not exclude all identifiers. Pronunciation passes selected text to an installed offline text-to-speech voice; that engine is supplied separately by its provider.

Reviewed source paths:
- `Medical-Terminology-Flashcards/docs/play/PRIVACY_POLICY.md` — SHA256 `34719986ad7331fcada0f8e2700eeb80c663aa894dfc55a976cb7676b6de963d`
- `Medical-Terminology-Flashcards/docs/play/READINESS.md` — SHA256 `e520846c2a4e7b2482ae6035eaaa8fb0e287a43e7bc77034fededbba39e527ac`
- `Medical-Terminology-Flashcards/docs/RELEASE_ISSUES.md` — SHA256 `c248a9bd577f76b05872aadd0f6b7e653ef009d66af8769358b12cfeb500171e`
- `Medical-Terminology-Flashcards/app/src/main/AndroidManifest.xml` — SHA256 `341ce09910833287b85268a30c9db88452d29bdf248a6bf6f288aaa9731fecc1`
- `Medical-Terminology-Flashcards/app/build.gradle.kts` — SHA256 `bfa64017db78a01e6fb75b5f2cc13abc3c3b8ba84e54b117fc29399854ab9350`

Outstanding:
- Production educational content is absent. Do not publish the listing as a usable released learning product or reuse synthetic test screenshots.
- Final audience, health declaration, account type, advertising configuration, Data safety and manual accessibility/device checks remain open.
- The existing app's embedded policy and provisional URL still require a governed update to match this public policy before distribution.


See VALIDATION.md for completed builds, screenshot preparation and remaining release checks. Earlier screenshot action items above now mean revalidation against the final signed upload artifact.
