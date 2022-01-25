-- drop schema flight_reservation;
-- create schema flight_reservation;
-- drop database flight_reservation;


    
create table customer
	(customer_id		varchar(15),
     customer_name		varchar(20),
     address			varchar(40),
     city				varchar(20),
     state				varchar(20),
     zip				varchar(20),
     phone_number		numeric(10,0),
     gender				varchar(10),
     age				numeric(2,0),
     date_of_birth		varchar(10),
	 primary key (customer_id)
	); 
    
create table airport
	(airport_code		varchar(15),
	 address			varchar(40),
     city				varchar(20),
     state				varchar(20),
     zip				varchar(20),
     country			varchar(15),
	 primary key (airport_code)
	); 

create table gate
	(gate_id			varchar(15),
	 terminal			varchar(15),
     airport_code		varchar(15),
	 primary key (gate_id, terminal, airport_code),
     foreign key (airport_code) references airport (airport_code)
		on delete cascade
	); 
    
create table flight
	(flight_num			varchar(15),
     plane_type			varchar(15),
     airline			varchar(15),
     depart_airport		varchar(15),
     arrive_airport		varchar(15),
     depart_gate		varchar(15),
     arrive_gate		varchar(15),
     is_international	int default 0,
     has_pilot			int default 0,
     max_seats			int default 0,
     is_full			int default 0,
	 primary key (flight_num),
	 foreign key (depart_airport, depart_gate) references gate (airport_code, gate_id)
		on delete cascade,
	 foreign key (arrive_airport, arrive_gate) references gate (airport_code, gate_id)
		on delete cascade
	); 
    
create table seat
	(seat_num			varchar(5) NOT NULL,
     flight_num			varchar(15),
     is_booked			int default 0,
	 primary key (flight_num, seat_num),
	 foreign key (flight_num) references flight (flight_num)
		on delete cascade
	); 
    
create table trip
	(trip_id			varchar(15),
	 arrive_airport		varchar(15),
     depart_airport		varchar(15),
     customer_id		varchar(15),
	 flight_num			varchar(15),
     seat_num			varchar(15) default NULL,
	 primary key (trip_id),
     foreign key (customer_id) references customer (customer_id)
		on delete set null,
     foreign key (flight_num, seat_num) references seat (flight_num, seat_num)
		on delete set null
	); 

create table pilot
	(pilot_num			varchar(15),
     pilot_name			varchar(20),
	 airline			varchar(15),
     address			varchar(40),
     city				varchar(20),
     state				varchar(20),
     zip				varchar(20),
     phone_number		numeric(10,0),
     gender				varchar(10),
     age				numeric(2,0),
     date_of_birth		varchar(10),
	 primary key (pilot_num)
	); 

create table attendant
	(attendant_num		varchar(15),
	 attendant_name		varchar(20),
	 airline			varchar(15),
     address			varchar(40),
     city				varchar(20),
     state				varchar(20),
     zip				varchar(20),
     phone_number		numeric(10,0),
     gender				varchar(10),
     age				numeric(2,0),
     date_of_birth		varchar(10),
	 primary key (attendant_num)
	);
    

create table pilots_flight
	(pilot_num			varchar(15),
	 flight_num			varchar(15),
	 primary key (pilot_num, flight_num),
     foreign key (pilot_num) references pilot (pilot_num)
		on delete cascade,
     foreign key (flight_num) references flight (flight_num)
		on delete cascade
	);

create table attends_flight
	(attendant_num		varchar(15),
	 flight_num			varchar(15),
	 primary key (attendant_num, flight_num),
     foreign key (attendant_num) references attendant (attendant_num)
		on delete cascade,
     foreign key (flight_num) references flight (flight_num)
		on delete cascade
	);









