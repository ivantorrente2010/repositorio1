import React, { useEffect, useState } from "react";
import api from "../services/api";
import Header from "../components/Header"; // Importa el Header

const TrainerPage = () => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedClient, setSelectedClient] = useState("");
  const [planDescription, setPlanDescription] = useState("");
  const [message, setMessage] = useState("");

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      console.log("Token enviado:", token); // Verificar el token almacenado en localStorage
  
      if (!token) {
        setMessage("No se encontró un token. Por favor, inicia sesión.");
        return;
      }
  
      const headers = { Authorization: `Bearer ${token}` };
  
      console.log("Datos enviados al backend:", {
        descripcion: planDescription,
        cliente_id: selectedClient,
      }); // Verificar los datos que se envían
  
      // Crear un plan de nutrición para el cliente seleccionado
      const response = await api.post(
        "/nutrition-plans/",
        {
          descripcion: planDescription,
          cliente_id: selectedClient,
        },
        { headers }
      );
  
      console.log("Respuesta del backend:", response.data); // Verificar la respuesta del backend
      setMessage("Plan de nutrición asignado con éxito.");
      setPlanDescription("");
      setSelectedClient("");
    } catch (error) {
      console.error("Error al asignar el plan de nutrición:", error);
      if (error.response && error.response.status === 401) {
        setMessage("No autorizado. Verifica el token.");
      } else {
        setMessage("Hubo un error al asignar el plan de nutrición.");
      }
    }
  };
  

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

      {/* Formulario para asignar un plan de nutrición */}
      <h2>Asignar Plan de Nutrición</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="client">Seleccionar Cliente:</label>
          <select
            id="client"
            value={selectedClient}
            onChange={(e) => setSelectedClient(e.target.value)}
            required
          >
            <option value="">Selecciona un cliente</option>
            {clients.map((client) => (
              <option key={client.id} value={client.id}>
                {client.nombre} (ID: {client.id})
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="description">Descripción del Plan:</label>
          <textarea
            id="description"
            value={planDescription}
            onChange={(e) => setPlanDescription(e.target.value)}
            required
          />
        </div>
        <button type="submit">Asignar Plan</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default TrainerPage;
