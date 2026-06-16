// Este script se inyecta automáticamente en Gmail
// Su único trabajo es leer el email abierto y responder cuando popup.js lo pida

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

  // Solo respondemos al mensaje que nos manda popup.js
  if (message.action === 'getEmailContent') {

    // Gmail muestra el email en un elemento con este atributo
    const emailBody = document.querySelector('[data-message-id]')

    if (emailBody) {
      sendResponse({ text: emailBody.innerText })
    } else {
      // No hay email abierto en este momento
      sendResponse({ text: null })
    }
  }

  // Importante: return true le dice a Chrome que la respuesta es asíncrona
  return true
})