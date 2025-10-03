// import { useState } from "react";
// import { searchRecipes } from "./services/api";

// export default function App() {
//   const [query, setQuery] = useState("");
//   const [results, setResults] = useState([]);

//   const handleSearch = async () => {
//     const data = await searchRecipes(query);
//     setResults(data);
//   };

//   return (
//     <div className="p-6">
//       <h1 className="text-2xl font-bold mb-4">🍳 CamCook Buscador</h1>
//       <input
//         type="text"
//         value={query}
//         onChange={(e) => setQuery(e.target.value)}
//         placeholder="Buscar receta o ingrediente..."
//         className="border p-2 rounded"
//       />
//       <button onClick={handleSearch} className="ml-2 bg-blue-500 text-white p-2 rounded">
//         Buscar
//       </button>
//       <div className="mt-4 grid gap-4">
//         {results.map((r, i) => (
//           <div key={i} className="p-4 border rounded shadow">
//             <h2 className="font-bold">{r.title}</h2>
//             <p><b>Ingredientes:</b> {r.ingredients.join(", ")}</p>
//             <p>{r.instructions}</p>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }
import { useState } from "react";
import SearchResults from "./components/SearchResults";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const search = async () => {
    const res = await fetch(`http://localhost:8000/search?q=${query}`);
    const data = await res.json();
    setResults(data.hits);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>CamCook Search</h1>
      <input
        type="text"
        value={query}
        placeholder="Buscar receta..."
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={search}>Buscar</button>
      <SearchResults results={results} />
    </div>
  );
}

export default App;
