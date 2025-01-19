import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { AuthProvider } from "./context/AuthContext.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    {/* Envuelve la aplicación con AuthProvider */}
    <AuthProvider>
      <App />
    </AuthProvider>
  </StrictMode>
);

