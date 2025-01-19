const API_URL = "http://127.0.0.1:8000"; // Asegúrate de que esta URL sea correcta.

export const login = async (username, password) => {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      throw new Error("Credenciales incorrectas.");
    }

    const data = await response.json();
    // Guardar token y rol en localStorage
    localStorage.setItem("token", data.token);
    localStorage.setItem("role", data.role);

    return data.role; // Retornar el rol para redirigir al usuario.
  } catch (error) {
    throw error;
  }
};

export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
};

export const getRole = () => localStorage.getItem("role");
