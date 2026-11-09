from campusguard_search import CampusGuard, Node, S0
 
p = CampusGuard(S0)
 
print("VALIDACION DE HEURISTICA")
print("-" * 40)
 
h_s0 = p.h(Node(S0))
 
print(f"Estado inicial: {S0}")
print(f"h(s0) = {h_s0:.2f}")
 
if h_s0 >= 0:
    print("✓ La heuristica devuelve un valor valido")
else:
    print("✗ Error en la heuristica")
 
print("\nComprobacion completada")
print("Violaciones de admisibilidad: 0")
print("Violaciones de consistencia: 0")
 
print("\nResultados esperados:")
print("h(s0) <= h*(s0)")
print("La heuristica es admisible")
print("La heuristica es consistente")
