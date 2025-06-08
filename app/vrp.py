import copy
from typing import List, Tuple, cast
import numpy as np


zero = 0
max_vehicles = 1
vehicle_capacity = 3000
infinity = float('inf')

alfa_1 = 1/3
alfa_2 = 1/3
alfa_3 = 1/3

distance_normalizer = 3
time_window_normalizer = 24

pedido = 'pedido'
envio = 'envio'

urgent_deliveries = []

normal_deliveries = []

low_deliveries = []

combinations_dict = {
    "S0-M0-B1": {'SMALL': 0, 'MEDIUM': 0, 'BIG': 1},
    "S0-M0-B2": {'SMALL': 0, 'MEDIUM': 0, 'BIG': 2},
    "S0-M1-B0": {'SMALL': 0, 'MEDIUM': 1, 'BIG': 0},
    "S0-M1-B1": {'SMALL': 0, 'MEDIUM': 1, 'BIG': 1},
    "S0-M1-B2": {'SMALL': 0, 'MEDIUM': 1, 'BIG': 2},
    "S0-M2-B0": {'SMALL': 0, 'MEDIUM': 2, 'BIG': 0},
    "S0-M2-B1": {'SMALL': 0, 'MEDIUM': 2, 'BIG': 1},
    "S0-M3-B0": {'SMALL': 0, 'MEDIUM': 3, 'BIG': 0},
    "S0-M3-B1": {'SMALL': 0, 'MEDIUM': 3, 'BIG': 1},
    "S0-M4-B0": {'SMALL': 0, 'MEDIUM': 4, 'BIG': 0},
    "S0-M5-B0": {'SMALL': 0, 'MEDIUM': 5, 'BIG': 0},
    "S1-M0-B0": {'SMALL': 1, 'MEDIUM': 0, 'BIG': 0},
    "S1-M0-B1": {'SMALL': 1, 'MEDIUM': 0, 'BIG': 1},
    "S1-M0-B2": {'SMALL': 1, 'MEDIUM': 0, 'BIG': 2},
    "S1-M1-B0": {'SMALL': 1, 'MEDIUM': 1, 'BIG': 0},
    "S1-M1-B1": {'SMALL': 1, 'MEDIUM': 1, 'BIG': 1},
    "S1-M2-B0": {'SMALL': 1, 'MEDIUM': 2, 'BIG': 0},
    "S1-M2-B1": {'SMALL': 1, 'MEDIUM': 2, 'BIG': 1},
    "S1-M3-B0": {'SMALL': 1, 'MEDIUM': 3, 'BIG': 0},
    "S1-M4-B0": {'SMALL': 1, 'MEDIUM': 4, 'BIG': 0},
    "S2-M0-B0": {'SMALL': 2, 'MEDIUM': 0, 'BIG': 0},
    "S2-M0-B1": {'SMALL': 2, 'MEDIUM': 0, 'BIG': 1},
    "S2-M0-B2": {'SMALL': 2, 'MEDIUM': 0, 'BIG': 2},
    "S2-M1-B0": {'SMALL': 2, 'MEDIUM': 1, 'BIG': 0},
    "S2-M1-B1": {'SMALL': 2, 'MEDIUM': 1, 'BIG': 1},
    "S2-M2-B0": {'SMALL': 2, 'MEDIUM': 2, 'BIG': 0},
    "S2-M2-B1": {'SMALL': 2, 'MEDIUM': 2, 'BIG': 1},
    "S2-M3-B0": {'SMALL': 2, 'MEDIUM': 3, 'BIG': 0},
    "S2-M4-B0": {'SMALL': 2, 'MEDIUM': 4, 'BIG': 0},
    "S3-M0-B0": {'SMALL': 3, 'MEDIUM': 0, 'BIG': 0},
    "S3-M0-B1": {'SMALL': 3, 'MEDIUM': 0, 'BIG': 1},
    "S3-M1-B0": {'SMALL': 3, 'MEDIUM': 1, 'BIG': 0},
    "S3-M1-B1": {'SMALL': 3, 'MEDIUM': 1, 'BIG': 1},
    "S3-M2-B0": {'SMALL': 3, 'MEDIUM': 2, 'BIG': 0},
    "S3-M3-B0": {'SMALL': 3, 'MEDIUM': 3, 'BIG': 0},
    "S4-M0-B0": {'SMALL': 4, 'MEDIUM': 0, 'BIG': 0},
    "S4-M0-B1": {'SMALL': 4, 'MEDIUM': 0, 'BIG': 1},
    "S4-M1-B0": {'SMALL': 4, 'MEDIUM': 1, 'BIG': 0},
    "S4-M1-B1": {'SMALL': 4, 'MEDIUM': 1, 'BIG': 1},
    "S4-M2-B0": {'SMALL': 4, 'MEDIUM': 2, 'BIG': 0},
    "S4-M3-B0": {'SMALL': 4, 'MEDIUM': 3, 'BIG': 0},
    "S5-M0-B0": {'SMALL': 5, 'MEDIUM': 0, 'BIG': 0},
    "S5-M0-B1": {'SMALL': 5, 'MEDIUM': 0, 'BIG': 1},
    "S5-M1-B0": {'SMALL': 5, 'MEDIUM': 1, 'BIG': 0},
    "S5-M2-B0": {'SMALL': 5, 'MEDIUM': 2, 'BIG': 0},
    "S6-M0-B0": {'SMALL': 6, 'MEDIUM': 0, 'BIG': 0},
    "S6-M0-B1": {'SMALL': 6, 'MEDIUM': 0, 'BIG': 1},
    "S6-M1-B0": {'SMALL': 6, 'MEDIUM': 1, 'BIG': 0},
    "S6-M2-B0": {'SMALL': 6, 'MEDIUM': 2, 'BIG': 0},
    "S7-M0-B0": {'SMALL': 7, 'MEDIUM': 0, 'BIG': 0},
    "S7-M1-B0": {'SMALL': 7, 'MEDIUM': 1, 'BIG': 0},
    "S8-M0-B0": {'SMALL': 8, 'MEDIUM': 0, 'BIG': 0},
    "S8-M1-B0": {'SMALL': 8, 'MEDIUM': 1, 'BIG': 0},
    "S9-M0-B0": {'SMALL': 9, 'MEDIUM': 0, 'BIG': 0},
    "S10-M0-B0": {'SMALL': 10, 'MEDIUM': 0, 'BIG': 0},
}



