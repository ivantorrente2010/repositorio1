import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post("/auth/login", {
                email,
                password,
            });
            localStorage.setItem("token", response.data.access_token);
            alert("¡Inicio de sesión exitoso!");
            navigate("/dashboard");
        } catch (error) {
            console.error("Error completo:", error); // Detalles completos del error
            console.error("Detalles de la respuesta:", error.response); // Respuesta del servidor
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
