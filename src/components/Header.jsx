import React from "react";
import { useAuth } from "../context/AuthContext";

const Header = () => {
  const { logout } = useAuth();

  const handleLogout = () => {
    logout(); // Llama a la función de logout del contexto
  };

  return (
    <header style={{ display: "flex", justifyContent: "space-between", padding: "10px", backgroundColor: "#f5f5f5" }}>
      <h1>Gimnasio Fitness</h1>
      <button onClick={handleLogout} style={{ padding: "5px 10px", cursor: "pointer" }}>
        Cerrar Sesión
      </button>
    </header>
  );
};

export default Header;

