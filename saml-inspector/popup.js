let currentIndex = 0;
let payloadsWithTime = [];
let list;  // Declare globally so all functions can access it

function prettyPrintXml(xml) {
  const PADDING = '  ';
  const reg = /(>)(<)(\/*)/g;
  let xmlFormatted = '';
  let pad = 0;

  xml = xml.replace(reg, '$1\r\n$2$3');
  xml.split('\r\n').forEach((node) => {
    let indent = 0;
    if (node.match(/.+<\/\w[^>]*>$/)) indent = 0;
    else if (node.match(/^<\/\w/)) pad = Math.max(pad - 1, 0);
    else if (node.match(/^<\w[^>]*[^\/]>.*$/)) indent = 1;

    const padding = PADDING.repeat(pad);
    xmlFormatted += padding + node + '\r\n';
    pad += indent;
  });

  return xmlFormatted.trim();
}

function decodeBase64Xml(b64) {
  try {
    const xmlString = atob(b64);
    return prettyPrintXml(xmlString);
  } catch (e) {
    return "Failed to decode SAML: " + e.message;
  }
}

function updatePayloadList() {
  if (!list) {
    console.error("Payload list element is not ready yet.");
    return;
  }

  chrome.storage.local.get({ samlPayloadsWithTime: [] }, (result) => {
    payloadsWithTime = result.samlPayloadsWithTime;
    list.innerHTML = '';
    payloadsWithTime.forEach((entry, index) => {
      const item = document.createElement("li");
      const timeLabel = entry.time || "Unknown time";
      item.textContent = `Payload ${index + 1} @ ${timeLabel}`;
      item.addEventListener("click", () => {
        currentIndex = index;
        renderCurrent();
      });
      list.appendChild(item);
    });
    renderCurrent();
  });
}

function renderCurrent() {
  const timestampDiv = document.getElementById("timestamp");
  const payloadDiv = document.getElementById("payload");
  const nextBtn = document.getElementById("nextBtn");
  const currentLabel = document.getElementById("currentLabel");

  if (payloadsWithTime.length > 0) {
    const { payload, time } = payloadsWithTime[currentIndex];
    timestampDiv.textContent = `Captured at: ${time}`;
    const wasExpanded = payloadDiv.classList.contains('expanded');
    payloadDiv.textContent = decodeBase64Xml(payload);
    if (wasExpanded) {
      payloadDiv.classList.add('expanded');
    } else {
      payloadDiv.classList.remove('expanded');
    }
    currentLabel.textContent = `Payload ${currentIndex + 1} @ ${time}`;

    nextBtn.disabled = payloadsWithTime.length <= 1;
    nextBtn.textContent = nextBtn.disabled ? "No More Captures" : "Next";
  } else {
    timestampDiv.textContent = "No captures yet.";
    payloadDiv.textContent = "Waiting for captures...";
    nextBtn.disabled = true;
    nextBtn.textContent = "No Captures";
    currentLabel.textContent = "";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  list = document.getElementById("payloadList");
  const clearBtn = document.getElementById("clearBtn");

  clearBtn.addEventListener("click", () => {
    chrome.storage.local.set({ samlPayloadsWithTime: [] }, () => {
      payloadsWithTime = [];
      list.innerHTML = '';
      renderCurrent();
    });
  });

  updatePayloadList();

  document.getElementById("nextBtn").addEventListener("click", () => {
    if (payloadsWithTime.length > 0) {
      currentIndex = (currentIndex + 1) % payloadsWithTime.length;
      renderCurrent();
    }
  });

  document.getElementById("prevBtn").addEventListener("click", () => {
    if (payloadsWithTime.length > 0) {
      currentIndex = (currentIndex - 1 + payloadsWithTime.length) % payloadsWithTime.length;
      renderCurrent();
    }
  });

  document.getElementById("payload").addEventListener("click", () => {
    document.getElementById("payload").classList.toggle('expanded');
  });

  document.getElementById("copyBtn").addEventListener("click", () => {
    const payloadText = document.getElementById("payload").textContent;
    navigator.clipboard.writeText(payloadText).then(() => {
      console.log("Payload copied to clipboard.");
    }).catch(err => {
      console.error("Failed to copy payload:", err);
    });
  });
});
