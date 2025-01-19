import React, { useEffect, useState } from "react";
import api from "../services/api";
import Header from "../components/Header"; // Importa el Header

const TrainerPage = () => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        // Obtener clientes asignados al entrenador
        const response = await api.get("/users/", { headers });
        const allUsers = response.data;

        // Filtrar para mostrar solo clientes
        const clientUsers = allUsers.filter((user) => user.tipo_usuario === "cliente");
        setClients(clientUsers);
        setLoading(false);
      } catch (error) {
        console.error("Error al cargar los clientes:", error);
        setLoading(false);
      }
    };

    fetchClients();
  }, []);

  if (loading) {
    return <p>Cargando clientes...</p>;
  }

  return (
    <div>
      {/* Header con el botón de Logout */}
      <Header />
      <h1>Panel del Entrenador</h1>
      <h2>Mis Clientes</h2>
      {clients.length > 0 ? (
        <ul>
          {clients.map((client) => (
            <li key={client.id}>
              <h3>{client.nombre}</h3>
              <p>Email: {client.email}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No tienes clientes asignados.</p>
      )}
    </div>
  );
};

export default TrainerPage;


