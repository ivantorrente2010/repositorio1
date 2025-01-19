import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext"; // Importamos el contexto

const AdminPage = () => {
  const { logout } = useAuth(); // Accedemos a la función de logout
  const navigate = useNavigate();

  const handleLogout = () => {
    logout(); // Limpia el estado y localStorage
    navigate("/"); // Redirige al login
  };

  return (
    <div>
      <h1>Admin Panel</h1>
      <p>Gestión de usuarios y configuraciones del sistema.</p>
      <button onClick={handleLogout}>Cerrar Sesión</button>
    </div>
  );
};

export default AdminPage;

