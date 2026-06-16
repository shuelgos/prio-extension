// Esperamos a que el HTML esté listo antes de ejecutar cualquier cosa
document.addEventListener('DOMContentLoaded', () => {

  // Referencias a los elementos del HTML que vamos a manipular
  const btnAnalyze = document.getElementById('btn-analyze')
  const resultDiv  = document.getElementById('result')
  const tagsDiv    = document.getElementById('tags')
  const reasonsDiv = document.getElementById('reasons')
  const suggestion = document.getElementById('suggestion')
  const status     = document.getElementById('status')

  // Cuando el usuario clickea "Analizar email"
  btnAnalyze.addEventListener('click', async () => {

    // 1. Deshabilitamos el botón para evitar doble click
    btnAnalyze.disabled = true
    btnAnalyze.textContent = 'Analizando...'
    status.textContent = ''
    resultDiv.style.display = 'none'

    try {
      // 2. Pedimos a content.js que lea el email activo en Gmail
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true })

      const response = await chrome.tabs.sendMessage(tab.id, {
        action: 'getEmailContent'
      })

      // 3. Si no hay email abierto, avisamos al usuario
      if (!response || !response.text) {
        status.textContent = 'Abre un email en Gmail primero.'
        return
      }

      // 4. Por ahora usamos datos mock — en Semana 2 llamamos al backend real
      const result = getMockResult(response.text)

      // 5. Mostramos el resultado en el popup
      showResult(result)

    } catch (error) {
      status.textContent = 'Error al leer el email. ¿Estás en Gmail?'
      console.error('Prio error:', error)
    } finally {
      // Siempre re-habilitamos el botón al terminar
      btnAnalyze.disabled = false
      btnAnalyze.textContent = 'Analizar email'
    }
  })

  // Función que muestra el resultado en el popup
  function showResult(result) {

    // Tags de urgencia y área
    tagsDiv.innerHTML = `
      <span class="tag tag-${result.urgencia.toLowerCase()}">${result.urgencia}</span>
      <span class="area-tag">${result.area}</span>
    `

    // Razones (lista de bullets)
    reasonsDiv.innerHTML = result.razones
      .map(r => `<div class="reason">• ${r}</div>`)
      .join('')

    // Respuesta sugerida
    suggestion.textContent = result.respuesta

    // Mostramos el contenedor de resultado
    resultDiv.style.display = 'block'
  }

  // Datos de prueba — simula lo que devolverá la IA
  // Esto lo reemplazamos en Semana 2 con el fetch real al backend
  function getMockResult(emailText) {
    return {
      urgencia: 'Urgente',
      area: 'Facturación',
      razones: [
        'El usuario menciona un cobro duplicado',
        'Usa lenguaje de frustración ("esto es inaceptable")',
        'Solicita reembolso explícitamente'
      ],
      respuesta: 'Hola, entendemos tu situación y lamentamos el inconveniente. Hemos escalado tu caso al equipo de facturación y te contactaremos en menos de 24 horas con una solución.'
    }
  }

})