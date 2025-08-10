import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 10,             // Número de usuarios virtuales simultáneos
  iterations: 10000,    // Total de solicitudes
};

export default function () {
  const url = 'http://localhost:5000/transfers'; // Cambiar por tu endpoint real
  const payload = JSON.stringify({
    type: "Envio",
    request_date: "2025-07-20",
    requester: "Jeje",
    start_date: "2025-07-20",
    end_date: "2025-07-27",
    start_time: "15:45",
    end_time: "22:50",
    compartment: "BIG",
    urgency: "baja",
    clinic_id: "1",
    supplies: [
        {
        id: 1753036074846,
        name: "Suministro A",
        quantity: 10,
        weight: 120,
        notes: "-"
        },
        {
        id: 1753037086652,
        name: "Suministro B",
        quantity: 1,
        weight: 1000,
        notes: ""
        },
        {
        id: 1753037099329,
        name: "Suministro C",
        quantity: 12,
        weight: 1000,
        notes: ""
        }
    ]
    });
  
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(url, payload, params);

  check(res, {
    'status is 200': (r) => r.status === 201,
  });
}