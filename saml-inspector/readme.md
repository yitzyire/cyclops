# SAML Inspector

SAML Inspector is a Chrome Extension that captures and decodes SAMLRequest and SAMLResponse messages from your browser traffic. It provides a simple popup interface to review, copy, and manage captured SAML payloads.

## Features

- Captures SAMLRequest and SAMLResponse from:
  - URLs with `SAMLRequest=` or `SAMLResponse=`
  - HTTP POST body parameters
- Lists all captured payloads with timestamps
- Pretty-prints Base64-decoded SAML XML
- Provides navigation (Next, Previous) through captured payloads
- Allows expanding and collapsing the SAML XML view
- One-click Copy Payload button
- Clear All button to reset capture history
- Fully self-contained in the popup (no DevTools panel required)

## Installation (Developer Mode)

1. Clone or download this repository.
2. Open Chrome and go to `chrome://extensions/`.
3. Enable **Developer mode** using the toggle in the top-right.
4. Click **Load unpacked**.
5. Select the folder containing this extension.

## Usage

1. Open any SAML-authenticated website or service.
2. Trigger a SAML login or response action.
3. Click the **SAML Inspector** icon in your Chrome toolbar.
4. Browse captured payloads, view their XML, or copy them.

## File Structure

- `background.js` – Captures SAML data via webRequest API
- `manifest.json` – Chrome extension configuration
- `popup.html` – Popup user interface layout
- `popup.js` – Popup logic and event handling


## Permissions

- `webRequest`: Required to capture SAML data in transit.
- `storage`: Stores captured payloads for session review.
- `host_permissions`: Grants access to all URLs (`*://*/*`).

## Roadmap

- Dark mode support
- Filtering by SAMLRequest or SAMLResponse
- Download captured payloads as files
- Automatic cleanup options (clear older captures)

## Credits

Created by [Your Name or Organization].  
Designed to simplify SAML debugging and inspection.

