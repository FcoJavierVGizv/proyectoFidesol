const resultado = document.getElementById("resultado");

document.getElementById("verTodos").addEventListener("click", () => {
  fetch("https://restcountries.com/v3.1/all")
    .then(res => res.json())
    .then(data => mostrarPaises(data));
});

document.getElementById("buscarNombre").addEventListener("click", () => {
  const nombre = document.getElementById("nombreInput").value;
  fetch(`https://restcountries.com/v3.1/name/${nombre}`)
    .then(res => res.json())
    .then(data => mostrarPaises(data));
});

document.getElementById("filtroContinente").addEventListener("change", (e) => {
  const region = e.target.value;
  if (region) {
    fetch(`https://restcountries.com/v3.1/region/${region}`)
      .then(res => res.json())
      .then(data => mostrarPaises(data));
  }
});

document.getElementById("filtrar").addEventListener("click", () => {
  const min = parseInt(document.getElementById("poblMin").value) || 0;
  const max = parseInt(document.getElementById("poblMax").value) || Infinity;
  const idiomaBuscado = document.getElementById("idiomaInput").value.toLowerCase();

  fetch("https://restcountries.com/v3.1/all")
    .then(res => res.json())
    .then(data => {
      const filtrados = data.filter(pais => {
        const poblacion = pais.population || 0;

        const idiomas = pais.languages ? Object.values(pais.languages).map(i => i.toLowerCase()) : [];
        const idiomaIncluido = idiomaBuscado === "" || idiomas.includes(idiomaBuscado);

        return poblacion >= min && poblacion <= max && idiomaIncluido;
      });

      mostrarPaises(filtrados);
    });
});

function mostrarPaises(paises) {
  resultado.innerHTML = "";
  paises.forEach(pais => {
    resultado.innerHTML += `
      <div>
        <h2>${pais.name.common}</h2>
        <p><strong>Capital:</strong> ${pais.capital ? pais.capital[0] : 'N/A'}</p>
        <p><strong>Región:</strong> ${pais.region}</p>
        <p><strong>Población:</strong> ${pais.population.toLocaleString()}</p>
        <p><strong>Idiomas:</strong> ${pais.languages ? Object.values(pais.languages).join(", ") : 'N/A'}</p>
        <img src="${pais.flags.png}" width="100" />
      </div>
      <hr />
    `;
  });
}
