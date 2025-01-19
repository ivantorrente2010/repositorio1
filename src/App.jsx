import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import AdminPage from "./pages/AdminPage";
import TrainerPage from "./pages/TrainerPage";
import ClientPage from "./pages/ClientPage";
import { useAuth } from "./context/AuthContext"; // Usa el contexto para obtener el rol

function App() {
    const { role } = useAuth(); // Obtenemos el rol desde el contexto

    return (
        <Router>
            <Routes>
                {/* Ruta para el login */}
                <Route path="/" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* Rutas protegidas según el rol */}
                {role === "admin" && <Route path="/dashboard" element={<AdminPage />} />}
                {role === "entrenador" && <Route path="/dashboard" element={<TrainerPage />} />}
                {role === "cliente" && <Route path="/dashboard" element={<ClientPage />} />}

                {/* Redirección genérica */}
                <Route
                    path="*"
                    element={
                        role ? (
                            <Navigate to="/dashboard" />
                        ) : (
                            <Navigate to="/" />
                        )
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