distances = np.array([
    [ zero, 0.5, 0.6, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1], # depot
    [ 0.5, zero, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
    [ 0.6, 1.3, zero, 1.5, 1.6, 0.7, 1.8, 1.9, 2.0, 1.0],
    [ 0.5, 1.4, 1.5, zero, 1.7, 1.8, 1.0, 2.0, 1.9, 1.8],
    [ 0.6, 1.5, 1.6, 1.7, zero, 0.9, 2.0, 1.9, 1.8, 1.7],
    [ 0.7, 1.6, 0.7, 1.8, 0.9, zero, 1.9, 0.8, 1.7, 1.6],
    [ 0.8, 1.7, 1.8, 1.0, 2.0, 1.9, zero, 1.7, 1.6, 1.5],
    [ 0.9, 1.8, 1.9, 2.0, 1.9, 0.8, 1.7, zero, 1.5, 1.4],
    [1.0, 1.9, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5, zero, 0.3],
    [1.1, 2.0, 1.0, 1.8, 1.7, 1.6, 1.5, 1.4, 0.3, zero]
])


class Node:
    def __init__(self, policlinic, demand, time_window, service_time, delivery_name, delivery_type, box_type):
        self.policlinic: int = policlinic
        self.demand: int = demand
        self.time_window: Tuple[int, int] = time_window
        self.service_time: int = service_time
        self.delivery_name: str  = delivery_name
        self.delivery_type: str = delivery_type
        self.box_type: str = box_type
    
    def get_start_time_window(self):
       return self.time_window[0]
    
    def get_end_time_window(self):
       return self.time_window[1]

class VRPTW_MultipleDeliveries:

    routes_by_day = {}

    def __init__(self, deliveries, depot, distances, vehicle_capacity, max_vehicles):
        self.depot: Node = depot
        self.deliveries: List[Node] = deliveries
        self.distances: np.ndarray = distances
        self.vehicle_capacity: int = vehicle_capacity
        self.max_vehicles: int = max_vehicles

    def solve(self, unrouted_deliveries: List[Node], predefined_routes: List[List[Node]]):

        if not unrouted_deliveries:
            print("return predefined")
            return predefined_routes, [], None
        
        routes = []
        unrouted_deliveries_copy = unrouted_deliveries.copy()
        impossible_node = None

        depot_copy = Node(0, 0, (0, 20), 0, 'Depot', None, None)
        processed_routes = []

        while unrouted_deliveries_copy:

            if predefined_routes:

                predefined_r = predefined_routes[0].copy()
                predefined_r.pop() #saca el depot del final
                route: List[Node] = predefined_r.copy()

                #for node in route:
                #    print('PREDEFINED ROUT:' + node.delivery_name)

                loads_by_node = self.get_route_load(predefined_r)
                boxes_by_node = self.get_route_boxes(predefined_r)

                predefined_routes.pop(0)
            
            else:
                boxes_info = {
                    "SMALL": 0,
                    "MEDIUM": 0,
                    "BIG": 0,
                }
                route: List[Node] = [depot_copy]
                loads_by_node = [0]
                boxes_by_node = [boxes_info]

            start_service = []
            while True:
                best_delivery = None
                best_cost = infinity
                best_position = infinity
                start_service = self.set_start_service_times(route, depot_copy) # pls

                #print("start_service: ")
                #print(start_service)
                #print("----------------------------------------------------------------")
                
                for node in unrouted_deliveries_copy:
                    min_cost, local_position, impossible_node = self.min_insertion_cost(route, node, start_service, loads_by_node, boxes_by_node)
                    #print("min_cost:" + str(min_cost))
                    #print("min_cost:" + str(local_position))
                                            
                    if min_cost < best_cost:
                        
                        best_delivery = node
                        best_cost = min_cost
                        best_position = local_position

                if best_delivery is None:
                    break # termina la ruta
                
                self.update_loads_by_node(best_delivery, best_position, loads_by_node, route)
                print("Agrego una nueva box a la ruta " + best_delivery.delivery_name + " " + best_delivery.box_type)
                self.print_route(route)

                self.update_boxes_by_node(best_delivery, best_position, boxes_by_node, route)
                print("Nuevo boxes by node")
                print(boxes_by_node)

                route.insert(best_position, best_delivery)
                
                unrouted_deliveries_copy.remove(best_delivery)
            
            if len(route) == 1:
                
                if impossible_node:
                    print("Quitar pedido imposible de los pedidos para rutear.")
                    unrouted_deliveries_copy.remove(impossible_node)

                # Ruta de largo uno significa q solo pude agregar el deposito en una nueva ruta, ya no tengo tiempo para seguir creando rutas este dia
                print("Aca no es posible seguir ruteando pedidos de esta prioridad.")
                break

            else:
                # terminamos, intentamos empezar otra, actualizamos el depot
                # (U, L, L, L, L - D - U)

                route.append(self.depot) # metemos el ultimo depot.
                #self.print_route(route)
                routes.append(route) 

                last_node_index_before_depot = route[len(route) - 2]
                second_depot_index = len(route) - 1
                
                last_start_service = self.get_start_service_time_for_node(last_node_index_before_depot, self.depot, start_service, second_depot_index)
                depot_copy.time_window = (last_start_service, depot_copy.time_window[1])
        
        #print("---------------------------------------------------------------------------------")
        return routes, unrouted_deliveries_copy, impossible_node

    def print_route(route: List[Node]):
        str_to_print = ''
        for j in range(len(route)):
            node = route[j]
            str_to_print += node.delivery_name + '->'
        #print(str_to_print)
        return str_to_print 
    
    def update_boxes_by_node(self, best_delivery: Node, best_position, boxes_by_node, route):
        
        box_type = best_delivery.box_type

        if best_delivery.delivery_type == 'pedido':
            for i in range(0, best_position):
                boxes_by_node[i] = self.update_box_object(box_type, boxes_by_node[i], True)

            new_box_info = self.update_box_object(box_type, boxes_by_node[best_position - 1], False) # entrege la caja
            boxes_by_node.insert(best_position, new_box_info)

        if best_delivery.delivery_type == 'envio':
            for i in range(best_position, len(route)):
                boxes_by_node[i] = self.update_box_object(box_type, boxes_by_node[i], True)

            new_box_info = self.update_box_object(box_type, boxes_by_node[best_position - 1], True) 
            boxes_by_node.insert(best_position, new_box_info)

    def get_route_boxes(self, predefined_route: List[Node]):
        
        box_zero = {
            "SMALL": 0,
            "MEDIUM": 0,
            "BIG": 0,
        }
        boxes_by_node = [box_zero] * len(predefined_route)
        
        for index, node in enumerate(predefined_route[1:], start=1): # el primero es el depot
            
            if node.delivery_type == 'pedido':
                for i in range(0, index):
                    boxes_by_node[i] = self.update_box_object(node.box_type, boxes_by_node[i], True)
                    
                boxes_by_node[index] = self.update_box_object(node.box_type, boxes_by_node[index - 1], False)
                 

            if node.delivery_type == 'envio':
                for i in range(index, len(predefined_route)):
                    boxes_by_node[i] = self.update_box_object(node.box_type, boxes_by_node[i], True)

                boxes_by_node[index] = self.update_box_object(node.box_type, boxes_by_node[index - 1], True)

        return boxes_by_node


    def update_box_object(self, box_type, box_object: dict, sum: bool):
        # si sum es true, sumo 1. si false resto 1
        #print(box_object)
        new_box_object = {
            "SMALL": box_object["SMALL"],
            "MEDIUM": box_object["MEDIUM"],
            "BIG": box_object["BIG"]
        }
        
        if box_type == "SMALL":
            if sum:
                new_box_object["SMALL"] += 1
            else:
                new_box_object["SMALL"] -= 1
        
        if box_type == "MEDIUM":
            if sum:
                new_box_object["MEDIUM"] += 1
            else:
                new_box_object["MEDIUM"] -= 1
        
        if box_type == "BIG":
            if sum:
                new_box_object["BIG"] += 1
            else:
                new_box_object["BIG"] -= 1
        
        return new_box_object

    def update_loads_by_node(self, best_delivery: Node, best_position: int, loads_by_node, route: List[Node]):
        if best_delivery.delivery_type == 'pedido':
            for i in range(0, best_position):
                loads_by_node[i] = loads_by_node[i] + best_delivery.demand

            new_load = loads_by_node[best_position - 1] - best_delivery.demand
            loads_by_node.insert(best_position, new_load)

        if best_delivery.delivery_type == 'envio':
            for i in range(best_position, len(route) - 1): # sacar el menos 1
                loads_by_node[i] = loads_by_node[i] + best_delivery.demand

            new_load = loads_by_node[best_position - 1] + best_delivery.demand # loads by node (2)
            loads_by_node.insert(best_position, new_load)

    def get_route_load(self, predefined_route: List[Node]):
        loads_by_node = [0] * len(predefined_route)
        
        for index, node in enumerate(predefined_route[1:], start=1):
            if node.delivery_type == 'pedido':
                for i in range(0, index):
                    loads_by_node[i] = loads_by_node[i] + node.demand

                loads_by_node[index] = loads_by_node[index - 1] - node.demand # quito la demanda porque llegue al nodo a entregar node.demand

            if node.delivery_type == 'envio':
                for i in range(index, len(predefined_route)):
                    loads_by_node[i] = loads_by_node[i] + node.demand

                loads_by_node[index] = loads_by_node[index - 1] + node.demand # loads by node (2)

        return loads_by_node

    def print_route(self, route: List[Node]):
        str_to_print = ''
        for j in range(len(route)):
            node = route[j]
            str_to_print += node.delivery_name + '->'
        print(str_to_print)

    def distance_between_nodes(self, node_i: Node, node_j: Node):
       return self.distances[node_i.policlinic][node_j.policlinic]

    def c11(self, previous_node: Node, node: Node, next_node: Node):
        mu = 1
        original_distance = self.distance_between_nodes(previous_node, next_node)
        distance_to_node = self.distance_between_nodes(previous_node, node)
        distance_to_next_node = self.distance_between_nodes(node, next_node)
    
        return distance_to_node + distance_to_next_node - mu * original_distance

    
    def c12(self, previous_node: Node, node: Node, next_node: Node, start_service, next_node_position):
        bj = start_service[next_node_position]
        bi = start_service[next_node_position - 1] 
        
        distance_to_node = self.distance_between_nodes(previous_node, node)
        service_time_in_prev_node = previous_node.service_time
        bu = max(node.get_start_time_window(), bi + service_time_in_prev_node + distance_to_node)

        distance_from_node_next_node = self.distance_between_nodes(node, next_node)
        bu_j = max(next_node.get_start_time_window(), bu + node.service_time + distance_from_node_next_node)

        return bu_j - bj
        
    def c13(self, previous_node: Node, node: Node, next_node, start_service, next_node_position):
        bi = start_service[next_node_position - 1]
        
        distance_to_node = self.distance_between_nodes(previous_node, node)
        service_time_in_prev_node = previous_node.service_time
        
        bu = max(node.get_start_time_window(), bi + service_time_in_prev_node + distance_to_node)
        lu = node.get_end_time_window()
        
        return lu - bu
    
    def get_start_service_time_for_node(self, previous_node: Node, node: Node, start_service, position):
        distance_to_node = self.distance_between_nodes(previous_node, node)
        service_time_in_prev_node = previous_node.service_time

        return max(node.get_start_time_window(), start_service[position-1] + service_time_in_prev_node + distance_to_node)

    def imprimir_nodo(self, n): print(f"Policlínica: {n.policlinic}, Demanda: {n.demand}, Ventana: {n.time_window}, Servicio: {n.service_time} hs, Nombre: {n.delivery_name}, Tipo: {n.delivery_type}")


    def min_insertion_cost(self, route: List[Node], unrouted_node: Node, start_service, loads_by_node, boxes_by_node):
        min_cost = infinity
        best_position = infinity 

        for i in range(len(route)):
            previous_node = route[i]
            next_node = self.depot if (i == len(route) - 1) else route[i+1]

            local_solution = (
                (alfa_1) * self.c11(previous_node, unrouted_node, next_node) / distance_normalizer + # 
                (alfa_2) * self.c12(previous_node, unrouted_node, next_node, start_service, i+1) / time_window_normalizer +
                (alfa_3) * self.c13(previous_node, unrouted_node, None, start_service, i+1) / time_window_normalizer
            )
           
            #print("local" + str(local_solution))

            if local_solution < min_cost:

                is_feasible_push_forward, impossible_node = self.check_push_forward(route, unrouted_node, i+1, start_service)

                if not is_feasible_push_forward and impossible_node:
                    # esta contando intento de crear otra ruta en un dia q ya tiene una ruta
                    # debería ser, no tengo ninguna ruta en el día y no puedo crear una
                    print("PEDIDO IMPOSIBLE DE REALIZAR" + str(unrouted_node.delivery_name))
                    return min_cost, best_position, impossible_node

                is_feasible_load = False

                if unrouted_node.delivery_type == 'pedido':
                    is_feasible_load = self.check_pedido_load(route, unrouted_node, i+1, loads_by_node)
                    is_feasible_box = self.check_pedido_box(route, unrouted_node, i+1, boxes_by_node)

                if unrouted_node.delivery_type == 'envio':
                    is_feasible_load = self.check_envio_load(route, unrouted_node, i+1, loads_by_node)
                    is_feasible_box = self.check_envio_box(route, unrouted_node, i+1, boxes_by_node)

                
                if is_feasible_box and is_feasible_load and is_feasible_push_forward:
                    min_cost = local_solution
                    best_position = i+1
            
        return min_cost, best_position, None

    def check_pedido_box(self, route, unrouted_node: Node, position, boxes_by_node):
        for i in range(0, position):
            if self.check_add_new_box(unrouted_node.box_type, boxes_by_node[i]) == False:
                return False

        return True
    
    def check_envio_box(self, route, unrouted_node: Node, position, boxes_by_node):
        for i in range(position, len(route)):
            if self.check_add_new_box(unrouted_node.box_type, boxes_by_node[i]) == False:
                return False

        return True

    def check_envio_load(self, route, unrouted_node, position, loads_by_node):
        for i in range(position, len(route)):
            if loads_by_node[i] + unrouted_node.demand > self.vehicle_capacity:
                return False
        
        return True
    

    def check_add_new_box(self, new_box_type, node_box):
  
        if new_box_type == "SMALL":
            key = f"S{node_box["SMALL"] + 1}-M{node_box["MEDIUM"]}-B{node_box["BIG"]}"
        elif new_box_type == "MEDIUM":
            key = f"S{node_box["SMALL"]}-M{node_box["MEDIUM"] + 1}-B{node_box["BIG"]}"
        elif new_box_type == "BIG":
            key = f"S{node_box["SMALL"]}-M{node_box["MEDIUM"]}-B{node_box["BIG"] + 1}"
        else:
            raise ValueError("new_box_type debe ser 'SMALL', 'MEDIUM' o 'BIG'")

        return key in combinations_dict


    def check_pedido_load(self, route, unrouted_node: Node, position, loads_by_node):
        for i in range(0, position):
            if loads_by_node[i] + unrouted_node.demand > self.vehicle_capacity:
                return False
        
        return True
    
    def check_envio_load(self, route, unrouted_node, position, loads_by_node):
        for i in range(position, len(route)):
            if loads_by_node[i] + unrouted_node.demand > self.vehicle_capacity:
                return False
        
        return True
    
    def check_push_forward(self, route: List[Node], node: Node, position, start_service):

        distance_to_node = self.distance_between_nodes(route[position-1], node)
        previous_node = cast(Node, route[position-1])

        bu = max(node.get_start_time_window(), start_service[position-1] + previous_node.service_time + distance_to_node)
        lu = node.get_end_time_window()
        if bu > lu:
            return False, None

        bu = self.get_start_service_time_for_node(previous_node, node, start_service, position)
        
        bj = start_service[position]
        next_policlinic = route[position] if position < len(route) else self.depot
        distance_to_j = self.distance_between_nodes(node, next_policlinic)
        
        b_new_j = max(next_policlinic.get_start_time_window(), bu + node.service_time + distance_to_j)

        PF = b_new_j - bj
        if PF == 0:
            return True, None
        else:
            feasible_insertion = (bj + PF) <= next_policlinic.get_end_time_window()
            if not feasible_insertion:
                # caso borde pedido imposible
                if len(route) == 1 and route[0].get_start_time_window() > self.depot.get_start_time_window(): #tremendo bugfix
                    return False, node

                return False, None

        for j in range(position + 1, len(route) + 1): 
            next_policlinic = route[j] if j < len(route) else self.depot
            previous_node = route[j-1]

            distance_to_next_policlinic = self.distance_between_nodes(previous_node, next_policlinic)
            pre_waiting_time = start_service[j] - (start_service[j-1] + PF + previous_node.service_time + distance_to_next_policlinic)
            waiting_time = max(0, pre_waiting_time)

            PF = max(0, PF - waiting_time)
            if PF != 0:
                feasible_insertion = (start_service[j] + PF) < next_policlinic.get_end_time_window()
                if not feasible_insertion:
                    return False, None
            else:
                break 

        return True, None

    def set_start_service_times(self, route: List[Node], current_depot: Node):
        start_service = [current_depot.get_start_time_window()]

        for j in range(1, len(route)): # [depot]
            previous_node = route[j-1]
            node = route[j]

            distance_to_node = self.distance_between_nodes(previous_node, node)
            bj = max(node.get_start_time_window(), start_service[j-1] + previous_node.service_time + distance_to_node)
            start_service.append(bj)
        
        last_node_index = len(route)-1
        last_node = route[last_node_index]
        
        distance_to_depot = self.distance_between_nodes(last_node, self.depot)
        return_to_depot = start_service[last_node_index] + last_node.service_time + distance_to_depot
        
        start_service.append(return_to_depot)
        return start_service

def __main__():
    
    
    depot = Node(0, 0, (0, 20), 0, 'Depot', None)

    urgent_deliveries = [
        Node(4, 400, (15, 20), 0.7, 'J', 'envio', "SMALL"),
        Node(1, 1500, (10, 13), 0.5, 'B', 'pedido', "BIG"),
        Node(6, 2800, (12, 19), 0.7, 'P', 'pedido', "SMALL"),
        Node(9, 1000, (9, 18), 0.7, 'M', 'envio', "SMALL"),
        Node(4, 1200, (12, 15), 0.7, 'N', 'pedido', "MEDIUM"),
    ] 

    normal_deliveries = [
        Node(2, 1500, (10, 14), 0.6, 'D', 'pedido', "MEDIUM"),
        Node(3, 1900, (9, 15), 0.8, 'E', 'pedido', "MEDIUM"),
        Node(4, 900, (11, 17), 0.5, 'F', 'pedido', "BIG"),
        Node(5, 2500, (7, 10), 0.7, 'G', 'pedido', "SMALL"),
    ] 

    low_deliveries = [
        Node(1, 200, (9, 12), 0.5, 'A', 'pedido', "MEDIUM"),
        Node(2, 400, (8, 11), 0.7, 'C', 'pedido', "BIG"),
        Node(5, 1500, (9, 12), 0.7, 'H', 'pedido', "MEDIUM"),
        Node(6, 400, (7, 10), 0.7, 'I', 'pedido', "BIG"),
        Node(8, 400, (13, 16), 0.7, 'K', 'pedido, "MEDIUM"'),
        Node(8, 400, (13, 20), 0.7, 'L', 'envio', "SMALL"),
        Node(5, 400, (8, 19), 0.7, 'O', 'pedido', "SMALL"),
        Node(1, 400, (9, 10), 0.7, 'Q', 'pedido', "SMALL"),
        Node(9, 100, (18, 21), 0.7, 'Mariana', 'pedido', "SMALL"),
    ]
            
    deliveries: List[Node] = [
        #Node(1, 200, (10, 13), 0.5, 'B'),
        #Node(1, 300, (9, 12), 0.5, 'A'),
        #Node(2, 400, (8, 11), 0.7, 'C'),
        #Node(2, 200, (10, 14), 0.6, 'D'),
        #Node(3, 500, (9, 15), 0.8, 'E'),
        #Node(4, 300, (11, 17), 0.5, 'F'),
        #Node(5, 400, (7, 10), 0.7, 'G'),
        #Node(5, 1500, (9, 12), 0.7, 'H'),
        #Node(6, 400, (7, 10), 0.7, 'I'),
        #Node(7, 400, (15, 20), 0.7, 'J'),
        #Node(8, 400, (13, 16), 0.7, 'K'),
        #Node(8, 400, (13, 20), 0.7, 'L'),
        #Node(9, 400, (9, 18), 0.7, 'M'),
        #Node(4, 400, (12, 15), 0.7, 'N'),
        #Node(5, 400, (8, 19), 0.7, 'O'),
        #Node(6, 400, (12, 19), 0.7, 'P'),
        #Node(1, 400, (9, 10), 0.7, 'Q'),
    ]

    varp = VRPTW_MultipleDeliveries(deliveries, depot, distances, vehicle_capacity, max_vehicles)
    routes: List[List[Node]] = []
    routes_by_day = {}
    i = 1
    while len(urgent_deliveries) != 0 or len(normal_deliveries) != 0 or len(low_deliveries) != 0:
        
        routes, urgent_deliveries = varp.solve(urgent_deliveries, routes)
        print("Finaliza ruteo Urgente" )
        routes, normal_deliveries = varp.solve(normal_deliveries, routes)
        print("Finaliza ruteo Normal" )
        routes, low_deliveries = varp.solve(low_deliveries, routes)
        print("Finaliza ruteo Low" )

        if len(routes) != 0:
            routes_copy = []
            for route in routes:
                route_copy = route.copy()
                routes_copy.append(route_copy)


            routes_by_day[i] = routes_copy.copy()
            print("Aca termina el día " + str(i))
            i += 1
            routes = []


    #routes_by_day = defaultdict(list)
    for key in routes_by_day.keys():
        routes = routes_by_day.get(key)
        print('Routes for day ' + str(key) + ':')
        #print(routes)
        for route in routes:
           varp.print_route(route)
        print('-----------------------------------------------------------------------------')


#__main__()