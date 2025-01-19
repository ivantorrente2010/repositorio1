import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext"; // Importamos el contexto de autenticación

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const { login } = useAuth(); // Usamos el método `login` del contexto

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post("/auth/login", {
                email,
                password,
            });

            // Log para depurar el rol recibido
            console.log("Role recibido desde backend:", response.data.role);

            // Actualizar el contexto con el rol del usuario
            login(response.data.role); // Actualiza el estado global del rol

            alert("¡Inicio de sesión exitoso!");

            // Redirigir al dashboard, el rol se manejará dinámicamente en App.jsx
            navigate("/dashboard");
        } catch (error) {
            console.error("Error completo:", error);
            const errorMessage =
                error.response?.data?.detail || "Error inesperado al iniciar sesión";
            alert(`Error al iniciar sesión: ${errorMessage}`);
        }
    };

    return (
        <div>
            <h2>Inicio de Sesión</h2>
            <form onSubmit={handleLogin}>
                <input
                    type="email"
                    placeholder="Correo electrónico"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Contraseña"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Iniciar sesión</button>
            </form>
            <p>¿No tienes una cuenta?</p>
            <button onClick={() => navigate("/register")}>Registrarse</button>
        </div>
    );
};

export default Login;
