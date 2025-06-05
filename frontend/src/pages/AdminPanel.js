import React, { useState, useEffect } from 'react';
import { format, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Users, Calendar, MapPin, Plus, Edit, Eye, GraduationCap, Trash2 } from 'lucide-react';
import apiService from '../services/api';
import { toast } from 'react-toastify';
import Navbar from '../components/Navbar';

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('bookings');  const [bookings, setBookings] = useState([]);
  const [users, setUsers] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showRoomForm, setShowRoomForm] = useState(false);
  const [showStudentForm, setShowStudentForm] = useState(false);
  const [editingRoom, setEditingRoom] = useState(null);
  const [editingStudent, setEditingStudent] = useState(null);
  const [roomForm, setRoomForm] = useState({
    name: '',
    description: '',
    capacity: 1,
    equipment: ''
  });  const [studentForm, setStudentForm] = useState({
    name: '',
    email: '',
    phone: '',
    teacher_name: '',
    room_id: '',
    weekday: '',
    start_time: '',
    end_time: '',
    notes: ''
  });  useEffect(() => {
    if (activeTab === 'bookings') {
      fetchBookings();
    } else if (activeTab === 'users') {
      fetchUsers();
    } else if (activeTab === 'rooms') {
      fetchRooms();
    } else if (activeTab === 'students') {
      fetchStudents();
      fetchRooms(); // Also fetch rooms for the dropdown
    }
  }, [activeTab]);

  const fetchBookings = async () => {
    setLoading(true);
    try {
      const bookingsData = await apiService.getAllBookings();
      setBookings(bookingsData);
    } catch (error) {
      toast.error('Falha ao buscar agendamentos');
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const usersData = await apiService.getAllUsers();
      setUsers(usersData);
    } catch (error) {
      toast.error('Falha ao buscar usuários');
    } finally {
      setLoading(false);
    }
  };
  const fetchRooms = async () => {
    setLoading(true);
    try {
      const roomsData = await apiService.getRooms();
      setRooms(roomsData);
    } catch (error) {
      toast.error('Falha ao buscar salas');
    } finally {
      setLoading(false);
    }
  };
  const fetchStudents = async () => {
    setLoading(true);
    try {
      const studentsData = await apiService.getAllStudents();
      setStudents(studentsData);
    } catch (error) {
      toast.error('Falha ao buscar estudantes');
    } finally {
      setLoading(false);
    }
  };
  const handleRoomSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingRoom) {
        await apiService.updateRoom(editingRoom.id, roomForm);
        toast.success('Sala atualizada com sucesso');
        setEditingRoom(null);
      } else {
        await apiService.createRoom(roomForm);
        toast.success('Sala criada com sucesso');
      }
      setShowRoomForm(false);
      setRoomForm({ name: '', description: '', capacity: 1, equipment: '' });
      fetchRooms();
    } catch (error) {
      toast.error(editingRoom ? 'Falha ao atualizar sala' : 'Falha ao criar sala');
    }
  };
  const handleStudentSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingStudent) {
        await apiService.updateStudent(editingStudent.id, studentForm);
        toast.success('Estudante atualizado com sucesso');
        setEditingStudent(null);
      } else {
        await apiService.createStudent(studentForm);
        toast.success('Estudante criado com sucesso');
      }
      setShowStudentForm(false);
      setStudentForm({
        name: '',
        email: '',
        phone: '',
        teacher_name: '',
        room_id: '',
        weekday: '',
        start_time: '',
        end_time: '',
        notes: ''
      });
      fetchStudents();
    } catch (error) {
      toast.error(editingStudent ? 'Falha ao atualizar estudante' : 'Falha ao criar estudante');
    }
  };

  const handleEditRoom = (room) => {
    setEditingRoom(room);
    setRoomForm({
      name: room.name,
      description: room.description,
      capacity: room.capacity,
      equipment: room.equipment || ''
    });
    setShowRoomForm(true);
  };

  const handleDeleteRoom = async (roomId, roomName) => {
    if (window.confirm(`Tem certeza que deseja excluir a sala "${roomName}"?`)) {
      try {
        await apiService.deleteRoom(roomId);
        toast.success('Sala excluída com sucesso');
        fetchRooms();
      } catch (error) {
        toast.error('Falha ao excluir sala');
      }
    }
  };

  const handleCancelRoomEdit = () => {
    setEditingRoom(null);
    setShowRoomForm(false);
    setRoomForm({ name: '', description: '', capacity: 1, equipment: '' });
  };

  const handleEditStudent = (student) => {
    setEditingStudent(student);
    setStudentForm({
      name: student.name,
      email: student.email || '',
      phone: student.phone || '',
      teacher_name: student.teacher_name,
      room_id: student.room_id,
      weekday: student.weekday,
      start_time: student.start_time,
      end_time: student.end_time,
      notes: student.notes || ''
    });
    setShowStudentForm(true);
  };

  const handleDeleteStudent = async (studentId, studentName) => {
    if (window.confirm(`Tem certeza que deseja excluir o estudante "${studentName}"?`)) {
      try {
        await apiService.deleteStudent(studentId);
        toast.success('Estudante excluído com sucesso');
        fetchStudents();
      } catch (error) {
        toast.error('Falha ao excluir estudante');
      }
    }
  };

  const handleCancelStudentEdit = () => {
    setEditingStudent(null);
    setShowStudentForm(false);
    setStudentForm({
      name: '',
      email: '',
      phone: '',
      teacher_name: '',
      room_id: '',
      weekday: '',
      start_time: '',
      end_time: '',
      notes: ''
    });
  };
  const tabs = [
    { id: 'bookings', name: 'Agendamentos', icon: Calendar },
    { id: 'users', name: 'Usuários', icon: Users },
    { id: 'rooms', name: 'Salas', icon: MapPin },
    { id: 'students', name: 'Estudantes', icon: GraduationCap },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">          <h1 className="text-3xl font-bold text-gray-900">Painel de Administração</h1>
          <p className="mt-2 text-gray-600">Gerencie usuários, salas, aulas e agendamentos.</p>
        </div>

        {/* Tab Navigation */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            {/* Bookings Tab */}
            {activeTab === 'bookings' && (
              <div className="space-y-4">                <h2 className="text-xl font-semibold text-gray-900">Todos os Agendamentos</h2>
                {bookings.length === 0 ? (
                  <p className="text-gray-500">Nenhum agendamento encontrado.</p>
                ) : (
                  <div className="bg-white shadow overflow-hidden rounded-lg">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Usuário
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Sala
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Data e Horário
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Status
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Contato
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {bookings.map((booking) => (
                          <tr key={booking.id}>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div>
                                <div className="font-medium text-gray-900">{booking.user?.full_name}</div>
                                <div className="text-sm text-gray-500">{booking.user?.email}</div>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              {booking.room?.name}
                            </td>                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm text-gray-900">
                                {format(parseISO(booking.start_time), 'MMM d, yyyy', { locale: ptBR })}
                              </div>
                              <div className="text-sm text-gray-500">
                                {format(parseISO(booking.start_time), 'h:mm a', { locale: ptBR })} - {format(parseISO(booking.end_time), 'h:mm a', { locale: ptBR })}
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                booking.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                                booking.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                                'bg-blue-100 text-blue-800'
                              }`}>
                                {booking.status}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {booking.user?.phone || 'Não informado'}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {/* Users Tab */}
            {activeTab === 'users' && (
              <div className="space-y-4">                <h2 className="text-xl font-semibold text-gray-900">Todos os Usuários</h2>
                {users.length === 0 ? (
                  <p className="text-gray-500">Nenhum usuário encontrado.</p>
                ) : (
                  <div className="bg-white shadow overflow-hidden rounded-lg">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Nome
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Email
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Telefone
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Papel
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Status
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Cadastro
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {users.map((user) => (
                          <tr key={user.id}>
                            <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                              {user.full_name}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {user.email}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {user.phone || 'Não informado'}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${                                user.is_admin ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'
                              }`}>
                                {user.is_admin ? 'Administrador' : 'Usuário'}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${                                user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                              }`}>
                                {user.is_active ? 'Ativo' : 'Inativo'}
                              </span>
                            </td>                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {format(parseISO(user.created_at), 'MMM d, yyyy', { locale: ptBR })}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {/* Rooms Tab */}
            {activeTab === 'rooms' && (
              <div className="space-y-4">
                <div className="flex justify-between items-center">                  <h2 className="text-xl font-semibold text-gray-900">Todas as Salas</h2>
                  <button
                    onClick={() => setShowRoomForm(true)}
                    className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    <Plus className="h-4 w-4" />
                    <span>Adicionar Sala</span>
                  </button>
                </div>

                {showRoomForm && (
                  <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">{editingRoom ? 'Editar Sala' : 'Criar Nova Sala'}</h3>
                    <form onSubmit={handleRoomSubmit} className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Nome</label>
                          <input
                            type="text"
                            required
                            value={roomForm.name}
                            onChange={(e) => setRoomForm({ ...roomForm, name: e.target.value })}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Capacidade</label>
                          <input
                            type="number"
                            min="1"
                            required
                            value={roomForm.capacity}
                            onChange={(e) => setRoomForm({ ...roomForm, capacity: parseInt(e.target.value) })}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Descrição</label>
                        <textarea
                          value={roomForm.description}
                          onChange={(e) => setRoomForm({ ...roomForm, description: e.target.value })}
                          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          rows="3"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Equipamentos</label>
                        <textarea
                          value={roomForm.equipment}
                          onChange={(e) => setRoomForm({ ...roomForm, equipment: e.target.value })}
                          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          rows="2"
                        />
                      </div>
                      <div className="flex space-x-3">
                        <button
                          type="submit"
                          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                        >                          {editingRoom ? 'Salvar Alterações' : 'Criar Sala'}
                        </button>                        <button
                          type="button"
                          onClick={handleCancelRoomEdit}
                          className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                        >
                          Cancelar
                        </button>
                      </div>
                    </form>
                  </div>
                )}

                {rooms.length === 0 ? (
                  <p className="text-gray-500">Nenhuma sala encontrada.</p>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {rooms.map((room) => (
                      <div key={room.id} className="bg-white rounded-lg shadow p-6">
                        <h3 className="font-medium text-gray-900 mb-2">{room.name}</h3>
                        <p className="text-sm text-gray-600 mb-4">{room.description}</p>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-500">Capacidade:</span>
                            <span className="text-gray-900">{room.capacity}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-500">Status:</span>
                            <span className={`px-2 py-1 rounded-full text-xs ${                              room.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}>
                              {room.is_active ? 'Ativa' : 'Inativa'}
                            </span>
                          </div>
                        </div>
                        {room.equipment && (
                          <div className="mt-4">
                            <span className="text-sm font-medium text-gray-700">Equipamentos:</span>
                            <p className="text-sm text-gray-600 mt-1">{room.equipment}</p>
                          </div>
                        )}
                        <div className="mt-4 flex space-x-2">
                          <button
                            onClick={() => handleEditRoom(room)}
                            className="px-3 py-1 bg-yellow-500 text-white rounded-md hover:bg-yellow-600 flex items-center space-x-2"
                          >
                            <Edit className="h-4 w-4" />
                            <span>Editar</span>
                          </button>
                          <button
                            onClick={() => handleDeleteRoom(room.id, room.name)}
                            className="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 flex items-center space-x-2"
                          >
                            <Trash2 className="h-4 w-4" />
                            <span>Excluir</span>
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}              </div>
            )}            {/* Students Tab */}
            {activeTab === 'students' && (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold text-gray-900">Todos os Estudantes</h2>
                  <button
                    onClick={() => setShowStudentForm(true)}
                    className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    <Plus className="h-4 w-4" />
                    <span>Adicionar Estudante</span>
                  </button>
                </div>

                {showStudentForm && (
                  <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                      {editingStudent ? 'Editar Estudante' : 'Criar Novo Estudante'}
                    </h3>
                    <form onSubmit={handleStudentSubmit} className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Nome do Estudante</label>
                          <input
                            type="text"
                            required
                            value={studentForm.name}
                            onChange={(e) => setStudentForm({ ...studentForm, name: e.target.value })}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Nome do Professor</label>
                          <input
                            type="text"
                            required
                            value={studentForm.teacher_name}
                            onChange={(e) => setStudentForm({ ...studentForm, teacher_name: e.target.value })}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Email</label>
                          <input
                            type="email"
                            value={studentForm.email}
                            onChange={(e) => setStudentForm({ ...studentForm, email: e.target.value })}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Telefone</label>
                          <input
                            type="tel"
                            value={studentForm.phone}
                            onChange={(e) => setStudentForm({ ...studentForm, phone: e.target.value })}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Sala</label>
                          <select
                            required
                            value={studentForm.room_id}
                            onChange={(e) => setStudentForm({ ...studentForm, room_id: e.target.value })}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          >
                            <option value="">Selecione uma sala</option>
                            {rooms.map((room) => (
                              <option key={room.id} value={room.id}>
                                {room.name}
                              </option>
                            ))}
                          </select>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Dia da Semana</label>
                          <select
                            required
                            value={studentForm.weekday}
                            onChange={(e) => setStudentForm({ ...studentForm, weekday: e.target.value })}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          >
                            <option value="">Selecione o dia</option>
                            <option value="0">Segunda-feira</option>
                            <option value="1">Terça-feira</option>
                            <option value="2">Quarta-feira</option>
                            <option value="3">Quinta-feira</option>
                            <option value="5">Sábado</option>
                          </select>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Horário de Início</label>
                          <input
                            type="time"
                            required
                            value={studentForm.start_time}
                            onChange={(e) => setStudentForm({ ...studentForm, start_time: e.target.value })}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Horário de Término</label>
                          <input
                            type="time"
                            required
                            value={studentForm.end_time}
                            onChange={(e) => setStudentForm({ ...studentForm, end_time: e.target.value })}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700">Observações</label>
                        <textarea
                          value={studentForm.notes}
                          onChange={(e) => setStudentForm({ ...studentForm, notes: e.target.value })}
                          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                          rows="3"
                          placeholder="Observações adicionais sobre o estudante"
                        />
                      </div>

                      <div className="flex space-x-3">
                        <button
                          type="submit"
                          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                        >
                          {editingStudent ? 'Salvar Alterações' : 'Criar Estudante'}
                        </button>
                        <button
                          type="button"
                          onClick={handleCancelStudentEdit}
                          className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                        >
                          Cancelar
                        </button>
                      </div>
                    </form>
                  </div>
                )}

                {students.length === 0 ? (
                  <p className="text-gray-500">Nenhum estudante encontrado.</p>
                ) : (
                  <div className="bg-white shadow overflow-hidden rounded-lg">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Estudante
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Professor
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Contato
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Aula Semanal
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Sala
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Status
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Ações
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {students.map((student) => {
                          const weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
                          return (
                            <tr key={student.id}>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div>
                                  <div className="font-medium text-gray-900">{student.name}</div>
                                  {student.notes && (
                                    <div className="text-sm text-gray-500">{student.notes}</div>
                                  )}
                                </div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                {student.teacher_name}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                <div>{student.email || 'Email não informado'}</div>
                                <div>{student.phone || 'Telefone não informado'}</div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <div className="text-sm text-gray-900">
                                  {weekdays[student.weekday]}
                                </div>
                                <div className="text-sm text-gray-500">
                                  {student.start_time} - {student.end_time}
                                </div>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                {student.room?.name || 'Sala não encontrada'}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                  student.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                }`}>
                                  {student.is_active ? 'Ativo' : 'Inativo'}
                                </span>
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                                <button
                                  onClick={() => handleEditStudent(student)}
                                  className="text-blue-600 hover:text-blue-900 inline-flex items-center"
                                >
                                  <Edit className="h-4 w-4 mr-1" />
                                  Editar
                                </button>
                                <button
                                  onClick={() => handleDeleteStudent(student.id, student.name)}
                                  className="text-red-600 hover:text-red-900 inline-flex items-center ml-2"
                                >
                                  <Trash2 className="h-4 w-4 mr-1" />
                                  Excluir
                                </button>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default AdminPanel;
