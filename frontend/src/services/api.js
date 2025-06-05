const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...this.getAuthHeaders(),
      ...options.headers,
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Authentication
  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Falha no login');
    }

    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data;
  }

  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  // User authentication and profile
  async getCurrentUser() {
    return this.request('/auth/me');
  }

  async getMyClasses() {
    return this.request('/auth/me/classes');
  }

  logout() {
    localStorage.removeItem('access_token');
  }

  // Rooms
  async getRooms() {
    return this.request('/rooms/');
  }

  async getRoom(roomId) {
    return this.request(`/rooms/${roomId}`);
  }

  // Bookings
  async getMyBookings() {
    return this.request('/bookings/my-bookings');
  }

  async createBooking(bookingData) {
    return this.request('/bookings/', {
      method: 'POST',
      body: JSON.stringify(bookingData),
    });
  }

  async updateBooking(bookingId, updateData) {
    return this.request(`/bookings/${bookingId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  }

  async cancelBooking(bookingId) {
    return this.request(`/bookings/${bookingId}`, {
      method: 'DELETE',
    });
  }

  async getAvailableSlots(roomId, date, duration = 60) {
    const params = new URLSearchParams({
      room_id: roomId,
      date: date,
      duration: duration,
    });
    return this.request(`/bookings/available-slots?${params}`);
  }

  // Admin endpoints
  async getAllUsers() {
    return this.request('/admin/users');
  }

  async getAllBookings() {
    return this.request('/admin/bookings');
  }

  async createRoom(roomData) {
    return this.request('/admin/rooms', {
      method: 'POST',
      body: JSON.stringify(roomData),
    });
  }
  async updateRoom(roomId, updateData) {
    return this.request(`/admin/rooms/${roomId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  }

  async deleteRoom(roomId) {
    return this.request(`/admin/rooms/${roomId}`, {
      method: 'DELETE',
    });
  }

  // Classes endpoints (admin only)
  async getAllClasses() {
    return this.request('/classes/');
  }

  async getClass(classId) {
    return this.request(`/classes/${classId}`);
  }

  async createClass(classData) {
    return this.request('/classes/', {
      method: 'POST',
      body: JSON.stringify(classData),
    });
  }

  async updateClass(classId, updateData) {
    return this.request(`/classes/${classId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  }

  async deleteClass(classId) {
    return this.request(`/classes/${classId}`, {
      method: 'DELETE',
    });
  }

  async getClassesByRoom(roomId, startDate = null, endDate = null) {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    const queryString = params.toString();
    return this.request(`/classes/room/${roomId}${queryString ? '?' + queryString : ''}`);
  }

  // Students endpoints (admin only)
  async getAllStudents() {
    return this.request('/students/');
  }

  async getStudent(studentId) {
    return this.request(`/students/${studentId}`);
  }

  async createStudent(studentData) {
    return this.request('/students/', {
      method: 'POST',
      body: JSON.stringify(studentData),
    });
  }

  async updateStudent(studentId, updateData) {
    return this.request(`/students/${studentId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  }

  async deleteStudent(studentId) {
    return this.request(`/students/${studentId}`, {
      method: 'DELETE',
    });
  }

  async getStudentsByRoom(roomId) {
    return this.request(`/students/room/${roomId}`);
  }
}

export default new ApiService();
