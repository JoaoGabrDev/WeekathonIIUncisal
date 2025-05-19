 function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(item => {
      const [key, val] = item.trim().split('=');
      if (key === name) cookieValue = decodeURIComponent(val);
    });
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
  const cpfInput = document.getElementById("cpf-input");
  cpfInput.addEventListener("input", e => {
    let v = e.target.value.replace(/\D/g, "");
    if (v.length > 11) v = v.slice(0, 11);
    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    e.target.value = v;
  });
});

function buscarQrCode() {
  const cpf = document.getElementById('cpf-input').value.replace(/\D/g, '');
  if (cpf.length !== 11) { alert("CPF inválido."); return; }

  fetch(`/api/qr/${cpf}/`)
    .then(res => res.ok ? res.json() : Promise.reject("Paciente não encontrado"))
    .then(data => {
      document.getElementById('qrCodeImagem').src = data.qr_code_base64;
    })
    .catch(err => alert(err));
}

function gerarQrCode() {
  const nome        = document.getElementById('fullName').value.trim();
  const cpf         = document.getElementById('cpf-input').value.replace(/\D/g, '');
  const tipo        = document.getElementById('bloodType').value;
  const alergias    = document.getElementById('alergias').value.trim();
  const medicamento = document.getElementById('medicamento').value.trim();
  const dosagem     = document.getElementById('dosagem').value.trim();
  const frequencia  = document.getElementById('frequencia').value.trim();
  const observacoes = document.getElementById('observacoes').value.trim();

  if (!nome || cpf.length !== 11 || !tipo || !medicamento || !dosagem || !frequencia) {
    alert("Preencha todos os campos obrigatórios (incluindo prescrição).");
    return;
  }

  const payload = {
    nome,
    cpf,
    tipo_sanguineo: tipo,
    alergias,
    ativo: true,
    prescricao: {
      medicamento,
      dosagem,
      frequencia,
      observacoes
    }
  };

  fetch('/api/cadastrar_gerar_qr/', {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie('csrftoken')
    },
    body: JSON.stringify(payload)
  })
  .then(async res => {
    if (!res.ok) {
      const err = await res.json();
      alert("Erro ao cadastrar:\n" + JSON.stringify(err));
      return Promise.reject(err);
    }
    return res.json();
  })
  .then(data => {
    document.getElementById('qrCodeImagem').src = data.qr_code_base64;
  })
  .catch(console.error);
}