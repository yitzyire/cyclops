chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    let captured = null;

    if (details.method === "POST" && details.requestBody) {
      const formData = details.requestBody.formData;
      if (formData && (formData.SAMLRequest || formData.SAMLResponse)) {
        captured = formData.SAMLRequest ? formData.SAMLRequest[0] : formData.SAMLResponse[0];
      }
    } else if (details.url.includes("SAMLRequest=") || details.url.includes("SAMLResponse=")) {
      const url = new URL(details.url);
      captured = url.searchParams.get("SAMLRequest") || url.searchParams.get("SAMLResponse");
    }

    if (captured) {
      const entry = { payload: captured, time: new Date().toLocaleString() };
      chrome.storage.local.get({ samlPayloadsWithTime: [] }, (result) => {
        const updated = result.samlPayloadsWithTime.concat([entry]);
        chrome.storage.local.set({ samlPayloadsWithTime: updated });
      });
    }
  },
  { urls: ["<all_urls>"] },
  ["requestBody"]
);
