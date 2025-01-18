create database registro

create table humano (
id_persona int primary key identity not null,
nombre varchar(11) not null,
apellido varchar(11) not null,
f_nacimiento datetime not null,
provincia varchar(25) not null
);

select * from humano;