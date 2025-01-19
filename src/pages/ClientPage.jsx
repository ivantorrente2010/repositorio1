import React, { useEffect, useState } from "react";
import api from "../services/api";
import Header from "../components/Header"; // Importa el Header

const ClientPage = () => {
  const [routines, setRoutines] = useState([]);
  const [nutritionPlans, setNutritionPlans] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        // Obtener rutinas del cliente
        const routinesResponse = await api.get("/routines/me", { headers });
        setRoutines(routinesResponse.data);

        // Obtener planes de nutrición
        const nutritionPlansResponse = await api.get("/nutrition-plans/me", { headers });
        setNutritionPlans(nutritionPlansResponse.data);

        // Obtener métricas
        const metricsResponse = await api.get("/metrics/me", { headers });
        setMetrics(metricsResponse.data);

        setLoading(false);
      } catch (error) {
        console.error("Error al cargar los datos del cliente:", error);
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
      {/* Header con el botón de Logout */}
      <Header />
      <h1>Panel del Cliente</h1>

      {/* Sección de rutinas */}
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

      {/* Sección de planes de nutrición */}
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

      {/* Sección de métricas */}
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
                  <td>{new Date(metric.fecha).toLocaleDateString()}</td>
                  <td>{metric.peso} kg</td>
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

