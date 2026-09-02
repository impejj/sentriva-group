const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }));
}

const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

const SENTRIVA_SUBMISSION_MODE = window.__SENTRIVA_SUBMISSION_MODE__ === 'API'
  ? 'API'
  : 'EMAIL_FALLBACK';
const SENTRIVA_API_BASE = typeof window.__SENTRIVA_API_BASE__ === 'string'
  ? window.__SENTRIVA_API_BASE__.trim().replace(/\/$/, '')
  : '';

const fieldLabel = (field) => {
  const label = field.closest('label');
  if (!label) return field.name.replaceAll('_', ' ');
  const clone = label.cloneNode(true);
  clone.querySelectorAll('input,textarea,select').forEach((node) => node.remove());
  return clone.textContent.trim() || field.name.replaceAll('_', ' ');
};

const buildEmailHref = (form) => {
  const recipient = form.dataset.recipient;
  const subject = form.dataset.subject || 'Sentriva Group';
  const lines = [];

  form.querySelectorAll('fieldset').forEach((fieldset) => {
    const legend = fieldset.querySelector('legend');
    if (legend) lines.push(legend.textContent.trim());
    fieldset.querySelectorAll('input,textarea,select').forEach((field) => {
      if (!field.name || field.type === 'file' || field.type === 'submit') return;
      const value = String(field.value || '').trim();
      if (value) lines.push(`${fieldLabel(field)}: ${value}`);
    });
    lines.push('');
  });

  lines.push('Documentación: adjuntar al correo si corresponde.');
  return `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
};

const serializeApiPayload = (form) => {
  const payload = {};
  const data = new FormData(form);
  data.forEach((value, key) => {
    if (value instanceof File) return;
    const normalized = String(value).trim();
    if (normalized) payload[key] = normalized;
  });
  return payload;
};

const ensureFormStatus = (form) => {
  let status = form.querySelector('[data-form-status]');
  if (status) return status;
  status = document.createElement('p');
  status.className = 'form-note wide';
  status.dataset.formStatus = '';
  status.setAttribute('role', 'status');
  status.setAttribute('aria-live', 'polite');
  const actions = form.querySelector('.form-actions');
  if (actions) actions.before(status);
  else form.append(status);
  return status;
};

const setStatusMessage = (status, message) => {
  status.replaceChildren();
  status.append(document.createTextNode(message));
};

const offerEmailFallback = (form, status) => {
  setStatusMessage(status, 'No se pudo verificar el envío por API. Sus datos siguen en el formulario. ');
  const fallback = document.createElement('a');
  fallback.href = buildEmailHref(form);
  fallback.textContent = 'Usar envío por email';
  fallback.className = 'text-link';
  status.append(fallback);
};

const submitViaApi = async (form) => {
  const endpoint = form.dataset.apiEndpoint;
  if (!endpoint || !endpoint.startsWith('/api/v1/')) throw new Error('API_ENDPOINT_MISSING');
  if (!SENTRIVA_API_BASE) throw new Error('API_BASE_MISSING');

  const response = await fetch(`${SENTRIVA_API_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'omit',
    body: JSON.stringify(serializeApiPayload(form)),
  });
  const result = await response.json().catch(() => null);
  if (!response.ok || result?.success !== true || !result?.data?.id) {
    throw new Error('API_SUBMISSION_NOT_VERIFIED');
  }
  return result;
};

document.querySelectorAll('[data-email-form]').forEach((form) => {
  const submitButton = form.querySelector('button[type="submit"]');
  if (SENTRIVA_SUBMISSION_MODE === 'API' && submitButton) {
    submitButton.dataset.emailFallbackLabel = submitButton.textContent || '';
    submitButton.textContent = 'Enviar al entorno de prueba';
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    if (SENTRIVA_SUBMISSION_MODE !== 'API') {
      window.location.href = buildEmailHref(form);
      return;
    }

    const status = ensureFormStatus(form);
    setStatusMessage(status, 'Enviando y verificando recepción…');
    if (submitButton) submitButton.disabled = true;

    try {
      const result = await submitViaApi(form);
      setStatusMessage(status, `Recibido en el entorno de prueba. ID: ${result.data.id}`);
    } catch (_) {
      offerEmailFallback(form, status);
    } finally {
      if (submitButton) submitButton.disabled = false;
    }
  });
});
