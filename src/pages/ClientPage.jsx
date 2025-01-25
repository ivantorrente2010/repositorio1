import React, { useEffect, useState } from "react";
import api from "../services/api";
import Header from "../components/Header";

const ClientPage = () => {
  const [routines, setRoutines] = useState([]);
  const [nutritionPlans, setNutritionPlans] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem("token");
      const clienteId = localStorage.getItem("cliente_id");
      const headers = { Authorization: `Bearer ${token}` };

      if (!clienteId) {
        console.error("No se encontró cliente_id en localStorage");
        return;
      }

      console.log("Token enviado:", token);
      console.log("Cliente ID obtenido:", clienteId);

      try {
        // Obtener planes de nutrición
        const nutritionPlansResponse = await api.get(`/nutrition-plans/client/${clienteId}`, { headers });
        console.log("Respuesta del backend para planes de nutrición:", nutritionPlansResponse.data);
        setNutritionPlans(nutritionPlansResponse.data);

        // Obtener rutinas del cliente
        const routinesResponse = await api.get(`/routines/client/${clienteId}`, { headers });
        console.log("Respuesta del backend para rutinas:", routinesResponse.data);
        setRoutines(routinesResponse.data);

        // Obtener métricas del cliente
        const metricsResponse = await api.get(`/metrics/${clienteId}`, { headers });
        console.log("Métricas obtenidas del backend:", metricsResponse.data);
        setMetrics(metricsResponse.data);
      } catch (error) {
        console.error("Error al cargar los datos del cliente:", error.response?.data || error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <p>Cargando datos...</p>;
  }

  return (
    <div>
      <Header />
      <h1>Panel del Cliente</h1>

      <section>
        <h2>Mis Rutinas</h2>
        {routines.length > 0 ? (
          <ul>
            {routines.map((routine) => (
              <li key={routine.id}>
                <h3>{routine.nombre}</h3>
                <p>{routine.descripcion}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No tienes rutinas asignadas.</p>
        )}
      </section>

      <section>
        <h2>Mis Planes de Nutrición</h2>
        {nutritionPlans.length > 0 ? (
          <ul>
            {nutritionPlans.map((plan) => (
              <li key={plan.id}>
                <p>{plan.descripcion}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No tienes planes de nutrición asignados.</p>
        )}
      </section>

      <section>
        <h2>Mis Métricas</h2>
        {metrics.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Peso</th>
                <th>Grasa Corporal</th>
              </tr>
            </thead>
            <tbody>
              {metrics.map((metric) => (
                <tr key={metric.id}>
                  <td>{metric.fecha ? new Date(metric.fecha).toLocaleDateString() : "N/A"}</td>
                  <td>{metric.peso || "N/A"} kg</td>
                  <td>{metric.grasa_corporal || "N/A"}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No tienes métricas registradas.</p>
        )}
      </section>
    </div>
  );
};

export default ClientPage;
