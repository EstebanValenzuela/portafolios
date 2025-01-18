create database formulario

create table empleado
(
idEmpleado int primary key not null,
nombre varchar(20) not null,
PApellido varchar(20)not null,
SApellido varchar(20)not null,
correo varchar (50) not null,
foto image
);

create table departamento
(
idDepartamento int primary key not null,
departamento varchar (20) not null
);

create table EmpDep
(
idDepartamento int references departamento(idDepartamento),
idEmpleado int references empleado(idEmpleado)
);

select * from empleado