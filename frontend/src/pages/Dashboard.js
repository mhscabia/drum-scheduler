import React, { useState, useEffect } from 'react';
import { format, startOfWeek, addDays, isSameDay, parseISO, isBefore, isToday } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Calendar, Clock, MapPin, BookOpen, User, Phone, Mail } from 'lucide-react';
import apiService from '../services/api';
import { toast } from 'react-toastify';
import Navbar from '../components/Navbar';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('booking'); // 'booking' or 'classes'
  const [rooms, setRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [selectedDate, setSelectedDate] = useState(() => {
    // Initialize with today's date, but ensure it's not in the past
    const today = new Date();
    return today;
  });
  const [availableSlots, setAvailableSlots] = useState([]);
  const [userClasses, setUserClasses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [classesLoading, setClassesLoading] = useState(false);

  useEffect(() => {
    fetchRooms();
    if (activeTab === 'classes') {
      fetchUserClasses();
    }
  }, [activeTab]);

  useEffect(() => {
    if (selectedRoom && activeTab === 'booking') {
      fetchAvailableSlots();
    }
  }, [selectedRoom, selectedDate, activeTab]);

  const fetchRooms = async () => {
    try {
      const roomsData = await apiService.getRooms();
      setRooms(roomsData);
      if (roomsData.length > 0) {
        setSelectedRoom(roomsData[0]);
      }
    } catch (error) {
      toast.error('Falha ao buscar salas');
    }
  };

  const fetchAvailableSlots = async () => {
    if (!selectedRoom) return;
    
    setLoading(true);
    try {
      const dateStr = format(selectedDate, 'yyyy-MM-dd');
      const slots = await apiService.getAvailableSlots(selectedRoom.id, dateStr);
      setAvailableSlots(slots);
    } catch (error) {
      toast.error('Falha ao buscar horários disponíveis');
    } finally {
      setLoading(false);
    }
  };

  const handleBookSlot = async (slot) => {
    if (!slot.is_available) return;
    
    setBookingLoading(true);
    try {
      await apiService.createBooking({
        room_id: selectedRoom.id,
        start_time: slot.start_time,
        end_time: slot.end_time,
        notes: ''
      });
      toast.success('Agendamento criado com sucesso!');
      fetchAvailableSlots(); // Refresh slots
    } catch (error) {
      toast.error(error.message || 'Falha ao criar agendamento');
    } finally {
      setBookingLoading(false);
    }
  };

  const getWeekDays = () => {
    const start = startOfWeek(new Date());
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Reset time to start of day for proper comparison
    
    // Generate 7 days but filter out Sunday (day 0) and Friday (day 5)
    const weekDays = Array.from({ length: 7 }, (_, i) => addDays(start, i))
      .filter(day => day.getDay() !== 0 && day.getDay() !== 5) // Remove Sunday and Friday
      .map(day => {
        const dayStart = new Date(day);
        dayStart.setHours(0, 0, 0, 0); // Reset time to start of day
        const isPast = isBefore(dayStart, today);
        
        return {
          date: day,
          isPast: isPast
        };
      });
    
    return weekDays;
  };

  const isSlotInPast = (slot) => {
    const now = new Date();
    const slotStart = new Date(slot.start_time);
    const isPast = slotStart < now;
    
    return isPast;
  };

  const fetchUserClasses = async () => {
    setClassesLoading(true);
    try {
      const classes = await apiService.getMyClasses();
      setUserClasses(classes);
    } catch (error) {
      toast.error('Falha ao buscar informações das aulas');
      console.error('Error fetching user classes:', error);
    } finally {
      setClassesLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            {activeTab === 'booking' ? 'Agendar prática' : 'Minhas Aulas'}
          </h1>
          <p className="mt-2 text-gray-600">
            {activeTab === 'booking' 
              ? 'Selecione uma sala, data e horário para agendar sua sessão de prática.'
              : 'Informações sobre suas aulas e horários.'
            }
          </p>
          
          {/* Tab Navigation */}
          <div className="mt-6">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8">
                <button
                  onClick={() => setActiveTab('booking')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'booking'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Calendar className="h-4 w-4 inline mr-2" />
                  Agendamento
                </button>
                <button
                  onClick={() => setActiveTab('classes')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'classes'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <BookOpen className="h-4 w-4 inline mr-2" />
                  Minhas Aulas
                </button>
              </nav>
            </div>
          </div>
          
          {activeTab === 'booking' && (
            <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
              <p className="text-sm text-blue-800">
                <strong>Horários de funcionamento:</strong> Segunda a Sexta: 9h às 21h | Sábado: 9h às 13h | Domingo: Fechado
              </p>
            </div>
          )}
        </div>

        {/* Booking Tab Content */}
        {activeTab === 'booking' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Room Selection */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <MapPin className="h-5 w-5 mr-2 text-blue-600" />
                Selecionar Sala
              </h2>
              <div className="space-y-3">
                {rooms.map((room) => (
                  <div
                    key={room.id}
                    onClick={() => setSelectedRoom(room)}
                    className={`p-4 rounded-lg border-2 cursor-pointer transition-colors ${
                      selectedRoom?.id === room.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <h3 className="font-medium text-gray-900">{room.name}</h3>
                    <p className="text-sm text-gray-600 mt-1">{room.description}</p>
                    <div className="mt-2 flex items-center text-xs text-gray-500">
                      <span>Capacidade: {room.capacity}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Date Selection */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Calendar className="h-5 w-5 mr-2 text-blue-600" />
                Selecionar Data
              </h2>
              <div className="grid grid-cols-1 gap-2">
                {getWeekDays().map((dayObj) => {
                  const { date: day, isPast } = dayObj;
                  return (
                    <button
                      key={day.toISOString()}
                      onClick={() => !isPast && setSelectedDate(day)}
                      disabled={isPast}
                      className={`p-3 rounded-lg text-left transition-colors ${
                        isSameDay(day, selectedDate)
                          ? 'bg-blue-500 text-white'
                          : isPast
                          ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                          : 'bg-gray-50 hover:bg-gray-100 text-gray-900'
                      }`}
                    >
                      <div className="font-medium">{format(day, 'EEEE', { locale: ptBR })}</div>
                      <div className="text-sm opacity-75">
                        {format(day, 'MMM d', { locale: ptBR })}
                        {isPast && ' (passado)'}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Time Slots */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Clock className="h-5 w-5 mr-2 text-blue-600" />
                Horários Disponíveis
              </h2>
              
              {loading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="mt-2 text-gray-600">Carregando horários...</p>
                </div>
              ) : (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {availableSlots.map((slot, index) => {
                    const isSlotPast = isSlotInPast(slot);
                    const isSlotDisabled = !slot.is_available || isSlotPast || bookingLoading;
                    
                    return (
                      <button
                        key={index}
                        onClick={() => !isSlotDisabled && handleBookSlot(slot)}
                        disabled={isSlotDisabled}
                        className={`w-full p-3 rounded-lg text-left transition-colors ${
                          isSlotPast
                            ? 'bg-gray-100 border border-gray-200 text-gray-400 cursor-not-allowed'
                            : slot.is_available
                            ? 'bg-green-50 border border-green-200 hover:bg-green-100 text-green-800'
                            : 'bg-gray-50 border border-gray-200 text-gray-400 cursor-not-allowed'
                        }`}
                      >
                        <div className="font-medium">
                          {format(parseISO(slot.start_time), 'HH:mm', { locale: ptBR })} - {format(parseISO(slot.end_time), 'HH:mm', { locale: ptBR })}
                        </div>
                        <div className="text-sm">
                          {isSlotPast 
                            ? 'Horário passado' 
                            : slot.is_available 
                            ? 'Disponível' 
                            : 'Ocupado'
                          }
                        </div>
                      </button>
                    );
                  })}
                  {availableSlots.length === 0 && (
                    <p className="text-gray-500 text-center py-4">
                      {selectedRoom ? 'Nenhum horário disponível para esta data' : 'Selecione uma sala para ver os horários disponíveis'}
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Room Details */}
        {activeTab === 'booking' && selectedRoom && (
          <div className="mt-6 bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Detalhes da Sala</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-medium text-gray-700">Equipamentos</h4>
                <p className="text-gray-600">{selectedRoom.equipment || 'Equipamentos padrão'}</p>
              </div>
              <div>
                <h4 className="font-medium text-gray-700">Capacidade</h4>
                <p className="text-gray-600">{selectedRoom.capacity} pessoa(s)</p>
              </div>
            </div>
          </div>
        )}

        {/* Classes Tab Content */}
        {activeTab === 'classes' && (
          <div className="space-y-6">
            {classesLoading ? (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Carregando informações das aulas...</p>
              </div>
            ) : userClasses.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhuma aula encontrada</h3>
                <p className="text-gray-600">
                  Você ainda não está matriculado em nenhuma aula. Entre em contato com a administração para se inscrever.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {userClasses.map((studentClass, index) => (
                  <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
                    <div className="bg-blue-600 text-white p-4">
                      <h3 className="text-lg font-semibold">{studentClass.name}</h3>
                      <p className="text-blue-100">Aluno</p>
                    </div>
                    <div className="p-6 space-y-4">
                      <div className="flex items-center text-gray-700">
                        <User className="h-5 w-5 mr-3 text-gray-400" />
                        <div>
                          <p className="font-medium">Professor</p>
                          <p className="text-sm">{studentClass.teacher_name}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center text-gray-700">
                        <MapPin className="h-5 w-5 mr-3 text-gray-400" />
                        <div>
                          <p className="font-medium">Sala</p>
                          <p className="text-sm">{studentClass.room?.name || `Sala ${studentClass.room_id}`}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center text-gray-700">
                        <Calendar className="h-5 w-5 mr-3 text-gray-400" />
                        <div>
                          <p className="font-medium">Dia da Semana</p>
                          <p className="text-sm">
                            {['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'][studentClass.weekday]}
                          </p>
                        </div>
                      </div>
                      
                      <div className="flex items-center text-gray-700">
                        <Clock className="h-5 w-5 mr-3 text-gray-400" />
                        <div>
                          <p className="font-medium">Horário</p>
                          <p className="text-sm">{studentClass.start_time} - {studentClass.end_time}</p>
                        </div>
                      </div>
                      
                      {studentClass.email && (
                        <div className="flex items-center text-gray-700">
                          <Mail className="h-5 w-5 mr-3 text-gray-400" />
                          <div>
                            <p className="font-medium">Email</p>
                            <p className="text-sm">{studentClass.email}</p>
                          </div>
                        </div>
                      )}
                      
                      {studentClass.phone && (
                        <div className="flex items-center text-gray-700">
                          <Phone className="h-5 w-5 mr-3 text-gray-400" />
                          <div>
                            <p className="font-medium">Telefone</p>
                            <p className="text-sm">{studentClass.phone}</p>
                          </div>
                        </div>
                      )}
                      
                      {studentClass.notes && (
                        <div className="border-t pt-4">
                          <p className="font-medium text-gray-700 mb-1">Observações</p>
                          <p className="text-sm text-gray-600">{studentClass.notes}</p>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
