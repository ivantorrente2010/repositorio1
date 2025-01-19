import { createContext, useContext, useState, useEffect } from "react";

// Crear el contexto
const AuthContext = createContext();

// Hook para acceder al contexto
export const useAuth = () => {
    return useContext(AuthContext);
};

// Proveedor del contexto
export const AuthProvider = ({ children }) => {
    const [role, setRole] = useState(localStorage.getItem("role") || null);

    // Función para iniciar sesión y actualizar el rol
    const login = (newRole) => {
        setRole(newRole);
        localStorage.setItem("role", newRole);
    };

    // Función para cerrar sesión
    const logout = () => {
        setRole(null);
        localStorage.removeItem("role");
        localStorage.removeItem("token"); // Elimina el token de autenticación
    };

    // Sincronizar el estado con los cambios en localStorage
    useEffect(() => {
        const handleStorageChange = () => {
            const storedRole = localStorage.getItem("role");
            setRole(storedRole);
        };
        window.addEventListener("storage", handleStorageChange);

        return () => {
            window.removeEventListener("storage", handleStorageChange);
        };
    }, []);

    return (
        <AuthContext.Provider value={{ role, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
