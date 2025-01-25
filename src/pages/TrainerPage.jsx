import React, { useEffect, useState } from "react";
import api from "../services/api";
import Header from "../components/Header";

const TrainerPage = () => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedClient, setSelectedClient] = useState("");
  const [planDescription, setPlanDescription] = useState("");
  const [routineName, setRoutineName] = useState("");
  const [routineDescription, setRoutineDescription] = useState("");
  const [metricWeight, setMetricWeight] = useState("");
  const [metricBodyFat, setMetricBodyFat] = useState("");
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

  const handlePlanSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");

      if (!token) {
        setMessage("No se encontró un token. Por favor, inicia sesión.");
        return;
      }

      const headers = { Authorization: `Bearer ${token}` };

      // Crear un plan de nutrición para el cliente seleccionado
      const response = await api.post(
        "/nutrition-plans/",
        {
          descripcion: planDescription,
          cliente_id: selectedClient,
        },
        { headers }
      );

      console.log("Plan asignado:", response.data);
      setMessage("Plan de nutrición asignado con éxito.");
      setPlanDescription("");
      setSelectedClient("");
    } catch (error) {
      console.error("Error al asignar el plan de nutrición:", error);
      setMessage(error.response?.data?.detail || "Error al asignar el plan.");
    }
  };

  const handleRoutineSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");

      if (!token) {
        setMessage("No se encontró un token. Por favor, inicia sesión.");
        return;
      }

      const headers = { Authorization: `Bearer ${token}` };

      // Crear una rutina para el cliente seleccionado
      const response = await api.post(
        "/routines/",
        {
          nombre: routineName,
          descripcion: routineDescription,
          cliente_id: selectedClient,
        },
        { headers }
      );

      console.log("Rutina asignada:", response.data);
      setMessage("Rutina asignada con éxito.");
      setRoutineName("");
      setRoutineDescription("");
      setSelectedClient("");
    } catch (error) {
      console.error("Error al asignar la rutina:", error);
      setMessage(error.response?.data?.detail || "Error al asignar la rutina.");
    }
  };

  const handleMetricSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
  
      if (!token) {
        setMessage("No se encontró un token. Por favor, inicia sesión.");
        return;
      }
  
      const headers = { Authorization: `Bearer ${token}` };
  
      const response = await api.post(
        "/metrics/",
        {
          peso: parseFloat(metricWeight),
          grasa_corporal: metricBodyFat ? parseFloat(metricBodyFat) : null,
          cliente_id: parseInt(selectedClient),
        },
        { headers }
      );
  
      console.log("Métrica asignada:", response.data);
      setMessage("Métrica registrada con éxito.");
      setMetricWeight("");
      setMetricBodyFat("");
      setSelectedClient("");
    } catch (error) {
      console.error("Error al registrar la métrica:", error);
      setMessage(
        typeof error.response?.data === "string"
    ? error.response.data
    : "Error al registrar la métrica."
    );
    }
  };
  

  if (loading) {
    return <p>Cargando clientes...</p>;
  }

  return (
    <div>
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
      <form onSubmit={handlePlanSubmit}>
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
          <label htmlFor="planDescription">Descripción del Plan:</label>
          <textarea
            id="planDescription"
            value={planDescription}
            onChange={(e) => setPlanDescription(e.target.value)}
            required
          />
        </div>
        <button type="submit">Asignar Plan</button>
      </form>

      {/* Formulario para asignar una rutina */}
      <h2>Asignar Rutina</h2>
      <form onSubmit={handleRoutineSubmit}>
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
          <label htmlFor="routineName">Nombre de la Rutina:</label>
          <input
            id="routineName"
            type="text"
            value={routineName}
            onChange={(e) => setRoutineName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="routineDescription">Descripción de la Rutina:</label>
          <textarea
            id="routineDescription"
            value={routineDescription}
            onChange={(e) => setRoutineDescription(e.target.value)}
            required
          />
        </div>
        <button type="submit">Asignar Rutina</button>
      </form>

      {/* Formulario para asignar una metrica */}
      
      <h2>Registrar Métricas</h2>
      <form onSubmit={handleMetricSubmit}>
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
          <label htmlFor="metricWeight">Peso (kg):</label>
          <input
            id="metricWeight"
            type="number"
            value={metricWeight}
            onChange={(e) => setMetricWeight(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="metricBodyFat">Grasa Corporal (%):</label>
          <input
            id="metricBodyFat"
            type="number"
            value={metricBodyFat}
            onChange={(e) => setMetricBodyFat(e.target.value)}
          />
        </div>
        ¡
        <button type="submit">Registrar Métricas</button>
      </form>
      
      {message && <p>{message}</p>}
    </div>
  );
};

export default TrainerPage;
