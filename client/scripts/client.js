const queries = new URLSearchParams(location.search);
const res = document.getElementById("result");
const form = document.querySelector("form");
const comitato = document.getElementById("comitato");
const qualifica = document.getElementById("qualifica");
const peso = document.getElementById("peso");

function displayLoading() {
    res.hidden = false;
    if (res.classList.contains("err")) res.classList.remove("err");
    if (res.classList.contains("succ")) res.classList.remove("succ");
    res.classList.add("loading");
    res.textContent = "⏳ Sto cercando gli atleti...";
}

function isValidQuery() {
    return queries.size === 1 && (queries.has("error") || queries.has("success"));
}

function handleError(err = -1) {
    switch (err) {
        case 1: res.textContent = "❌ Qualifica è obbligatoria"; break;
        case 2: res.textContent = "❌ Nome file è obbligatorio"; break;
        case 3: res.textContent = "❌ Numero minimo match non valido"; break;
        case 4: res.textContent = "❌ Numero massimo match non valido"; break;
        case 5: res.textContent = "❌ Min non può essere maggiore di max"; break;
        case 6: res.textContent = "❌ Nessun atleta trovato"; break;
        case 7: res.textContent = "❌ Errore del server"; break;
        case 8: res.textContent = "❌ File non trovato"; break;
        case 9: res.textContent = "❌ Errore caricamento dati"; break;
        default: return;
    }
    res.classList.remove("loading");
    res.classList.add("err");
    res.hidden = false;
}

function handleSuccess(succ = -1) {
    res.classList.remove("loading");
    if (succ === 1) {
        res.classList.add("succ");
        res.hidden = false;
        res.textContent = "✅ File Excel generato!";
        res.style.cursor = "pointer";
        window.location.href = "/download";
    }
}

function displayResult() {
    if (!isValidQuery()) return;

    if (queries.has("error"))
        handleError(Number(queries.get("error")));
    else if (queries.has("success"))
        handleSuccess(Number(queries.get("success")));
}

async function fetchQualifiche() {
    await fetch("/api/qualifiche")
        .then(response => response.text())
        .then(html => {
            qualifica.innerHTML = '<option value="">Seleziona qualifica...</option>' + html;
        })
        .catch(() => {
            qualifica.innerHTML = '<option value="">Errore caricamento qualifiche</option>';
        });
}

function fetchPesi() {
    fetch("/api/pesi")
        .then(response => response.text())
        .then(html => {
            peso.innerHTML = '<option value="">Seleziona peso...</option>' + html;
        })
        .catch(() => {
            peso.innerHTML = '<option value="">Errore caricamento pesi</option>';
        });
}

function handleChangeComitato() {
    const comitatoId = comitato.value;
    if (!comitatoId) return;

    fetch(`/api/update/comitato/${comitatoId}`);
}

function handleChangeQualifica() {
    const qualificaId = qualifica.value;

    if (!qualificaId) {
        peso.hidden = true;
        peso.value = "";
        return;
    }

    fetch(`/api/update/qualifica/${qualificaId}`)
        .then(() => {
            peso.hidden = false;
            peso.value = "";
            fetchPesi();
        });
}

function handleChangePeso() {
    const pesoId = peso.value;
    if (!pesoId) return;

    fetch(`/api/update/peso/${pesoId}`);
}

comitato.addEventListener("change", handleChangeComitato);
qualifica.addEventListener("change", handleChangeQualifica);
peso.addEventListener("change", handleChangePeso);
form.addEventListener("submit", displayLoading);

window.addEventListener("load", async () => {
    await fetchQualifiche();
    displayResult();
});