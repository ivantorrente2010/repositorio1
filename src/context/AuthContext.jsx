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
        localStorage.removeItem("token");
    };

    // Actualizar el estado si cambia el localStorage (opcional)
    useEffect(() => {
        const handleStorageChange = () => {
            setRole(localStorage.getItem("role"));
        };
        window.addEventListener("storage", handleStorageChange);
        return () => window.removeEventListener("storage", handleStorageChange);
    }, []);

    return (
        <AuthContext.Provider value={{ role, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
