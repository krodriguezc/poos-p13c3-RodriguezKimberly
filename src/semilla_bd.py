from datetime import date
from dominio.empleado import Administrador
from dominio.usuario import Usuario
from persistencia.crearbd import crear_tablas
from persistencia.empleadodao import EmpleadoDAO
from persistencia.usuariodao import UsuarioDAO

def ejecutar_semilla():
    print("Iniciando la semilla de la base de datos.")
    
    # Asegurar que las tablas de la base de datos estén creadas
    crear_tablas()
    
    # Datos estables para el administrador inicial
    correo_admin = "admin@ecotech.cl"
    nombre_usuario_admin = "admin"
    clave_inicial = "Admin123*"
    
    # Buscar si el empleado administrador ya existe por su correo estable
    empleado = None
    for emp in EmpleadoDAO.listar():
        if emp.correo == correo_admin:
            empleado = emp
            break
            
    if empleado is None:
        # Si no existe, se crea el registro del empleado administrador
        empleado = Administrador(
            rut="11111111-1",
            nombre="Administrador Sistema",
            correo=correo_admin,
            direccion="Oficina Central",
            telefono="+56911111111",
            fecha_inicio_contrato=date.today().isoformat(),
            salario_base=1500000.0,
            departamento_id=None
        )
        empleado = EmpleadoDAO.insertar(empleado)
        print(f"[SEMILLA] Empleado administrador creado con ID: {empleado.id}")
    else:
        print(f"[SEMILLA] El empleado administrador ya existe con ID: {empleado.id}")
        
    # Verificar si ya existe la cuenta de usuario asociada 
    usuario_existente = UsuarioDAO.buscar_por_nombre(nombre_usuario_admin)
    if usuario_existente is None:
        usuario_por_emp = UsuarioDAO.buscar_por_empleado(empleado.id)
        if usuario_por_emp is None:
            # Crear y vincular la cuenta de usuario con el hash de la contraseña
            usuario = Usuario(nombre_usuario=nombre_usuario_admin, empleado=empleado)
            usuario.establecer_contrasena(clave_inicial)
            UsuarioDAO.insertar(usuario)
            print(f"[SEMILLA] Cuenta de usuario '{nombre_usuario_admin}' creada correctamente.")
        else:
            print(f"[SEMILLA] El empleado ya tiene una cuenta de usuario asociada.")
    else:
        print(f"[SEMILLA] La cuenta de usuario '{nombre_usuario_admin}' ya existe.")
        
    print("[SEMILLA] Proceso de inicialización finalizado con éxito.")

if __name__ == "__main__":
    ejecutar_semilla()
