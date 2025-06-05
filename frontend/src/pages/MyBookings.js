import React, { useState, useEffect } from 'react';
import { format, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Calendar, Clock, MapPin, X } from 'lucide-react';
import apiService from '../services/api';
import { toast } from 'react-toastify';
import Navbar from '../components/Navbar';

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cancellingId, setCancellingId] = useState(null);

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const bookingsData = await apiService.getMyBookings();
      setBookings(bookingsData);
    } catch (error) {
      toast.error('Falha ao buscar agendamentos');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('Tem certeza que deseja cancelar este agendamento?')) {
      return;
    }

    setCancellingId(bookingId);
    try {
      await apiService.cancelBooking(bookingId);
      toast.success('Agendamento cancelado com sucesso');
      fetchBookings(); // Refresh the list
    } catch (error) {
      toast.error(error.message || 'Falha ao cancelar agendamento');
    } finally {
      setCancellingId(null);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {      case 'confirmed':
        return 'bg-green-100 text-green-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      case 'completed':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const isPastBooking = (endTime) => {
    return new Date(endTime) < new Date();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">          <h1 className="text-3xl font-bold text-gray-900">Meus Agendamentos</h1>
          <p className="mt-2 text-gray-600">Visualize e gerencie seus agendamentos de sessões de prática.</p>
        </div>

        {bookings.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />            <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhum agendamento ainda</h3>
            <p className="text-gray-600">Você ainda não fez nenhum agendamento. Comece agendando uma sessão de prática!</p>
          </div>
        ) : (
          <div className="grid gap-6">
            {bookings.map((booking) => (
              <div key={booking.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-4 mb-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(booking.status)}`}>
                        {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                      </span>                      <span className="text-sm text-gray-500">
                        Agendado em {format(parseISO(booking.created_at), 'MMM d, yyyy', { locale: ptBR })}
                      </span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="flex items-center space-x-2">
                        <MapPin className="h-4 w-4 text-gray-400" />
                        <div>
                          <p className="font-medium text-gray-900">{booking.room?.name}</p>
                          <p className="text-sm text-gray-600">{booking.room?.description}</p>
                        </div>
                      </div>

                      <div className="flex items-center space-x-2">
                        <Calendar className="h-4 w-4 text-gray-400" />                        <div>
                          <p className="font-medium text-gray-900">
                            {format(parseISO(booking.start_time), 'EEEE, MMM d', { locale: ptBR })}
                          </p>
                          <p className="text-sm text-gray-600">
                            {format(parseISO(booking.start_time), 'yyyy')}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center space-x-2">
                        <Clock className="h-4 w-4 text-gray-400" />                        <div>
                          <p className="font-medium text-gray-900">
                            {format(parseISO(booking.start_time), 'h:mm a', { locale: ptBR })} - {format(parseISO(booking.end_time), 'h:mm a', { locale: ptBR })}
                          </p>
                          <p className="text-sm text-gray-600">
                            {Math.round((new Date(booking.end_time) - new Date(booking.start_time)) / (1000 * 60))} minutos
                          </p>
                        </div>
                      </div>
                    </div>

                    {booking.notes && (
                      <div className="mt-4">
                        <p className="text-sm text-gray-700">
                          <span className="font-medium">Observações:</span> {booking.notes}
                        </p>
                      </div>
                    )}
                  </div>

                  {booking.status === 'confirmed' && !isPastBooking(booking.end_time) && (
                    <button
                      onClick={() => handleCancelBooking(booking.id)}
                      disabled={cancellingId === booking.id}
                      className="ml-4 flex items-center space-x-1 px-3 py-2 text-sm font-medium text-red-600 hover:text-red-800 hover:bg-red-50 rounded-md transition-colors disabled:opacity-50"
                    >
                      <X className="h-4 w-4" />
                      <span>{cancellingId === booking.id ? 'Cancelando...' : 'Cancelar'}</span>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default MyBookings;
