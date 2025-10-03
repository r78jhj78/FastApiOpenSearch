export default function SearchResults({ results }) {
  if (!results || results.length === 0) return <p>No hay resultados</p>;
  return (
    <div>
      {results.map((r, i) => (
        <div key={i} style={{ border: "1px solid #ccc", margin: "10px", padding: "10px" }}>
          <h2>{r.title}</h2>
          <img src={r.image_url} alt={r.title} style={{ width: "150px" }} />
          <p><b>Ingrediente principal:</b> {r.main_ingredient}</p>
          <p><b>Ingredientes:</b> {r.ingredients.join(", ")}</p>
          <p><b>Instrucciones:</b> {r.instructions}</p>
        </div>
      ))}
    </div>
  );
}
