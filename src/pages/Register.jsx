import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

const Register = () => {
    const [nombre, setNombre] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [tipoUsuario, setTipoUsuario] = useState("entrenador");
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            await api.post("/users/register", {
                nombre,
                email,
                password,
                tipo_usuario: tipoUsuario,
            });
            alert("¡Registro exitoso! Ahora puedes iniciar sesión.");
            navigate("/");
        } catch (error) {
            // Revisa si la respuesta del backend contiene un detalle del error
            const errorMessage = error.response?.data?.detail || "Error inesperado al registrarse";
            console.error("Error al registrarse:", errorMessage); // Imprime el error en la consola
            alert(`Error al registrarse: ${errorMessage}`); // Muestra el mensaje de error al usuario
        }
    };
    

    return (
        <div>
            <h2>Registrarse</h2>
            <form onSubmit={handleRegister}>
                <input
                    type="text"
                    placeholder="Nombre"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                />
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
                <select value={tipoUsuario} onChange={(e) => setTipoUsuario(e.target.value)}>
                    <option value="entrenador">Entrenador</option>
                    <option value="cliente">Cliente</option>
                </select>
                <button type="submit">Registrarse</button>
            </form>
            <p>¿Ya tienes una cuenta?</p>
            <button onClick={() => navigate("/")}>Iniciar sesión</button>
        </div>
    );
};

export default Register;
