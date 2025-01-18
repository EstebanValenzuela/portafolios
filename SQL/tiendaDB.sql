--create database tienda;

create table producto(
IdProducto int not null,
Nproducto varchar(20) not null,
precio int not null,
cantidad int not null,
Stotal int not null,
total float not null
);

insert into producto values(
1, 'mouse', 80, 1, 80, 85.4
);

select * from producto